'''
    Trabalho desenvolvido para a disciplina de Fundamentos de Computação Gráfica - Grau A
    Desenvolvido por Abrahão Francis e Marcos Rocha
    Entregue: 03/10/2025
'''


# main.py - Versão com Interface Gráfica (GUI)

import numpy as np
import tkinter as tk
from tkinter import ttk  # Usaremos para um estilo de widget melhor
from object import Object3D
from camera import Camera, ProjectionType
import math

# --- FUNÇÕES HANDLER (A LÓGICA POR TRÁS DOS BOTÕES) ---

def apply_translation():
    try:
        tx = float(entry_tx.get())
        ty = float(entry_ty.get())
        tz = float(entry_tz.get())
        obj.translate([tx, ty, tz])
        draw()
    except ValueError:
        print("Erro: Entrada de translação inválida.")

def apply_scale():
    try:
        sx = float(entry_sx.get())
        sy = float(entry_sy.get())
        sz = float(entry_sz.get())

        # Validação para impedir escala negativa ou zero
        if sx <= 0 or sy <= 0 or sz <= 0:
            print("Erro: Fatores de escala devem ser números positivos maiores que zero.")
            return  # Para a execução da função aqui

        obj.scale([sx, sy, sz])
        draw()
    except ValueError:
        print("Erro: Entrada de escala inválida.")

def apply_rotation(axis):
    try:
        if axis == 'x':
            angle_deg = float(entry_rx.get())
            obj.pitch(math.radians(angle_deg))
        elif axis == 'y':
            angle_deg = float(entry_ry.get())
            obj.yaw(math.radians(angle_deg))
        elif axis == 'z':
            angle_deg = float(entry_rz.get())
            obj.roll(math.radians(angle_deg))
        draw()
    except ValueError:
        print("Erro: Entrada de rotação inválida.")

def reset_object():
    obj.reset()
    draw()

def apply_camera_translation():
    try:
        tx = float(entry_cam_tx.get())
        ty = float(entry_cam_ty.get())
        tz = float(entry_cam_tz.get())
        cam.translate([tx, ty, tz])
        draw()
    except ValueError:
        print("Erro: Entrada de translação da câmera inválida.")

def apply_camera_rotation(axis):
    try:
        if axis == 'x':
            angle_deg = float(entry_cam_rx.get())
            cam.orbit(d_phi=math.radians(angle_deg))
        elif axis == 'y':
            angle_deg = float(entry_cam_ry.get())
            cam.orbit(d_theta=math.radians(angle_deg))
        elif axis == 'z':
            angle_deg = float(entry_cam_rz.get())
            cam.roll(d_roll=math.radians(angle_deg))
        draw()
    except ValueError:
        print("Erro: Entrada de rotação da câmera inválida.")

def reset_camera():
    cam.reset()
    draw()


def apply_perspective_projection():
    try:
        fov = float(entry_proj_fov.get())
        near = float(entry_proj_near.get())
        far = float(entry_proj_far.get())

        if near >= far:
            print("Erro: O plano Near deve ser MENOR que o plano Far.")
            return
        if fov <= 0 or fov >= 180:
            print("Erro: O Campo de Visão (FOV) deve ser um valor entre 0 e 180.")
            return

        cam.set_perspective_params(fov, near, far)
        draw()
    except ValueError:
        print("Erro: Entrada de projeção perspectiva inválida.")

def apply_orthographic_projection():
    try:
        left = float(entry_proj_left.get())
        right = float(entry_proj_right.get())
        bottom = float(entry_proj_bottom.get())
        top = float(entry_proj_top.get())

        if left == right or bottom == top:
            print("Erro: Os valores min e max de um eixo não podem ser iguais.")
            return

        cam.set_orthographic_params(left, right, bottom, top)
        draw()
    except ValueError:
        print("Erro: Entrada de projeção paralela inválida.")


def apply_window_mapping():
    try:
        xminw = float(entry_map_xminw.get())
        xmaxw = float(entry_map_xmaxw.get())
        yminw = float(entry_map_yminw.get())
        ymaxw = float(entry_map_ymaxw.get())

        if xminw == xmaxw or yminw == ymaxw:
            print("Erro: Os valores min e max de um eixo da Window não podem ser iguais.")
            return

        cam.set_window(xminw, xmaxw, yminw, ymaxw)
        draw()
    except ValueError:
        print("Erro: Entrada de Window inválida.")

def apply_viewport_mapping():
    try:
        xminv = float(entry_map_xminv.get())
        xmaxv = float(entry_map_xmaxv.get())
        yminv = float(entry_map_yminv.get())
        ymaxv = float(entry_map_ymaxv.get())

        if xminv >= xmaxv or yminv >= ymaxv:
            print("Erro: O valor min da Viewport deve ser menor que o valor max.")
            return
        
        cam.set_viewport(xminv, xmaxv, yminv, ymaxv)
        draw()
    except ValueError:
        print("Erro: Entrada de Viewport inválida.")

def exit_program():
    print("Encerrando o programa.")
    root.destroy()


# --- FUNÇÃO DE DESENHO ---
def draw():
    canvas.delete("all")
    verts = obj.get_vertices()
    projected = [cam.project_vertex(v) for v in verts]
    for edge in obj.get_edges():
        p1 = projected[edge[0]]
        p2 = projected[edge[1]]
        canvas.create_line(p1[0], p1[1], p2[0], p2[1], fill="white")
    root.update()

# --- FUNÇÃO PARA TROCAR DE MENU (FRAME) ---
def show_frame(frame_to_show):
    frame_to_show.tkraise()

# --- CONFIGURAÇÃO INICIAL ---
WIDTH, HEIGHT = 800, 600
obj = Object3D()
cam = Camera(width=WIDTH, height=HEIGHT, target=obj.get_position())

# --- CRIAÇÃO DA JANELA PRINCIPAL (ROOT) ---
root = tk.Tk()
root.title("Visualizador 3D Interativo")

# --- LAYOUT DA JANELA: Canvas à esquerda, Controles à direita ---
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

controls_container = tk.Frame(root, bd=2, relief=tk.SUNKEN)
controls_container.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)

# --- CRIAÇÃO DOS FRAMES (MENUS) ---
main_menu_frame = tk.Frame(controls_container)
object_menu_frame = tk.Frame(controls_container)
camera_menu_frame = tk.Frame(controls_container)
projection_menu_frame = tk.Frame(controls_container)
mapping_menu_frame = tk.Frame(controls_container)

for frame in (main_menu_frame, object_menu_frame, camera_menu_frame, projection_menu_frame, mapping_menu_frame):
    frame.grid(row=0, column=0, sticky='nsew')



# --- POPULANDO O FRAME DO MENU PRINCIPAL ---
ttk.Label(main_menu_frame, text="MENU PRINCIPAL", font=("Helvetica", 12, "bold")).pack(pady=10)

# Botões de navegação
ttk.Button(main_menu_frame, text="1. Manipular Objeto", command=lambda: show_frame(object_menu_frame)).pack(fill=tk.X, padx=5, pady=2)
ttk.Button(main_menu_frame, text="2. Manipular Câmera", command=lambda: show_frame(camera_menu_frame)).pack(fill=tk.X, padx=5, pady=2)
ttk.Button(main_menu_frame, text="3. Modificar Projeção", command=lambda: show_frame(projection_menu_frame)).pack(fill=tk.X, padx=5, pady=2)
ttk.Button(main_menu_frame, text="4. Modificar Mapeamento", command=lambda: show_frame(mapping_menu_frame)).pack(fill=tk.X, padx=5, pady=2)

# Separador e botão de sair
ttk.Separator(main_menu_frame, orient='horizontal').pack(fill=tk.X, padx=5, pady=20)
ttk.Button(main_menu_frame, text="Sair do Programa", command=exit_program).pack(fill=tk.X, padx=5, pady=2)

# Rodapé com créditos
ttk.Label(main_menu_frame, text="By: Abrahão Francis e Marcos Rocha\n2025", font=("Helvetica", 8)).pack(side=tk.BOTTOM, pady=5)


# --- POPULANDO O FRAME DE MANIPULAÇÃO DO OBJETO ---
ttk.Label(object_menu_frame, text="Manipular Objeto", font=("Helvetica", 12, "bold")).grid(row=0, column=0, columnspan=4, pady=10)

# Translação
ttk.Label(object_menu_frame, text="Translação (X, Y, Z):").grid(row=1, column=0, columnspan=4, sticky='w', padx=5)
entry_tx = ttk.Entry(object_menu_frame, width=5); entry_tx.grid(row=2, column=0, padx=5)
entry_ty = ttk.Entry(object_menu_frame, width=5); entry_ty.grid(row=2, column=1, padx=5)
entry_tz = ttk.Entry(object_menu_frame, width=5); entry_tz.grid(row=2, column=2, padx=5)
ttk.Button(object_menu_frame, text="Aplicar", command=apply_translation).grid(row=2, column=3, padx=5)

# Escala
ttk.Label(object_menu_frame, text="Escala (X, Y, Z):").grid(row=3, column=0, columnspan=4, sticky='w', padx=5, pady=(10, 0))
entry_sx = ttk.Entry(object_menu_frame, width=5); entry_sx.grid(row=4, column=0, padx=5)
entry_sy = ttk.Entry(object_menu_frame, width=5); entry_sy.grid(row=4, column=1, padx=5)
entry_sz = ttk.Entry(object_menu_frame, width=5); entry_sz.grid(row=4, column=2, padx=5)
ttk.Button(object_menu_frame, text="Aplicar", command=apply_scale).grid(row=4, column=3, padx=5)

# Rotações
ttk.Label(object_menu_frame, text="Rotação X (graus):").grid(row=5, column=0, columnspan=2, sticky='w', padx=5, pady=(10, 0))
entry_rx = ttk.Entry(object_menu_frame, width=8); entry_rx.grid(row=5, column=2, padx=5)
ttk.Button(object_menu_frame, text="Aplicar", command=lambda: apply_rotation('x')).grid(row=5, column=3, padx=5)

ttk.Label(object_menu_frame, text="Rotação Y (graus):").grid(row=6, column=0, columnspan=2, sticky='w', padx=5)
entry_ry = ttk.Entry(object_menu_frame, width=8); entry_ry.grid(row=6, column=2, padx=5)
ttk.Button(object_menu_frame, text="Aplicar", command=lambda: apply_rotation('y')).grid(row=6, column=3, padx=5)

ttk.Label(object_menu_frame, text="Rotação Z (graus):").grid(row=7, column=0, columnspan=2, sticky='w', padx=5)
entry_rz = ttk.Entry(object_menu_frame, width=8); entry_rz.grid(row=7, column=2, padx=5)
ttk.Button(object_menu_frame, text="Aplicar", command=lambda: apply_rotation('z')).grid(row=7, column=3, padx=5)

# Ações Finais
ttk.Separator(object_menu_frame, orient='horizontal').grid(row=8, column=0, columnspan=4, sticky='ew', pady=15)
ttk.Button(object_menu_frame, text="Resetar Objeto", command=reset_object).grid(row=9, column=0, columnspan=4, sticky='ew', padx=5)
ttk.Button(object_menu_frame, text="< Voltar ao Menu Principal", command=lambda: show_frame(main_menu_frame)).grid(row=10, column=0, columnspan=4, sticky='ew', padx=5, pady=(5, 0))



# --- POPULANDO O FRAME DE MANIPULAÇÃO DA CÂMERA ---
ttk.Label(camera_menu_frame, text="Manipular Câmera", font=("Helvetica", 12, "bold")).grid(row=0, column=0, columnspan=4, pady=10)

# Translação da Câmera
ttk.Label(camera_menu_frame, text="Translação (X, Y, Z):").grid(row=1, column=0, columnspan=4, sticky='w', padx=5)
entry_cam_tx = ttk.Entry(camera_menu_frame, width=5); entry_cam_tx.grid(row=2, column=0, padx=5)
entry_cam_ty = ttk.Entry(camera_menu_frame, width=5); entry_cam_ty.grid(row=2, column=1, padx=5)
entry_cam_tz = ttk.Entry(camera_menu_frame, width=5); entry_cam_tz.grid(row=2, column=2, padx=5)
ttk.Button(camera_menu_frame, text="Aplicar", command=apply_camera_translation).grid(row=2, column=3, padx=5)

# Rotações da Câmera
ttk.Label(camera_menu_frame, text="Rotação X (graus):").grid(row=3, column=0, columnspan=2, sticky='w', padx=5, pady=(10, 0))
entry_cam_rx = ttk.Entry(camera_menu_frame, width=8); entry_cam_rx.grid(row=3, column=2, padx=5)
ttk.Button(camera_menu_frame, text="Aplicar", command=lambda: apply_camera_rotation('x')).grid(row=3, column=3, padx=5)

ttk.Label(camera_menu_frame, text="Rotação Y (graus):").grid(row=4, column=0, columnspan=2, sticky='w', padx=5)
entry_cam_ry = ttk.Entry(camera_menu_frame, width=8); entry_cam_ry.grid(row=4, column=2, padx=5)
ttk.Button(camera_menu_frame, text="Aplicar", command=lambda: apply_camera_rotation('y')).grid(row=4, column=3, padx=5)

ttk.Label(camera_menu_frame, text="Rotação Z (graus):").grid(row=5, column=0, columnspan=2, sticky='w', padx=5)
entry_cam_rz = ttk.Entry(camera_menu_frame, width=8); entry_cam_rz.grid(row=5, column=2, padx=5)
ttk.Button(camera_menu_frame, text="Aplicar", command=lambda: apply_camera_rotation('z')).grid(row=5, column=3, padx=5)

# Ações Finais
ttk.Separator(camera_menu_frame, orient='horizontal').grid(row=6, column=0, columnspan=4, sticky='ew', pady=15)
ttk.Button(camera_menu_frame, text="Resetar Câmera", command=reset_camera).grid(row=7, column=0, columnspan=4, sticky='ew', padx=5)
ttk.Button(camera_menu_frame, text="< Voltar ao Menu Principal", command=lambda: show_frame(main_menu_frame)).grid(row=8, column=0, columnspan=4, sticky='ew', padx=5, pady=(5, 0))


# --- POPULANDO O FRAME DE MODIFICAÇÃO DE PROJEÇÃO ---
ttk.Label(projection_menu_frame, text="Modificar Projeção", font=("Helvetica", 12, "bold")).grid(row=0, column=0, columnspan=4, pady=10)

# Projeção Perspectiva
ttk.Label(projection_menu_frame, text="Projeção Perspectiva", font=("Helvetica", 10, "bold")).grid(row=1, column=0, columnspan=4, sticky='w', padx=5, pady=(10,0))
ttk.Label(projection_menu_frame, text="FOV (graus):").grid(row=2, column=0, sticky='w', padx=5)
entry_proj_fov = ttk.Entry(projection_menu_frame, width=8); entry_proj_fov.grid(row=2, column=1)
ttk.Label(projection_menu_frame, text="Near:").grid(row=3, column=0, sticky='w', padx=5)
entry_proj_near = ttk.Entry(projection_menu_frame, width=8); entry_proj_near.grid(row=3, column=1)
ttk.Label(projection_menu_frame, text="Far:").grid(row=4, column=0, sticky='w', padx=5)
entry_proj_far = ttk.Entry(projection_menu_frame, width=8); entry_proj_far.grid(row=4, column=1)
ttk.Button(projection_menu_frame, text="Aplicar Perspectiva", command=apply_perspective_projection).grid(row=5, column=0, columnspan=4, sticky='ew', padx=5, pady=5)

# --- AVISO DA PROJEÇÃO PERSPECTIVA ADICIONADO ---
hint_label_perspective = ttk.Label(projection_menu_frame,
                                   text="Dica: 'Near' deve ser menor que 'Far'. 'FOV' deve estar entre 0 e 180.",
                                   font=("Helvetica", 8, "italic"),
                                   wraplength=180,
                                   justify='center')
hint_label_perspective.grid(row=6, column=0, columnspan=4, padx=5, pady=5)


# Separador 
ttk.Separator(projection_menu_frame, orient='horizontal').grid(row=7, column=0, columnspan=4, sticky='ew', pady=15)


# Projeção Paralela (Ortográfica) 
ttk.Label(projection_menu_frame, text="Projeção Paralela", font=("Helvetica", 10, "bold")).grid(row=8, column=0, columnspan=4, sticky='w', padx=5)
ttk.Label(projection_menu_frame, text="Left:").grid(row=9, column=0, sticky='w', padx=5)
entry_proj_left = ttk.Entry(projection_menu_frame, width=8); entry_proj_left.grid(row=9, column=1)
ttk.Label(projection_menu_frame, text="Right:").grid(row=10, column=0, sticky='w', padx=5)
entry_proj_right = ttk.Entry(projection_menu_frame, width=8); entry_proj_right.grid(row=10, column=1)
ttk.Label(projection_menu_frame, text="Bottom:").grid(row=11, column=0, sticky='w', padx=5)
entry_proj_bottom = ttk.Entry(projection_menu_frame, width=8); entry_proj_bottom.grid(row=11, column=1)
ttk.Label(projection_menu_frame, text="Top:").grid(row=12, column=0, sticky='w', padx=5)
entry_proj_top = ttk.Entry(projection_menu_frame, width=8); entry_proj_top.grid(row=12, column=1)
ttk.Button(projection_menu_frame, text="Aplicar Paralela", command=apply_orthographic_projection).grid(row=13, column=0, columnspan=4, sticky='ew', padx=5, pady=5)


# --- AVISO DA PROJEÇÃO PARALELA ADICIONADO ---
hint_label_parallel = ttk.Label(projection_menu_frame,
                                text="Dica: min/max não podem ser iguais. Para ver o objeto, o intervalo deve ser maior que [-0.5, 0.5].",
                                font=("Helvetica", 8, "italic"),
                                wraplength=180,
                                justify='center')
hint_label_parallel.grid(row=14, column=0, columnspan=4, padx=5, pady=5)


# Ação Final 
ttk.Separator(projection_menu_frame, orient='horizontal').grid(row=15, column=0, columnspan=4, sticky='ew', pady=15)
ttk.Button(projection_menu_frame, text="< Voltar ao Menu Principal", command=lambda: show_frame(main_menu_frame)).grid(row=16, column=0, columnspan=4, sticky='ew', padx=5, pady=(5,0))



# --- POPULANDO O FRAME DE MODIFICAÇÃO DE MAPEAMENTO ---
ttk.Label(mapping_menu_frame, text="Modificar Mapeamento", font=("Helvetica", 12, "bold")).grid(row=0, column=0, columnspan=4, pady=10)

# Window
ttk.Label(mapping_menu_frame, text="Window", font=("Helvetica", 10, "bold")).grid(row=1, column=0, columnspan=4, sticky='w', padx=5, pady=(10,0))
ttk.Label(mapping_menu_frame, text="X (min, max):").grid(row=2, column=0, columnspan=2, sticky='w', padx=5)
entry_map_xminw = ttk.Entry(mapping_menu_frame, width=5); entry_map_xminw.grid(row=2, column=2)
entry_map_xmaxw = ttk.Entry(mapping_menu_frame, width=5); entry_map_xmaxw.grid(row=2, column=3)
ttk.Label(mapping_menu_frame, text="Y (min, max):").grid(row=3, column=0, columnspan=2, sticky='w', padx=5)
entry_map_yminw = ttk.Entry(mapping_menu_frame, width=5); entry_map_yminw.grid(row=3, column=2)
entry_map_ymaxw = ttk.Entry(mapping_menu_frame, width=5); entry_map_ymaxw.grid(row=3, column=3)
ttk.Button(mapping_menu_frame, text="Aplicar Window", command=apply_window_mapping).grid(row=4, column=0, columnspan=4, sticky='ew', padx=5, pady=5)

# --- AVISO DA WINDOW ---
hint_label_window = ttk.Label(mapping_menu_frame, 
                       text="Dica: Para manter o objeto visível, use um intervalo que contenha [-0.5, 0.5].",
                       font=("Helvetica", 8, "italic"),
                       wraplength=180,
                       justify='center')
hint_label_window.grid(row=5, column=0, columnspan=4, padx=5, pady=5)

# Separador
ttk.Separator(mapping_menu_frame, orient='horizontal').grid(row=6, column=0, columnspan=4, sticky='ew', pady=15)

# Viewport
ttk.Label(mapping_menu_frame, text="Viewport", font=("Helvetica", 10, "bold")).grid(row=7, column=0, columnspan=4, sticky='w', padx=5)
ttk.Label(mapping_menu_frame, text="X (min, max):").grid(row=8, column=0, columnspan=2, sticky='w', padx=5)
entry_map_xminv = ttk.Entry(mapping_menu_frame, width=5); entry_map_xminv.grid(row=8, column=2)
entry_map_xmaxv = ttk.Entry(mapping_menu_frame, width=5); entry_map_xmaxv.grid(row=8, column=3)
ttk.Label(mapping_menu_frame, text="Y (min, max):").grid(row=9, column=0, columnspan=2, sticky='w', padx=5)
entry_map_yminv = ttk.Entry(mapping_menu_frame, width=5); entry_map_yminv.grid(row=9, column=2)
entry_map_ymaxv = ttk.Entry(mapping_menu_frame, width=5); entry_map_ymaxv.grid(row=9, column=3)
ttk.Button(mapping_menu_frame, text="Aplicar Viewport", command=apply_viewport_mapping).grid(row=10, column=0, columnspan=4, sticky='ew', padx=5, pady=5)

# --- AVISO DA VIEWPORT ---
hint_label_viewport = ttk.Label(mapping_menu_frame,
                                text="Dica: A área visível da tela vai de X(0 a 800) e Y(0 a 600).",
                                font=("Helvetica", 8, "italic"),
                                wraplength=180,
                                justify='center')
hint_label_viewport.grid(row=11, column=0, columnspan=4, padx=5, pady=5)

# Ação Final
ttk.Separator(mapping_menu_frame, orient='horizontal').grid(row=12, column=0, columnspan=4, sticky='ew', pady=15)
ttk.Button(mapping_menu_frame, text="< Voltar ao Menu Principal", command=lambda: show_frame(main_menu_frame)).grid(row=13, column=0, columnspan=4, sticky='ew', padx=5, pady=(5,0))



# --- INICIALIZAÇÃO DO PROGRAMA ---
show_frame(main_menu_frame)  # Mostra o menu principal para começar
draw()  # Desenha o estado inicial do objeto
root.mainloop()  # Inicia o loop da interface gráfica