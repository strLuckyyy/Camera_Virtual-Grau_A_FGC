import numpy as np
from enum import Enum

#test
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from object import Object3D
import math

class ProjectionType(Enum):
    PERSPECTIVE = 1
    ORTHOGRAPHIC = 2

class Camera:    
    def normalize(self, v: np.ndarray) -> np.ndarray:
        norm = np.linalg.norm(v)
        if norm == 0:
            return v
        return v / norm
    
    def __init__(self, x: float = .0, y: float = .0, z: float = 5.,
                 pitch: float = .0, yaw: float = .0, roll: float = .0,
                 target: np.ndarray = np.array([.0, .0, .0]),
                 projection: ProjectionType = ProjectionType.PERSPECTIVE,
                 f: float = np.pi/4, width: int = 800, height: int = 600,
                 near: float = 0.1, far: float = 1000):
        
        self.position = np.array([x, y, z], dtype=float)
        self.rotation = np.array([pitch, yaw, roll], dtype=float) 
        self.target = np.array(target, dtype=float)
        
        self.projection = projection
        self.f = f
        
        self.width = width
        self.height = height
        
        self.near = near
        self.far = far
        
        # Window coordinates
        self.xminw, self.xmaxw = -1, 1
        self.yminw, self.ymaxw = -1, 1
        
        # Viewport coordinates
        self.xminv, self.xmaxv = 0, width
        self.yminv, self.ymaxv = 0, height
        
        # Orbit parameters
        self.radius = np.linalg.norm(self.position - self.target)
        self.theta = 0.0  # angle around Y axis
        self.phi = 0.0    # angle from XZ plane
    
    
    def get_position(self) -> np.ndarray: return self.position
    
    def get_rotation(self) -> np.ndarray: return self.rotation
    
    def get_target(self) -> np.ndarray: return self.target
    
    def get_view_matrix(self) -> np.ndarray:
        """
        Returns the camera view matrix by applying translation and rotation. If target is set, it functions as a lookAt.
        """
        
        if self.target is not None:
            forward = self.normalize(self.target - self.position)
        else:
            # If no target, define forward based on the rotation angles
            pitch, yaw, roll = self.rotation
            
            # Forward direction computed from angles
            forward = np.array([
            np.cos(pitch) * np.sin(yaw),
            np.sin(pitch),
            np.cos(pitch) * np.cos(yaw)
            ])
            forward = self.normalize(forward)
            
        # Camera basis vectors
        right = self.normalize(np.cross(forward, np.array([0, 1, 0])))
        up = np.cross(right, forward)

        # Apply roll (rotation around the camera's Z axis)
        if self.rotation[2] != 0:
            cos_r = np.cos(self.rotation[2])
            sin_r = np.sin(self.rotation[2])
            up = cos_r * up + sin_r * right
            right = np.cross(forward, up)
        
        # Build view matrix (R|t)
        return np.array([
            [right[0],   right[1],   right[2],   -np.dot(right, self.position)],
            [up[0],      up[1],      up[2],      -np.dot(up, self.position)],
            [-forward[0], -forward[1], -forward[2],  np.dot(forward, self.position)],
            [0, 0, 0, 1]
        ])
    
    # Projection methods
    
    def set_projection(self, projection: ProjectionType) -> None: self.projection = projection

    def toggle_projection(self) -> None:
        if self.projection == ProjectionType.PERSPECTIVE:
            self.projection = ProjectionType.ORTHOGRAPHIC
        else:
            self.projection = ProjectionType.PERSPECTIVE

    def project_vertex(self, v):
        # Transform to camera space
        v_cam = v @ self.get_view_matrix().T

        # Apply projection matrix
        if self.projection == ProjectionType.PERSPECTIVE:
            f = 1 / np.tan(self.f / 2)
            near, far = self.near, self.far
            P = np.array([
            [f, 0, 0, 0],
            [0, f, 0, 0],
            [0, 0, (far+near)/(near-far), 2*far*near/(near-far)],
            [0, 0, -1, 0]
            ])
        else:
            # Orthographic
            l, r = self.xminw, self.xmaxw
            b, t = self.yminw, self.ymaxw
            n, f = self.near, self.far
            P = np.array([
            [2/(r-l), 0, 0, -(r+l)/(r-l)],
            [0, 2/(t-b), 0, -(t+b)/(t-b)],
            [0, 0, 2/(n-f), -(f+n)/(f-n)],
            [0, 0, 0, 1]
            ])

        v_proj = v_cam @ P.T

        # Homogeneous division
        v_ndc = v_proj[:3] / (v_proj[3] if v_proj[3] != 0 else 1e-5)

        # Window → viewport
        x_pixel = self.xminv + (v_ndc[0]-self.xminw)*(self.xmaxv-self.xminv)/(self.xmaxw-self.xminw)
        y_pixel = self.yminv + (v_ndc[1]-self.yminw)*(self.ymaxv-self.yminv)/(self.ymaxw-self.yminw)

        return (x_pixel, y_pixel)
    
    # ------------------------------- #
    
    # Orbit methods
    
    def update_camera(self):
        # phi limiter to avoid gimbal lock
        #self.phi = max(-math.pi/2 + 0.01, min(math.pi/2 - 0.01, self.phi))

        # Convert spherical to Cartesian coordinates
        self.position[0] = self.target[0] + self.radius * math.cos(self.phi) * math.sin(self.theta)
        self.position[1] = self.target[1] + self.radius * math.sin(self.phi)
        self.position[2] = self.target[2] + self.radius * math.cos(self.phi) * math.cos(self.theta)

    def orbit_camera(self, d_theta=0.0, d_phi=0.0, d_radius=0.0):
        self.theta += d_theta
        self.phi += d_phi
        self.radius = max(1.0, self.radius + d_radius)
        self.update_camera()
        
    # ------------------------------- #
    