import numpy as np
from typing import Sequence, List, Optional

class Object3D:
    position: np.ndarray
   
    def __init__(self, vertices: Optional[Sequence[Sequence[float]]] = None,
                 edges: Optional[List[List[int]]] = None,
                 x: float = 0.0, y: float = 0.0, z: float = 0.0):
        self.position = np.array([x, y, z], dtype=float)
        """ Vertices should be a list of lists or a 2D array with shape (n, 4) where each vertex is [x, y, z, 1.0] """
                
        if vertices is None:
            # Default vertices for a pyramid (use floats)
            self.vertices = np.array([
                [-0.5, -0.25, -0.5, 1.0],  #P0
                [0.5, -0.25, -0.5, 1.0],   #P1
                [-0.5, -0.25, 0.5, 1.0],   #P2
                [0.5, -0.25, 0.5, 1.0],    #P3
                [0.0, 0.25, 0.0, 1.0]      #P4 = topo da pirâmide
            ], dtype=float)
        else:
            self.vertices = np.array(vertices, dtype=float)

        if edges is None:
            # Default edges for a pyramid (indices remain ints)
            self.edges = [[0, 1], [1, 3], [3, 2], [2, 0], # base edges
                          [0, 4], [1, 4], [2, 4], [3, 4]] # side edges
        else:
            self.edges = edges

    def reset(self):
        """Resets the object to its initial state."""
        self.__init__()
    
    def get_position(self) -> np.ndarray:
        return self.position
    
    def get_vertices(self) -> np.ndarray:
        return self.vertices
    
    def get_edges(self) -> List[List[int]]:
        return self.edges
    
    # Transformation methods
    
    def translate(self, translation_vector: Sequence[float]) -> None:
        """
        Translates the object by the given vector. Translation_vector should be a sequence of three floats [tx, ty, tz].
        """
        tx, ty, tz = float(translation_vector[0]), float(translation_vector[1]), float(translation_vector[2])
        translation_matrix = np.array([
            [1.0, 0.0, 0.0, tx],
            [0.0, 1.0, 0.0, ty],
            [0.0, 0.0, 1.0, tz],
            [0.0, 0.0, 0.0, 1.0]
        ], dtype=float)
        self.vertices = self.vertices @ translation_matrix.T
        self.position += np.array([tx, ty, tz], dtype=float)
    
    def scale(self, scale_factors: Sequence[float]) -> None:
        """
        Scales the object by the given scale factors. Scale_factors should be a sequence of three floats [sx, sy, sz].
        """
        sx, sy, sz = float(scale_factors[0]), float(scale_factors[1]), float(scale_factors[2])
        scale_matrix = np.array([
            [sx, 0.0, 0.0, 0.0],
            [0.0, sy, 0.0, 0.0],
            [0.0, 0.0, sz, 0.0],
            [0.0, 0.0, 0.0, 1.0]
        ], dtype=float)
        self.vertices = self.vertices @ scale_matrix.T
        
    def pitch(self, angle: float) -> None:
        """
        Rotates the object around the X-axis by the given angle in radians. Around X
        """
        cos_a = float(np.cos(angle))
        sin_a = float(np.sin(angle))
        rotation_matrix = np.array([
            [1.0, 0.0, 0.0, 0.0],
            [0.0, cos_a, -sin_a, 0.0],
            [0.0, sin_a, cos_a, 0.0],
            [0.0, 0.0, 0.0, 1.0]
        ], dtype=float)
        self.vertices = self.vertices @ rotation_matrix.T
    
    def yaw(self, angle: float) -> None:
        """
        Rotates the object around the Y-axis by the given angle in radians. Around Y
        """
        cos_a = float(np.cos(angle))
        sin_a = float(np.sin(angle))
        rotation_matrix = np.array([
            [cos_a, 0.0, sin_a, 0.0],
            [0.0, 1.0, 0.0, 0.0],
            [-sin_a, 0.0, cos_a, 0.0],
            [0.0, 0.0, 0.0, 1.0]
        ], dtype=float)
        self.vertices = self.vertices @ rotation_matrix.T
        
    def roll(self, angle: float) -> None:
        """
        Rotates the object around the Z-axis by the given angle in radians. Around Z
        """
        cos_a = float(np.cos(angle))
        sin_a = float(np.sin(angle))
        rotation_matrix = np.array([
            [cos_a, -sin_a, 0.0, 0.0],
            [sin_a, cos_a, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 1.0]
        ], dtype=float)
        self.vertices = self.vertices @ rotation_matrix.T
    
    # ------------------------------- #
