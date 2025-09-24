import numpy as np
import plotly.graph_objects as go
import plotly.offline as offline


def scatter_plot_3d_plotly(X,y=None,filename='plot3d.html',fig_title='Plot'):
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
    
    Notes
    -----
    - The plot uses the 'Viridis' color scale for visualization.
    - Coordinate axes are hidden by default to focus on the data distribution.
    - The generated HTML file can be opened in any web browser.
    - For large datasets (>10,000 points), consider downsampling for better performance.
    """
    assert X.shape[1] == 3, "X debe tener 3 dimensiones"
    if y is not None:
        assert X.shape[0] == y.shape[0], "X y y deben tener la misma cantidad de puntos"
    else:
        y = np.zeros(X.shape[0])
    N = X.shape[0]
    # Extraer coordenadas x, y, z
    x = X[:, 0]
    y = X[:, 1]
    z = X[:, 2]

    # Crear la figura 3D
    fig = go.Figure(data=[go.Scatter3d(
        x=x,
        y=y,
        z=z,
        mode='markers',
        marker=dict(
            size=3,
            color=y,  # Colorear por valor de clase
            colorscale='Viridis',  # Escala de colores
            opacity=0.8
        ),
        text=[f'{y[i]}' for i in range(N)],  # Texto al hacer hover (opcional)
        hovertemplate='%{text}'
    )])

    # Configurar el layout para elementos de interfaz
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
