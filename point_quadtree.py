import random
import time
import matplotlib.pyplot as plt
import matplotlib.patches as patches

RECTANGULOS = []
PUNTOS = []

class Punto:
    def __init__(self, x, y, val=None):
        self.x = x
        self.y = y
        self.val = val

    def __repr__(self):
        if self.val is None: return f'({self.x}, {self.y})'
        else: return f'({self.x}, {self.y}; {self.val})'

class Rectangulo:
    def __init__(self, inicio: Punto, dimensiones: Punto):
        self.inicio = inicio
        self.dimensiones = dimensiones

    def contiene(self, punto):
        return (self.inicio.x <= punto.x < self.dimensiones.x and 
                self.inicio.y <= punto.y < self.dimensiones.y)

    def __repr__(self):
        return f'({self.inicio.x}, {self.inicio.y}, {self.dimensiones.x}, {self.dimensiones.y})'

class Quadtree:
    def __init__(self, limite: Rectangulo):
        self.limite = limite
        self.dividido = False
        self.punto_no = Punto(limite.inicio.x, limite.inicio.y)
        self.punto_se = Punto(limite.dimensiones.x, limite.dimensiones.y)

        self.val = None

        self.no = None
        self.ne = None
        self.so = None
        self.se = None

    def subdividir(self, punto: Punto):
        self.val = punto

        no_limite = Rectangulo(self.limite.inicio, punto)
        ne_limite = Rectangulo(Punto(punto.x, self.limite.inicio.y), Punto(self.limite.dimensiones.x, punto.y))
        so_limite = Rectangulo(Punto(self.limite.inicio.x, punto.y), Punto(punto.x, self.limite.dimensiones.y))
        se_limite = Rectangulo(punto, self.limite.dimensiones)

        self.no = Quadtree(no_limite)
        self.ne = Quadtree(ne_limite)
        self.so = Quadtree(so_limite)
        self.se = Quadtree(se_limite)

        self.dividido = True

    def insertar(self, punto):
        if not self.limite.contiene(punto):
            return False

        if not self.dividido:
            self.subdividir(punto)
            return True
        else:
            return self._insertar_en_hijo(punto)

    def _insertar_en_hijo(self, punto):
        if self.no.insertar(punto):
            return True
        if self.ne.insertar(punto):
            return True
        if self.so.insertar(punto):
            return True
        if self.se.insertar(punto):
            return True
        return False

    def imprimir_sub(self):
        if self.dividido:

            self.no.imprimir_sub()
            self.ne.imprimir_sub()
            self.so.imprimir_sub()
            self.se.imprimir_sub()
        else:
            RECTANGULOS.append(self.limite)

        if self.val: PUNTOS.append(self.val)

def graficar_quadtree(rectangulos, puntos):
    fig, ax = plt.subplots()

    for rect in rectangulos:
        rect_patch = patches.Rectangle((rect.inicio.x, rect.inicio.y), rect.dimensiones.x - rect.inicio.x, rect.dimensiones.y - rect.inicio.y,
                                       linewidth=0.65, edgecolor='r', facecolor='none')
        ax.add_patch(rect_patch)

    x_vals = [punto.x for punto in puntos]
    y_vals = [punto.y for punto in puntos]
    ax.scatter(x_vals, y_vals, color='b')


    plt.xlim(0, 1000)
    plt.ylim(0, 1000)
    ax.set_aspect('equal', 'box')
    plt.gca().invert_yaxis()
    plt.gca().xaxis.set_ticks_position('top')
    plt.gca().xaxis.set_label_position('top') 

    plt.title('Visualización del Point Quadtree')
    plt.show()

if __name__ == '__main__':
    inicio = Punto(0, 0)
    dimensiones = Punto(1000, 1000)

    raiz = Rectangulo(inicio, dimensiones)
    pquadtree = Quadtree(raiz)

    random.seed(time.time())
    for _ in range(50):
        p = Punto(random.randint(0, 1000), random.randint(0, 1000), random.randint(1, 50))
        pquadtree.insertar(p)

    pquadtree.imprimir_sub()

    graficar_quadtree(RECTANGULOS, PUNTOS)

    