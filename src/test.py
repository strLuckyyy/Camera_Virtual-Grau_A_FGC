import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from matplotlib.collections import LineCollection
import numpy as np
from object import Object3D
from camera import Camera

# --- Setup object and camera ---
obj = Object3D()
cam = Camera(x=0, y=0, z=5, target=np.array([0, 0, 0]))

# --- Create figure with GridSpec ---
fig = plt.figure(figsize=(8, 6))
gs = fig.add_gridspec(5, 6, hspace=0.3, wspace=0.3)

# Drawing axis occupies the top 4 rows
ax_draw = fig.add_subplot(gs[0:4, :])
ax_draw.set_aspect('equal')
ax_draw.set_xlim(0, cam.width)
ax_draw.set_ylim(0, cam.height)

# --- Function to draw the object ---
def draw_object():
    ax_draw.cla()
    lines = [
        [cam.project_vertex(obj.vertices[i]), cam.project_vertex(obj.vertices[j])]
        for i, j in obj.get_edges()
    ]
    ax_draw.add_collection(LineCollection(lines, colors='red', linewidths=2))
    ax_draw.set(aspect='equal', xlim=(0, cam.width), ylim=(0, cam.height))
    fig.canvas.draw_idle()

# --- Camera movement ---
def move_camera(dtheta=0.0, dphi=0.0, dradius=0.0):
    cam.orbit_camera(d_theta=dtheta, d_phi=dphi, d_radius=dradius)
    draw_object()
    
def toggle_projection(event):
    cam.toggle_projection()
    draw_object()

# --- Button layout using GridSpec ---
button_axes = {
    "Up":       [0.45, 0.15, 0.1, 0.06],
    "Down":     [0.45, 0.05, 0.1, 0.06],
    "Left":     [0.33, 0.1, 0.1, 0.06],
    "Right":    [0.57, 0.1, 0.1, 0.06],
    "Forward":  [0.76, 0.15, 0.1, 0.06],
    "Back":     [0.76, 0.05, 0.1, 0.06],
    "Projection":[0.05, 0.1, 0.15, 0.06]
}

val = .3

button_callbacks = {
    "Up": lambda event: move_camera(dphi=val),
    "Down": lambda event: move_camera(dphi=-val),
    "Left": lambda event: move_camera(dtheta=-val),
    "Right": lambda event: move_camera(dtheta=val),
    "Forward": lambda event: move_camera(dradius=-val),
    "Back": lambda event: move_camera(dradius=val),
    "Projection": toggle_projection
}

buttons = []
for label, ax_loc in button_axes.items():
    ax_btn = fig.add_axes((ax_loc[0], ax_loc[1], ax_loc[2], ax_loc[3]))
    btn = Button(ax_btn, label)
    btn.on_clicked(button_callbacks[label])
    buttons.append(btn)

# --- Draw for the first time ---
draw_object()
plt.show()
