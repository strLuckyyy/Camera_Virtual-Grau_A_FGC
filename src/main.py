# main.py (ou reescreva seu test.py)

import numpy as np
import tkinter as tk
from object import Object3D
from camera import Camera, ProjectionType
import math

# --- Inicialização dos objetos e da janela gráfica ---
# (Essa parte do seu código test.py pode ser mantida)
WIDTH, HEIGHT = 800, 600
obj = Object3D()
cam = Camera(width=WIDTH, height=HEIGHT, target=obj.get_position())

# Janela gráfica (vamos controlá-la manualmente)
root = tk.Tk()
root.title("Visualizador 3D")
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
canvas.pack()

# --- Função de desenho (a sua já está perfeita) ---
def draw():
    canvas.delete("all")
    verts = obj.get_vertices()
    projected = [cam.project_vertex(v) for v in verts]
    for edge in obj.get_edges():
        p1 = projected[edge[0]]
        p2 = projected[edge[1]]
        canvas.create_line(p1[0], p1[1], p2[0], p2[1], fill="white")
    root.update() # Força a atualização da janela


def menu_manipular_objeto():
    while True:
        print("\n--- Manipular Objeto ---")
        print("1. Translação")
        print("2. Escala")
        print("3. Rotação em X")
        print("4. Rotação em Y")
        print("5. Rotação em Z")
        print("6. Resetar Objeto")
        print("0. Voltar ao menu principal")

        sub_choice = input("Escolha uma opção: ")

        if sub_choice == '1':
            try:
                tx = float(input("Digite o valor da translação em X: "))
                ty = float(input("Digite o valor da translação em Y: "))
                tz = float(input("Digite o valor da translação em Z: "))
                obj.translate([tx, ty, tz])
                draw() # <--- CORRETO: Chamar draw() após a ação
            except ValueError:
                print("Entrada inválida. Por favor, insira números.")
        
        elif sub_choice == '2':
            try:
                sx = float(input("Digite o fator de escala em X (ex: 1.5 para aumentar, 0.5 para diminuir): "))
                sy = float(input("Digite o fator de escala em Y: "))
                sz = float(input("Digite o fator de escala em Z: "))
                obj.scale([sx, sy, sz])
                draw() # <--- CORRETO: Chamar draw() após a ação
            except ValueError:
                print("Entrada inválida. Por favor, insira números.")

        elif sub_choice == '3': # Rotação em X
            try:
                angle_deg = float(input("Digite o ângulo de rotação em graus para o eixo X: "))
                angle_rad = math.radians(angle_deg)
                obj.pitch(angle_rad)
                draw() # <--- CORRETO: Chamar draw() após a ação
            except ValueError:
                print("Entrada inválida. Por favor, insira um número.")

        elif sub_choice == '4': # Rotação em Y
            try:
                angle_deg = float(input("Digite o ângulo de rotação em graus para o eixo Y: "))
                angle_rad = math.radians(angle_deg)
                obj.yaw(angle_rad)
                draw() # <--- CORRETO: Chamar draw() após a ação
            except ValueError:
                print("Entrada inválida. Por favor, insira um número.")

        elif sub_choice == '5': # Rotação em Z
            try:
                angle_deg = float(input("Digite o ângulo de rotação em graus para o eixo Z:  "))
                angle_rad = math.radians(angle_deg)
                obj.roll(angle_rad)
                draw() # <--- CORRETO: Chamar draw() após a ação
            except ValueError:
                print("Entrada inválida. Por favor, insira um número.")


        elif sub_choice == '6':
            print("Objeto resetado para o estado original.")
            obj.reset()
            draw()


        elif sub_choice == '0':
            break # Simplesmente sai do loop
        
        else:
            # Este else agora só pega opções que não são 0, 1, 2, 3, 4, 5
            print("Opção inválida.")


def menu_manipular_camera():
    while True:
        print("\n--- Manipular Câmera ---")
        print("1. Translação")
        print("2. Rotação em X (Pitch)")
        print("3. Rotação em Y (Yaw)")
        print("4. Rotação em Z (Roll)")
        print("5. Resetar Posição da Câmera")
        print("0. Voltar ao menu principal")

        sub_choice = input("Escolha uma opção: ")


        if sub_choice == '1':
            try:
                tx = float(input("Digite o valor da translação em X: "))
                ty = float(input("Digite o valor da translação em Y: "))
                tz = float(input("Digite o valor da translação em Z: "))
                cam.translate([tx, ty, tz])
                draw() # <--- CORRETO: Chamar draw() após a ação
            except ValueError:
                print("Entrada inválida. Por favor, insira números.")


        elif sub_choice == '2': # Rotação em X (Pitch)
            try:
                angle_deg = float(input("Digite o ângulo em graus para orbitar para cima/baixo: "))
                angle_rad = math.radians(angle_deg)
                # Usamos d_phi para orbitar em torno do eixo X da câmera
                cam.orbit(d_phi=angle_rad)
                draw()
            except ValueError:
                print("Entrada inválida. Por favor, insira um número.")


        elif sub_choice == '3': # Rotação em Y (Yaw)
            try:
                angle_deg = float(input("Digite o ângulo em graus para orbitar para esquerda/direita: "))
                angle_rad = math.radians(angle_deg)
                # Usamos d_theta para orbitar em torno do eixo Y do mundo
                cam.orbit(d_theta=angle_rad)
                draw()
            except ValueError:
                print("Entrada inválida. Por favor, insira um número.")


        elif sub_choice == '4': # Rotação em Z (Roll)
            try:
                angle_deg = float(input("Digite o ângulo em graus para o 'roll' da câmera: "))
                angle_rad = math.radians(angle_deg)
                cam.roll(d_roll=angle_rad)
                draw()
            except ValueError:
                print("Entrada inválida. Por favor, insira um número.")


        elif sub_choice == '5': # Resetar Câmera
            print("Posição da câmera resetada.")
            cam.reset()
            draw()


        elif sub_choice == '0':
            break # Simplesmente sai do loop
        else:
            print("Opção inválida.")


def menu_modificar_projecao():
    while True:
        # Mostra o estado atual da projeção
        proj_atual = "Perspectiva" if cam.projection == ProjectionType.PERSPECTIVE else "Paralela"
        print(f"\n--- Modificar Projeção (Atual: {proj_atual}) ---")
        print("1. Definir Projeção Perspectiva")
        print("2. Definir Projeção Paralela")
        print("0. Voltar ao menu principal")

        sub_choice = input("Escolha uma opção: ")


        if sub_choice == '1':
            try:
                fov = float(input("Digite o Campo de Visão (FOV) em graus (ex: 90): "))
                near = float(input("Digite a distância do plano Near (ex: 0.1): "))
                far = float(input("Digite a distância do plano Far (ex: 1000): "))

                # --- VALIDAÇÃO AQUI ---
                if near >= far:
                    print("\n!!! ERRO: O plano Near deve ser MENOR que o plano Far. Tente novamente. !!!")
                    continue # Volta para o início do loop

                # Validação extra (boa prática): FOV deve ser um ângulo válido
                if fov <= 0 or fov >= 180:
                    print("\n!!! ERRO: O Campo de Visão (FOV) deve ser um valor positivo e menor que 180. !!!")
                    continue # Volta para o início do loop

                cam.set_perspective_params(fov, near, far)
                draw()
                
            except ValueError:
                print("Entrada inválida. Por favor, insira números.")
        

        elif sub_choice == '2':
            try:
                left = float(input("Digite o limite esquerdo (left) (ex: -1): "))
                right = float(input("Digite o limite direito (right) (ex: 1): "))
                bottom = float(input("Digite o limite inferior (bottom) (ex: -1): "))
                top = float(input("Digite o limite superior (top) (ex: 1): "))

                # --- VALIDAÇÃO AQUI ---
                if left == right or bottom == top:
                    print("\n!!! ERRO: Os limites esquerdo/direito e inferior/superior não podem ser iguais. Tente novamente. !!!")
                    continue # Pula para a próxima iteração do loop, pedindo a opção novamente.
                
                cam.set_orthographic_params(left, right, bottom, top)
                draw()
                
            except ValueError:
                print("Entrada inválida. Por favor, insira números.")
        

        elif sub_choice == '0':
            break
        
        else:
            print("Opção inválida.")


def menu_modificar_mapeamento():
    while True:
        # Mostra os valores atuais para o usuário
        print("\n--- Modificar Mapeamento ---")
        print(f"  Window Atual: x({cam.xminw}, {cam.xmaxw}), y({cam.yminw}, {cam.ymaxw})")
        print(f"  Viewport Atual: x({cam.xminv}, {cam.xmaxv}), y({cam.yminv}, {cam.ymaxv})")
        print("\n1. Modificar Window")
        print("2. Modificar Viewport")
        print("0. Voltar ao menu principal")

        sub_choice = input("Escolha uma opção: ")

        if sub_choice == '1': # Modificar Window
            try:
                xminw = float(input("Digite o novo xmin da Window: "))
                xmaxw = float(input("Digite o novo xmax da Window: "))
                yminw = float(input("Digite o novo ymin da Window: "))
                ymaxw = float(input("Digite o novo ymax da Window: "))

                # Validação para evitar divisão por zero
                if xminw == xmaxw or yminw == ymaxw:
                    print("\n!!! ERRO: Os valores min e max de um eixo não podem ser iguais. !!!")
                    continue

                cam.set_window(xminw, xmaxw, yminw, ymaxw)
                draw()
            except ValueError:
                print("Entrada inválida. Por favor, insira números.")
        
        elif sub_choice == '2': # Modificar Viewport
            try:
                xminv = float(input("Digite o novo xmin da Viewport: "))
                xmaxv = float(input("Digite o novo xmax da Viewport: "))
                yminv = float(input("Digite o novo ymin da Viewport: "))
                ymaxv = float(input("Digite o novo ymax da Viewport: "))

                # Validação (min não pode ser maior ou igual a max)
                if xminv >= xmaxv or yminv >= ymaxv:
                    print("\n!!! ERRO: O valor min deve ser menor que o valor max. !!!")
                    continue
                
                cam.set_viewport(xminv, xmaxv, yminv, ymaxv)
                draw()
            except ValueError:
                print("Entrada inválida. Por favor, insira números.")
        
        elif sub_choice == '0':
            break
        
        else:
            print("Opção inválida.")





# --- Loop do Menu Principal ---
def main_menu():
    while True:
        print("\n===== MENU PRINCIPAL =====")
        print("1. Manipular o objeto")
        print("2. Manipular a câmera")
        print("3. Modificar projeção")
        print("4. Modificar mapeamento")
        print("0. Sair")
        
        choice = input("Escolha uma opção: ")

        if choice == '1':
            # Chamar a função do submenu do objeto
            menu_manipular_objeto()

        elif choice == '2':
            # Chamar a função do submenu da câmera
            menu_manipular_camera()

        elif choice == '3':
            # Chamar a função para mudar projeção da câmera
            menu_modificar_projecao()

        
        elif choice == '4':
            # Chamar a função para mudar mapeamento da câmera (área de visualização)
            menu_modificar_mapeamento()


        elif choice == '0':
            break
        else:
            print("Opção inválida!")
            
    root.destroy() # Fecha a janela ao sair do loop

# --- Comece o programa ---
if __name__ == "__main__":
    draw() # Desenha o estado inicial
    main_menu()



