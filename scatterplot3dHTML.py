import numpy as np
import plotly.graph_objects as go
import plotly.offline as offline


def scatter_plot_3d_plotly(X, y=None, hover_info=None, filename='plot3d.html', fig_title='Plot'):
    """
    Generate an interactive 3D scatter plot using Plotly.
    """
    
    # Convertir a numpy array y asegurar formato correcto
    X = np.asarray(X, dtype=float)
    
    assert X.shape[1] == 3, f"X debe tener 3 dimensiones, tiene {X.shape[1]}"
    assert X.shape[0] > 0, "X no puede estar vacío"
    
    # Extraer coordenadas como listas de Python
    x_coord = X[:, 0].tolist()
    y_coord = X[:, 1].tolist()
    z_coord = X[:, 2].tolist()
    
    if y is not None:
        y = np.asarray(y)
        assert X.shape[0] == y.shape[0], "X y y deben tener la misma cantidad de puntos"
        
    if hover_info is not None:
        assert X.shape[0] == len(hover_info), "X y hover_info deben tener la misma cantidad de puntos"
        # Limpiar hover_info: reemplazar None/NaN con string vacío
        try:
            hover_info = [str(text) if text is not None and str(text) != 'nan' else '' for text in hover_info]
            print(f"8. Hover_info limpio. Primeros 3: {hover_info[:3]}")
        except Exception as e:
            print(f"ERROR en limpieza de hover_info: {e}")
            raise
        
    if y is not None:
        # Obtener labels únicos y mapear a números secuenciales para colores discretos
        unique_labels = np.unique(y)
        n_classes = len(unique_labels)
        
        # Mapear cada label único a un número secuencial
        label_to_num = {label: i for i, label in enumerate(unique_labels)}
        numeric_labels = [label_to_num[label] for label in y]
        
        # Determinar texto para hover
        if hover_info is not None:
            hover_text = hover_info
            hover_template = '%{text}<extra></extra>'
        else:
            # Si no hay hover_info personalizado, usar las etiquetas de clase
            hover_text = [str(label) for label in y]
            hover_template = 'Clase: %{text}<extra></extra>'
        
        # Para pocas clases, usar colores específicos más contrastantes
        if n_classes <= 10:
            # Colores discretos bien diferenciados
            discrete_colors = ['red', 'blue', 'green', 'orange', 'purple', 
                             'brown', 'pink', 'gray', 'olive', 'cyan']
            point_colors = [discrete_colors[i] for i in numeric_labels]
            
            trace = go.Scatter3d(
                x=x_coord,
                y=y_coord,
                z=z_coord,
                mode='markers',
                marker=dict(
                    size=3,
                    color=point_colors,
                    opacity=0.8
                ),
                text=hover_text,
                hovertemplate=hover_template
            )
        else:
            # Para muchas clases, usar escala continua de Plotly
            trace = go.Scatter3d(
                x=x_coord,
                y=y_coord,
                z=z_coord,
                mode='markers',
                marker=dict(
                    size=3,
                    color=numeric_labels,
                    colorscale='turbo',
                    cmin=0,
                    cmax=n_classes-1,
                    opacity=0.8
                ),
                text=hover_text,
                hovertemplate=hover_template
            )
    else:
        # Sin etiquetas: verificar si hay hover personalizado
        if hover_info is not None:
            
            try:
                trace = go.Scatter3d(
                    x=x_coord,
                    y=y_coord,
                    z=z_coord,
                    mode='markers',
                    marker=dict(
                        size=3,
                        color='blue',
                        opacity=0.8
                    ),
                    text=hover_info,
                    hovertemplate='%{text}<extra></extra>'
                )
                print("12. Trace creado exitosamente")
            except Exception as e:
                print(f"ERROR creando trace: {e}")
                print(f"ERROR tipo: {type(e)}")
                import traceback
                traceback.print_exc()
                raise
        else:
            # Sin etiquetas ni hover personalizado: sin hover
            trace = go.Scatter3d(
                x=x_coord,
                y=y_coord,
                z=z_coord,
                mode='markers',
                marker=dict(
                    size=3,
                    color='blue',
                    opacity=0.8
                ),
                hoverinfo='none'
            )
    
    # Crear figura con el trace
    fig = go.Figure(data=[trace])

    # Configurar el layout
    fig.update_layout(
        title=fig_title,
        scene=dict(
            xaxis=dict(
                visible=False,
                showbackground=False,
                showgrid=False,
                zeroline=False,
            ),
            yaxis=dict(
                visible=False,
                showbackground=False,
                showgrid=False,
                zeroline=False,
            ),
            zaxis=dict(
                visible=False,
                showbackground=False,
                showgrid=False,
                zeroline=False,
            ),
            camera=dict(
                up=dict(x=0, y=0, z=1),
                center=dict(x=0, y=0, z=0),
                eye=dict(x=1.2, y=1.2, z=1.2)
            )
        ),
        showlegend=False,
        margin=dict(l=0, r=0, b=0, t=50),
    )
    
    # Guardar como archivo HTML
    offline.plot(fig, filename=filename, auto_open=False)
