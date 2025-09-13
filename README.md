# Trabalho - Câmera Virtual - Pipeline de Visualização 3D

## 🎯 Objetivo
Desenvolver uma aplicação que implemente um **pipeline de visualização 3D**, com as seguintes etapas:

---

## 📌 Etapas do Trabalho

### 1. Modelagem do Objeto 3D
- Modele um objeto 3D (**não pode ser um cubo**).
- A origem `(0,0,0)` deve estar no **centro do objeto**.
- Os limites de `x`, `y`, `z` devem variar de **-1 a 1**.  
Exemplo: uma pirâmide ou um prisma.

---

### 2. Menu de Opções
Ao iniciar, deve ser exibido um menu com as opções:

1. Manipular o objeto  
2. Manipular a câmera  
3. Modificar projeção  
4. Modificar mapeamento  
5. Visualizar objeto  

---

### 3. Manipulação do Objeto
Submenu com as opções:

- **Translação**  
- **Escala**  
- **Rotação em X**  
- **Rotação em Y**  
- **Rotação em Z**  

👉 Cada transformação deve ser aplicada em uma **matriz de transformação do modelo**, iniciada como **matriz identidade**.

---

### 4. Manipulação da Câmera
Submenu com as opções:

- **Translação**  
- **Rotação em X**  
- **Rotação em Y**  
- **Rotação em Z**  

👉 As transformações devem ser acumuladas em uma **matriz de visualização**, com **valores invertidos** (exemplo: se o ângulo for `45°`, a matriz usa `-45°`).  
A matriz começa como **identidade**.

---

### 5. Modificar Projeção
Opções:

- **Projeção perspectiva**  
- **Projeção paralela**  

👉 O usuário insere os parâmetros, e a aplicação monta a matriz de projeção.  
Por padrão, inicia com **projeção perspectiva**.

---

### 6. Modificar Mapeamento
Submenu com as opções:

- **Window**  
- **Viewport**  

Valores iniciais:

- Window: `xminw = -1`, `xmaxw = 1`, `yminw = -1`, `ymaxw = 1`  
- Viewport: `xminv = 0`, `xmaxv = 500`, `yminv = 0`, `ymaxv = 500`

---

### 7. Visualização do Objeto
O sistema deve exibir os vértices do objeto final após aplicar o **pipeline 3D**:

1. Aplicar **matriz de transformação do modelo** nos vértices originais.  
2. Aplicar **matriz de visualização**.  
3. Aplicar **matriz de projeção** (convertendo 3D em 2D).  
4. Aplicar **mapeamento** com os parâmetros de window e viewport.  

👉 Os vértices finais (2D) devem ser exibidos em tela usando **biblioteca gráfica 2D**  
(exemplo: `matplotlib` em Python).  

⚠️ O objeto deve ser exibido **desde o começo da aplicação**, e atualizado sempre que houver modificações.

---

## 🚫 Restrições
- **Não usar** bibliotecas de renderização 3D (OpenGL, Unity, etc.).  
- Somente bibliotecas **matemáticas** e **gráficas 2D** são permitidas (ex.: `numpy`, `matplotlib`).  
