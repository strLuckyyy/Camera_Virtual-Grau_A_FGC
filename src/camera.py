import numpy as np
from enum import Enum

#test
import tkinter as tk
from object import Object3D
import math

class ProjectionType(Enum):
    PERSPECTIVE = 1
    ORTHOGRAPHIC = 2

class Camera:
    '''
    
    translação e rotação da câmera:
    x, y, z: posição da câmera
    pitch, yaw, roll: ângulos de rotação da câmera em radianos
    
    lookat
    target: ponto para o qual a câmera está olhando (np.array de 3 elementos)
    
    projeção: -> Enum(ProjectionType): Perspectiva ou Ortográfica
    
    f: distância focal (distância entre a câmera e o plano de projeção)
    width, height: dimensões do plano de projeção (em pixels)
    near, far: planos de corte próximo e distante
    
    mapeamento
    window coordinates:
    xminw = -1
    xmaxw = 1
    yminw = -1
    ymaxw = 1
    
    viewport coordinates:
    xminv = 0
    xmaxv = width
    yminv = 0
    ymaxv = height
    
    '''
    
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
        Computes and returns the view matrix for the camera, which transforms world coordinates
        world_up = np.array([0, 1, 0])
        # If forward is parallel to world_up, use a different up vector to avoid zero right vector
        if np.allclose(np.abs(np.dot(forward, world_up)), 1.0):
            world_up = np.array([0, 0, 1])
        right = self.normalize(np.cross(forward, world_up))

        Returns:
            np.ndarray: A 4x4 view matrix as a NumPy array.
        """
        # Calculate the forward, right, and up vectors
        forward = self.normalize(self.target - self.position)
        right = self.normalize(np.cross(forward, np.array([0, 1, 0])))
        up = np.cross(right, forward)
        
        # Create the view matrix
        view_matrix = np.array([
            [right[0], right[1], right[2], -np.dot(right, self.position)],
            [up[0], up[1], up[2], -np.dot(up, self.position)],
            [-forward[0], -forward[1], -forward[2], np.dot(forward, self.position)],
            [0, 0, 0, 1]
        ])
        
        return view_matrix
    
    # Projection methods
    
    def set_projection(self, projection: ProjectionType) -> None: self.projection = projection

    def switch_projection(self) -> None:
        if self.projection == ProjectionType.PERSPECTIVE:
            self.projection = ProjectionType.ORTHOGRAPHIC
        else:
            self.projection = ProjectionType.PERSPECTIVE

    def project_vertex(self, v) -> tuple:
        view_matrix = cam.get_view_matrix()
        v_cam = v @ view_matrix.T 
        
        if cam.projection == ProjectionType.PERSPECTIVE:
            fov = cam.f
            z = v_cam[2] if v_cam[2] != 0 else 1e-5
            x_proj = (v_cam[0] / -z) * (WIDTH/2) * (1/np.tan(fov/2)) + WIDTH/2
            y_proj = -(v_cam[1] / -z) * (HEIGHT/2) * (1/np.tan(fov/2)) + HEIGHT/2
        else:
            x_proj = (v_cam[0] + 1) * (WIDTH/2)
            y_proj = (-v_cam[1] + 1) * (HEIGHT/2)

        return (x_proj, y_proj)
    
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
    

# testar a camera, deve mostrar o objeto base na tela com o tkinter com botões que movimentam a camera 10px pra cima, baixo, esquerda, direita, frente e trás
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Camera Test")
    
    WIDTH, HEIGHT = 800, 600
    canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
    canvas.pack()
    
    cam = Camera(width=WIDTH, height=HEIGHT)
    obj = Object3D()

    def draw():
        canvas.delete("all")
        verts = obj.get_vertices()
        projected = [cam.project_vertex(v) for v in verts]
        for edge in obj.get_edges():
            p1 = projected[edge[0]]
            p2 = projected[edge[1]]
            canvas.create_line(p1[0], p1[1], p2[0], p2[1], fill="white")

    # Botões
    btns = tk.Frame(root)
    btns.pack()

    value = .3
    zoom = 0.5

    tk.Button(btns, text="↑ Cima", command=lambda: [cam.orbit_camera(d_phi=value), draw()]).grid(row=0, column=1)
    tk.Button(btns, text="↓ Baixo", command=lambda: [cam.orbit_camera(d_phi=-value), draw()]).grid(row=2, column=1)
    
    tk.Button(btns, text="← Esquerda", command=lambda: [cam.orbit_camera(d_theta=-value), draw()]).grid(row=1, column=0)
    tk.Button(btns, text="→ Direita", command=lambda: [cam.orbit_camera(d_theta=value), draw()]).grid(row=1, column=2)
    
    tk.Button(btns, text="Zoom +", command=lambda: [cam.orbit_camera(d_radius=-zoom), draw()]).grid(row=0, column=2)
    tk.Button(btns, text="Zoom -", command=lambda: [cam.orbit_camera(d_radius=zoom), draw()]).grid(row=2, column=2)
    
    tk.Button(btns, text="Mudar Projeção", command=lambda: [cam.switch_projection(), draw()]).grid(row=1, column=1)

    draw()
    root.mainloop()
