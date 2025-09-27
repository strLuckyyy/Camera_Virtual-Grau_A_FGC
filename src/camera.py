import math
import numpy as np
from enum import Enum

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
        """Initializes the Camera with position, rotation (in radians), target, projection type, and other parameters."""
        
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


    def set_perspective_params(self, fov_degrees, near, far):
        """Define os parâmetros para a projeção perspectiva."""
        self.f = math.radians(fov_degrees)
        self.near = near
        self.far = far
        self.projection = ProjectionType.PERSPECTIVE
        print(f"Projeção alterada para Perspectiva (FoV={fov_degrees}°, Near={near}, Far={far}).")


    def set_orthographic_params(self, left, right, bottom, top):
        """Define os parâmetros para a projeção paralela (ortográfica)."""
        self.xminw = left
        self.xmaxw = right
        self.yminw = bottom
        self.ymaxw = top
        self.projection = ProjectionType.ORTHOGRAPHIC
        print(f"Projeção alterada para Paralela (L={left}, R={right}, B={bottom}, T={top}).")


    
    def reset(self):
        self.__init__(width=self.width, height=self.height)
        
    # Getters
     
    def get_position(self) -> np.ndarray: return self.position
    
    def get_rotation(self) -> np.ndarray: return self.rotation
    
    def get_target(self) -> np.ndarray: return self.target
    
    def set_target(self, target: np.ndarray) -> None:
        self.target = np.array(target, dtype=float)
        self.update()
    
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
        """Projects a 3D vertex to 2D screen coordinates using the camera's view and projection matrices."""
        v_cam = v @ self.get_view_matrix().T

        # Projection matrix
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
            # Orthographic projection
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

        # Convert to NDC
        v_ndc = v_proj[:3] / -(v_proj[3] if v_proj[3] != 0 else 1e-5)

        # Map NDC to viewport
        x_pixel, y_pixel = self.window_to_viewport(v_ndc[0], v_ndc[1])

        return x_pixel, y_pixel


    # ------------------------------- #

    # Mapping methods

    def set_viewport(self, xminv, xmaxv, yminv, ymaxv):
        """Define the viewport bounds in pixels."""
        
        self.xminv, self.xmaxv = xminv, xmaxv
        self.yminv, self.ymaxv = yminv, ymaxv

    def set_window(self, xminw, xmaxw, yminw, ymaxw):
        """Define the window bounds in normalized coordinates."""
        
        self.xminw, self.xmaxw = xminw, xmaxw
        self.yminw, self.ymaxw = yminw, ymaxw
    
    def window_to_viewport(self, xw, yw):
        """Convert window (NDC) coordinates to viewport pixel coordinates. xw, yw are in the ranges [xminw, xmaxw] and [yminw, ymaxw]."""
        
        xv = self.xminv + (xw - self.xminw) * (self.xmaxv - self.xminv) / (self.xmaxw - self.xminw)
        yv = self.yminv + (yw - self.yminw) * (self.ymaxv - self.yminv) / (self.ymaxw - self.yminw)
        return xv, yv
    
    def viewport_to_window(self, xv, yv):
        """Convert viewport coordinates in pixels to window (NDC)."""
        
        xw = self.xminw + (xv - self.xminv) * (self.xmaxw - self.xminw) / (self.xmaxv - self.xminv)
        yw = self.yminw + (yv - self.yminv) * (self.ymaxw - self.yminw) / (self.ymaxv - self.yminv)
        return xw, yw

    # ------------------------------- #
    
    # Orbit methods
    
    def update(self):
        """Update camera position based on spherical coordinates (radius, theta, phi) around the target."""
        #self.phi = max(-math.pi/2 + 0.01, min(math.pi/2 - 0.01, self.phi))

        # Convert spherical to Cartesian coordinates
        self.position[0] = self.target[0] + self.radius * math.cos(self.phi) * math.sin(self.theta)
        self.position[1] = self.target[1] + self.radius * math.sin(self.phi)
        self.position[2] = self.target[2] + self.radius * math.cos(self.phi) * math.cos(self.theta)

    def orbit(self, d_theta=0.0, d_phi=0.0, d_radius=0.0):
        """Orbit the camera around the target by changing theta, phi, and radius."""
        self.theta += d_theta
        self.phi += d_phi
        self.radius = max(1.0, self.radius + d_radius)
        self.update()
    
    def roll(self, d_roll=0.0):
        """Roll the camera around its forward axis."""
        self.rotation[2] += d_roll
        self.rotation = self.rotation % (2 * np.pi)
        self.update()
    
    # ------------------------------- #
    
    # Translate method
    def translate(self, translation_vector: list) -> None:
        """Translate the camera and its target by a given vector."""
        translation = np.array(translation_vector, dtype=float)
        self.position += translation
        if self.target is not None:
            self.target += translation
        self.update()
    
    # ------------------------------- #
    