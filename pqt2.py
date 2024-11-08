import random
import time
import matplotlib.pyplot as plt
import matplotlib.patches as patches

RECTANGULOS = []
PUNTOS = []

class Punto:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __repr__(self):
        return f'{{"x": {self.x}, "y": {self.y}}}'

class Rectangulo:
    def __init__(self, x, y, ancho, alto):
        self.x = x
        self.y = y
        self.ancho = ancho
        self.alto = alto

    def contiene(self, punto):
        return (self.x <= punto.x < self.x + self.ancho and 
                self.y <= punto.y < self.y + self.alto)

    def __repr__(self):
        return f'({self.x}, {self.y}, {self.ancho}, {self.alto})'

class Quadtree:
    def __init__(self, limite, capacidad=1):
        self.limite = limite
        self.capacidad = capacidad
        self.dividido = False
        self.punto = None
        self.noreste = None
        self.sureste = None
        self.noroeste = None
        self.suroeste = None

    def subdividir(self):
        px, py = self.punto.x, self.punto.y
        mitad_ancho = (self.limite.x + self.limite.ancho - px) / 2
        mitad_alto = (self.limite.y + self.limite.alto - py) / 2

        self.noreste = Quadtree(Rectangulo(px, py, mitad_ancho, mitad_alto))
        self.sureste = Quadtree(Rectangulo(px, py + mitad_alto, mitad_ancho, mitad_alto))
        self.noroeste = Quadtree(Rectangulo(px - mitad_ancho, py, mitad_ancho, mitad_alto))
        self.suroeste = Quadtree(Rectangulo(px - mitad_ancho, py + mitad_alto, mitad_ancho, mitad_alto))
        self.dividido = True

    def insert(self, punto):
        if not self.limite.contiene(punto):
            return False

        if self.punto is None and not self.dividido:
            self.punto = punto
            return True
        else:
            if not self.dividido:
                self.subdividir()
                if self.punto:
                    self._insertar_en_hijo(self.punto)
                    self.punto = None

            return self._insertar_en_hijo(punto)

    def _insertar_en_hijo(self, punto):
        if self.noreste.limite.contiene(punto):
            return self.noreste.insert(punto)
        elif self.sureste.limite.contiene(punto):
            return self.sureste.insert(punto)
        elif self.noroeste.limite.contiene(punto):
            return self.noroeste.insert(punto)
        elif self.suroeste.limite.contiene(punto):
            return self.suroeste.insert(punto)
        return False

    def imprimir_sub(self):
        global RECTANGULOS, PUNTOS
        if not self.dividido and self.punto:
            RECTANGULOS.append(self.limite)
            PUNTOS.append(self.punto)
        elif self.dividido:
            if self.noreste:
                self.noreste.imprimir_sub()
            if self.sureste:
                self.sureste.imprimir_sub()
            if self.noroeste:
                self.noroeste.imprimir_sub()
            if self.suroeste:
                self.suroeste.imprimir_sub()

def graficar_quadtree(rectangulos, puntos):
    fig, ax = plt.subplots()

    for rect in rectangulos:
        rect_patch = patches.Rectangle((rect.x, rect.y), rect.ancho, rect.alto,
                                       linewidth=1, edgecolor='r', facecolor='none')
        ax.add_patch(rect_patch)

    x_vals = [punto.x for punto in puntos]
    y_vals = [punto.y for punto in puntos]
    ax.scatter(x_vals, y_vals, color='b')

    plt.xlim(0, 200)
    plt.ylim(0, 200)
    ax.set_aspect('equal', 'box')
    plt.title('Visualización del Point Quadtree')
    plt.show()

if __name__ == '__main__':
    raiz = Rectangulo(0, 0, 200, 200)
    quadtree = Quadtree(raiz)

    random.seed(time.time())
    for _ in range(20):
        p = Punto(random.randint(0, 200), random.randint(0, 200))
        quadtree.insert(p)

    quadtree.imprimir_sub()
    graficar_quadtree(RECTANGULOS, PUNTOS)
