import cv2
import numpy as np
import matplotlib.pyplot as plt

class Rectangulo:
    def __init__(self, x, y, ancho, alto):
        self.x = x
        self.y = y
        self.ancho = ancho
        self.alto = alto
        self.puntos = []

    def contiene(self, punto):
        return self.x <= punto[0] < self.x + self.ancho and self.y <= punto[1] < self.y + self.alto

class Quadtree:
    def __init__(self, limite, capacidad):
        self.limite = limite
        self.capacidad = capacidad
        self.dividido = False
        self.noreste = None
        self.sureste = None
        self.noroeste = None
        self.suroeste = None

    def subdividir(self):
        x, y, ancho, alto = self.limite.x, self.limite.y, self.limite.ancho, self.limite.alto
        noreste = Rectangulo(x + ancho / 2, y, ancho / 2, alto / 2)
        self.noreste = Quadtree(noreste, self.capacidad)
        sureste = Rectangulo(x + ancho / 2, y + alto / 2, ancho / 2, alto / 2)
        self.sureste = Quadtree(sureste, self.capacidad)
        suroeste = Rectangulo(x, y + alto / 2, ancho / 2, alto / 2)
        self.suroeste = Quadtree(suroeste, self.capacidad)
        noroeste = Rectangulo(x, y, ancho / 2, alto / 2)
        self.noroeste = Quadtree(noroeste, self.capacidad)
        self.dividido = True

    def insertar(self, punto):
        if not self.limite.contiene(punto):
            return False
        if len(self.limite.puntos) < self.capacidad:
            self.limite.puntos.append(punto)
            return True
        else:
            if not self.dividido:
                self.subdividir()
            if self.noreste.insertar(punto): return True
            if self.sureste.insertar(punto): return True
            if self.suroeste.insertar(punto): return True
            if self.noroeste.insertar(punto): return True

    def contar_celulas(self):
        if not self.dividido:
            return len(self.limite.puntos)
        else:
            return (self.noreste.contar_celulas() +
                    self.sureste.contar_celulas() +
                    self.suroeste.contar_celulas() +
                    self.noroeste.contar_celulas())

    def dibujar(self, ax):
        ax.add_patch(plt.Rectangle((self.limite.x, self.limite.y),
                                   self.limite.ancho, self.limite.alto,
                                   fill=False, edgecolor='r', linewidth=1))
        if self.dividido:
            self.noreste.dibujar(ax)
            self.sureste.dibujar(ax)
            self.suroeste.dibujar(ax)
            self.noroeste.dibujar(ax)

def cargar_imagen(ruta_imagen):
    imagen = cv2.imread(ruta_imagen, cv2.IMREAD_GRAYSCALE)
    return imagen

def eliminar_lineas(imagen):
    lineas = cv2.HoughLinesP(imagen, 1, np.pi / 180, threshold=100, minLineLength=100, maxLineGap=10)
    if lineas is not None:
        for linea in lineas:
            x1, y1, x2, y2 = linea[0]
            if abs(x1 - x2) > 50:
                cv2.line(imagen, (x1, y1), (x2, y2), (0, 0, 0), 3)
            if abs(y1 - y2) > 50:
                cv2.line(imagen, (x1, y1), (x2, y2), (0, 0, 0), 3)
    return imagen

def aplicar_mascara_circular(imagen):
    filas, columnas = imagen.shape
    centro = (columnas // 2, filas // 2)
    radio = min(centro[0], centro[1])
    mascara = np.zeros_like(imagen)
    cv2.circle(mascara, centro, radio, 255, thickness=-1)
    imagen_sin_bordes = cv2.bitwise_and(imagen, mascara)
    return imagen_sin_bordes

def preprocesar_imagen(imagen):
    imagen_suavizada = cv2.GaussianBlur(imagen, (3, 3), 0)
    imagen_bordes = cv2.Canny(imagen_suavizada, 30, 100)
    imagen_sin_lineas = eliminar_lineas(imagen_bordes)
    imagen_sin_bordes = aplicar_mascara_circular(imagen_sin_lineas)
    _, imagen_binaria = cv2.threshold(imagen_sin_bordes, 50, 255, cv2.THRESH_BINARY)
    return imagen_binaria

def detectar_contornos(imagen_binaria):
    contornos, _ = cv2.findContours(imagen_binaria, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contornos

def extraer_centros(contornos):
    centros = []
    for contorno in contornos:
        M = cv2.moments(contorno)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            centros.append((cX, cY))
    return centros

def mostrar_resultados(imagen_original, contornos, quadtree):
    imagen_color = cv2.cvtColor(imagen_original, cv2.COLOR_GRAY2BGR)
    

    cv2.drawContours(imagen_color, contornos, -1, (0, 255, 0), 2)
    
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.imshow(cv2.cvtColor(imagen_color, cv2.COLOR_BGR2RGB))
    quadtree.dibujar(ax)
    plt.title("Colonias detectadas")
    plt.show()

if __name__ == '__main__':
    ruta_imagen = 'Images/unnamed3.png'
    imagen = cargar_imagen(ruta_imagen)
    imagen_binaria = preprocesar_imagen(imagen)
    contornos = detectar_contornos(imagen_binaria)
    centros_celulas = extraer_centros(contornos)
    limite_inicial = Rectangulo(0, 0, imagen.shape[1], imagen.shape[0])
    quadtree = Quadtree(limite_inicial, 4)
    for centro in centros_celulas:
        quadtree.insertar(centro)
    mostrar_resultados(imagen, contornos, quadtree)
    total_celulas = quadtree.contar_celulas()
    print(f"Número total de colonias detectadas: {total_celulas}")
