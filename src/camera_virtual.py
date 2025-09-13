#lista de listas para guardar dados do objeto (piramide)

#Numpy -> biblioteca que facilita operações matemáticas com matrizes.


import numpy as np

#definindo vértices da pirâmide 
# (lembrando que o "1" é a Coordenada Homogênea, que permite fazer todas as transformações 
# em uma matriz 4x4. Sem ele, a translação teria que ser tratada de forma diferente)
vertices = np.array([
    [-0.5, -0.25, -0.5, 1],  #P0
    [0.5, -0.25, -0.5, 1],   #P1
    [-0.5, -0.25, 0.5, 1],   #P2
    [0.5, -0.25, 0.5, 1],    #P3
    [0.0, 0.25, 0.0, 1]      #P4 = topo da pirâmide
])

#Lista para determinar arestas (linhas) ligando os pontos. Cada item será um par, 
#representando os indíces de dois vértices que serão ligados por uma linha.
arestas = [[0, 1], [1, 3], [3, 2], [2, 0], #arestas da base
           [0, 4], [1, 4], [2, 4], [3, 4]  #arestas do topo
            ] 