import numpy as np

class Object3D:
    position: np.ndarray
   
    def __init__(self, vertices = None, edges = None, x: float = 0, y: float = 0, z: float = 0):
        self.position = np.array([x, y, z])
        
        if vertices is None:
            # Default vertices for a pyramid
            self.vertices = np.array([
                [-0.5, -0.25, -0.5, 1],  #P0
                [0.5, -0.25, -0.5, 1],   #P1
                [-0.5, -0.25, 0.5, 1],   #P2
                [0.5, -0.25, 0.5, 1],    #P3
                [0.0, 0.25, 0.0, 1]      #P4 = topo da pirâmide
            ])
        else:
            self.vertices = np.array(vertices)

        if edges is None:
            # Default edges for a pyramid
            self.edges = [[0, 1], [1, 3], [3, 2], [2, 0], # base edges
                          [0, 4], [1, 4], [2, 4], [3, 4]] # side edges
        else:
            self.edges = edges
    
    def get_position(self) -> np.ndarray:
        return self.position
    
    def get_vertices(self) -> np.ndarray:
        return self.vertices
    
    def get_edges(self) -> list:
        return self.edges
    
    # Transformation methods
    
    def translate(self, translation_vector: list) -> None:
        translation_matrix = np.array([
            [1, 0, 0, translation_vector[0]],
            [0, 1, 0, translation_vector[1]],
            [0, 0, 1, translation_vector[2]],
            [0, 0, 0, 1]
        ])
        self.vertices = self.vertices @ translation_matrix.T
    
    def scale(self, scale_factors: list) -> None:
        scale_matrix = np.array([
            [scale_factors[0], 0, 0, 0],
            [0, scale_factors[1], 0, 0],
            [0, 0, scale_factors[2], 0],
            [0, 0, 0, 1]
        ])
        self.vertices = self.vertices @ scale_matrix.T
        
    def rotate_x(self, angle: float) -> None:
        cos_a = np.cos(angle)
        sin_a = np.sin(angle)
        rotation_matrix = np.array([
            [1, 0, 0, 0],
            [0, cos_a, -sin_a, 0],
            [0, sin_a, cos_a, 0],
            [0, 0, 0, 1]
        ])
        self.vertices = self.vertices @ rotation_matrix.T
    
    def rotate_y(self, angle: float) -> None:
        cos_a = np.cos(angle)
        sin_a = np.sin(angle)
        rotation_matrix = np.array([
            [cos_a, 0, sin_a, 0],
            [0, 1, 0, 0],
            [-sin_a, 0, cos_a, 0],
            [0, 0, 0, 1]
        ])
        self.vertices = self.vertices @ rotation_matrix.T
        
    def rotate_z(self, angle: float) -> None:
        cos_a = np.cos(angle)
        sin_a = np.sin(angle)
        rotation_matrix = np.array([
            [cos_a, -sin_a, 0, 0],
            [sin_a, cos_a, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])
        self.vertices = self.vertices @ rotation_matrix.T
    
    # ------------------------------- #
    
    def reset(self) -> None:
        self.__init__()
        
    