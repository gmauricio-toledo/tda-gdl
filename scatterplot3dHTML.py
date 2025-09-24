import numpy as np
import plotly.graph_objects as go
import plotly.offline as offline


def scatter_plot_3d_plotly(X, y=None, hover_info=None, filename='plot3d.html', fig_title='Plot'):
    """
    Generate an interactive 3D scatter plot using Plotly.
    
    This function creates a 3D visualization of data points with optional coloring
    based on class labels. The plot is saved as an interactive HTML file.
    
    Parameters
    ----------
    X : array-like of shape (n_samples, 3)
        Input data with exactly 3 features for 3D visualization.
        
    y : array-like of shape (n_samples,), default=None
        Target values used for coloring the points. If None, all points 
        will be colored uniformly.
        
    hover_info : array-like of shape (n_samples,), default=None
        Custom text to display when hovering over points. If None and y is provided,
        shows class labels. If None and y is None, hover is disabled.
        
    filename : str, default='plot3d.html'
        Name of the output HTML file where the plot will be saved.
        
    fig_title : str, default='Plot'
        Title to display above the plot.
    
    Returns
    -------
    None
        The function saves the plot as an HTML file and does not return any value.
    
    Raises
    ------
    AssertionError
        If X does not have exactly 3 dimensions.
        If X and y have different number of samples.
    
    Examples
    --------
    >>> import numpy as np
    >>> from sklearn.decomposition import PCA
    >>> from sklearn.datasets import load_iris
    >>> 
    >>> # Load iris dataset and apply PCA
    >>> iris = load_iris()
    >>> X_pca = PCA(n_components=3).fit_transform(iris.data)
    >>> 
    >>> # Create 3D scatter plot colored by target
    >>> scatter_plot_3d_plotly(X_pca, y=iris.target, 
    ...                       filename='iris_pca.html',
    ...                       fig_title='Iris Dataset - PCA 3D')
    >>> 
    >>> # Create plot without target coloring
    >>> scatter_plot_3d_plotly(X_pca, filename='iris_no_labels.html')
    >>> 
    >>> # Create plot with custom hover text
    >>> custom_text = [f'Sample {i}' for i in range(len(X_pca))]
    >>> scatter_plot_3d_plotly(X_pca, y=iris.target, hover_info=custom_text,
    ...                       filename='iris_custom_hover.html')
    
    Notes
    -----
    - The plot uses discrete colors for categorical data.
    - Coordinate axes are hidden by default to focus on the data distribution.
    - The generated HTML file can be opened in any web browser.
    - For large datasets (>10,000 points), consider downsampling for better performance.
    - When hover_info=None and y=None, hover information is disabled for cleaner visualization.
    - When hover_info is provided, it overrides default class label hover text.
    """
    assert X.shape[1] == 3, "X debe tener 3 dimensiones"
    
    # Extraer coordenadas
    x_coord = X[:, 0]
    y_coord = X[:, 1]
    z_coord = X[:, 2]
    
    if y is not None:
        assert X.shape[0] == y.shape[0], "X y y deben tener la misma cantidad de puntos"
        
    if hover_info is not None:
        assert X.shape[0] == len(hover_info), "X y hover_info deben tener la misma cantidad de puntos"
        
        # Obtener labels únicos y mapear a números secuenciales para colores discretos
        unique_labels = np.unique(y)
        n_classes = len(unique_labels)
        
        # Mapear cada label único a un número secuencial
        label_to_num = {label: i for i, label in enumerate(unique_labels)}
        numeric_labels = [label_to_num[label] for label in y]
        
        # Determinar texto para hover
        if hover_info is not None:
            hover_text = [f'{text}' for text in hover_info]
            hover_template = '%{text}<extra></extra>'
        else:
            # Si no hay hover_info personalizado, usar las etiquetas de clase
            hover_text = [f'{label}' for label in y]
            hover_template = 'Clase: %{text}<extra></extra>'
        
        # Para pocas clases, usar colores específicos más contrastantes
        if n_classes <= 10:
            # Colores discretos bien diferenciados
            discrete_colors = ['red', 'blue', 'green', 'orange', 'purple', 
                             'brown', 'pink', 'gray', 'olive', 'cyan']
            point_colors = [discrete_colors[i] for i in numeric_labels]
            
            fig = go.Figure(data=[go.Scatter3d(
                x=x_coord,
                y=y_coord,
                z=z_coord,
                mode='markers',
                marker=dict(
                    size=3,
                    color=point_colors,  # Colores específicos
                    opacity=0.8
                ),
                text=hover_text,
                hovertemplate=hover_template
            )])
        else:
            # Para muchas clases, usar escala continua de Plotly
            fig = go.Figure(data=[go.Scatter3d(
                x=x_coord,
                y=y_coord,
                z=z_coord,
                mode='markers',
                marker=dict(
                    size=3,
                    color=numeric_labels,
                    colorscale='turbo',  # Escala válida de Plotly con muchos colores
                    cmin=0,
                    cmax=n_classes-1,
                    opacity=0.8
                ),
                text=hover_text,
                hovertemplate=hover_template
            )])
    else:
        # Sin etiquetas: verificar si hay hover personalizado
        if hover_info is not None:
            fig = go.Figure(data=[go.Scatter3d(
                x=x_coord,
                y=y_coord,
                z=z_coord,
                mode='markers',
                marker=dict(
                    size=3,
                    color='blue',
                    opacity=0.8
                ),
                text=[f'{text}' for text in hover_info],
                hovertemplate='%{text}<extra></extra>'
            )])
        else:
            # Sin etiquetas ni hover personalizado: sin hover
            fig = go.Figure(data=[go.Scatter3d(
                x=x_coord,
                y=y_coord,
                z=z_coord,
                mode='markers',
                marker=dict(
                    size=3,
                    color='blue',
                    opacity=0.8
                ),
                hoverinfo='none'  # Desactivar hover completamente
            )])

    # Configurar el layout
    fig.update_layout(
        title=fig_title,
        scene=dict(
            # Ocultar ejes coordenados
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
            # Configurar cámara y aspecto
            camera=dict(
                up=dict(x=0, y=0, z=1),
                center=dict(x=0, y=0, z=0),
                eye=dict(x=1.2, y=1.2, z=1.2)
            )
        ),
        # Ocultar elementos de la interfaz
        showlegend=False,
        margin=dict(l=0, r=0, b=0, t=50),
    )
    
    # Guardar como archivo HTML
    offline.plot(fig, filename=filename, auto_open=False)
