import numpy as np
import tkinter as tk
from object import Object3D
from camera import Camera
import math

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Camera Test")
    
    WIDTH, HEIGHT = 800, 600
    canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
    canvas.pack()
    
    obj = Object3D()
    cam = Camera(width=WIDTH, height=HEIGHT, target=obj.get_position())

    def draw():
        canvas.delete("all")
        verts = obj.get_vertices()
        projected = [cam.project_vertex(v) for v in verts]
        for edge in obj.get_edges():
            p1 = projected[edge[0]]
            p2 = projected[edge[1]]
            canvas.create_line(p1[0], p1[1], p2[0], p2[1], fill="red")

    # Botões
    btns = tk.Frame(root)
    btns.pack()

    value = .2

    tk.Button(btns, text="↑ Cima", command=lambda: [cam.orbit(d_phi=value), draw()]).grid(row=0, column=1)
    tk.Button(btns, text="↓ Baixo", command=lambda: [cam.orbit(d_phi=-value), draw()]).grid(row=2, column=1)
    tk.Button(btns, text="← Esquerda", command=lambda: [cam.orbit(d_theta=-value), draw()]).grid(row=1, column=0)
    tk.Button(btns, text="→ Direita", command=lambda: [cam.orbit(d_theta=value), draw()]).grid(row=1, column=2)
    
    tk.Button(btns, text="Roll ←", command=lambda: [cam.roll(-value), draw()]).grid(row=0, column=0)
    tk.Button(btns, text="Roll →", command=lambda: [cam.roll(value), draw()]).grid(row=0, column=2)
    
    tk.Button(btns, text="Reset Cam", command=lambda: [cam.reset(), draw()]).grid(row=1, column=3)
    tk.Button(btns, text="Reset Obj", command=lambda: [obj.reset(), draw()]).grid(row=2, column=3)
    
    tk.Button(btns, text="Mudar Projeção", command=lambda: [cam.toggle_projection(), draw()]).grid(row=1, column=1)
    
    # traslada a camera
    tk.Button(btns, text="cam x", command=lambda: [cam.translate([value, 0, 0]), draw()]).grid(row=3, column=0)
    tk.Button(btns, text="cam y", command=lambda: [cam.translate([0, value, 0]), draw()]).grid(row=3, column=1)
    tk.Button(btns, text="cam z", command=lambda: [cam.translate([0, 0, value]), draw()]).grid(row=3, column=2)
    
    # traslada o objeto
    tk.Button(btns, text="obj t ←", command=lambda: [obj.translate([value, 0, 0]), draw()]).grid(row=4, column=0)
    tk.Button(btns, text="obj t ↑", command=lambda: [obj.translate([0, value, 0]), draw()]).grid(row=4, column=1)
    tk.Button(btns, text="obj t f", command=lambda: [obj.translate([0, 0, value]), draw()]).grid(row=4, column=2)
    
    # rotaciona o objeto
    tk.Button(btns, text="obj r x", command=lambda: [obj.pitch(value), draw()]).grid(row=5, column=0)
    tk.Button(btns, text="obj r y", command=lambda: [obj.yaw(value), draw()]).grid(row=5, column=1)
    tk.Button(btns, text="obj r z", command=lambda: [obj.roll(value), draw()]).grid(row=5, column=2)
    
    # escala o objeto
    tk.Button(btns, text="obj s +", command=lambda: [obj.scale([1.1, 1.1, 1.1]), draw()]).grid(row=6, column=0)
    tk.Button(btns, text="obj s -", command=lambda: [obj.scale([0.9, 0.9, 0.9]), draw()]).grid(row=6, column=2)
    
    # Exemplo: muda para uma viewport menor no centro do canvas
    def set_custom_viewport():
        cam.set_viewport(200*2, 600*2, 150*2, 450*2)
        draw()

    # Exemplo: volta para a viewport padrão (igual ao window [-1,1])
    def reset_viewport():
        cam.set_viewport(0, cam.width, 0, cam.height)
        draw()

    # Adicionando os botões ao seu frame
    tk.Button(btns, text="Viewport Custom", command=set_custom_viewport).grid(row=7, column=1)
    tk.Button(btns, text="Viewport Reset", command=reset_viewport).grid(row=7, column=3)

    draw()
    root.mainloop()