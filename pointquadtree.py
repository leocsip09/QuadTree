import pygame
import math

class Punto:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if isinstance(other, Punto):
            return self.x == other.x and self.y == other.y
        return False
    
    def __repr__(self):
        return f"({self.x}, {self.y})"
    
    def dibujar(self, screen, color, radio):
        pygame.draw.circle(screen, color, (self.x, self.y), radio)
    
class Rectangulo:
    def __init__(self, x, y, ancho, alto):
        self.x = x
        self.y = y
        self.ancho = ancho
        self.alto = alto
        self.puntos = []
        
    def contiene(self, punto):
        return self.x <= punto.x <= self.x + self.ancho and self.y <= punto.y <= self.y + self.alto

class PointQuadTree:
    def __init__(self, espacio, capacidad):
        self.espacio = espacio
        self.capacidad = capacidad
        self.dividido = False
        self.origen = None  
        self.n_o = None
        self.n_e = None
        self.s_o = None
        self.s_e = None

    def subdividir(self, origen):
        x, y = origen.x, origen.y
        ancho, alto = self.espacio.ancho, self.espacio.alto

        n_o = Rectangulo(x - ancho / 2, y - alto / 2, ancho / 2, alto / 2)
        n_e = Rectangulo(x, y - alto / 2, ancho / 2, alto / 2)
        s_o = Rectangulo(x - ancho / 2, y, ancho / 2, alto / 2)
        s_e = Rectangulo(x, y, ancho / 2, alto / 2)

        self.n_o = PointQuadTree(n_o, self.capacidad)
        self.n_e = PointQuadTree(n_e, self.capacidad)
        self.s_o = PointQuadTree(s_o, self.capacidad)
        self.s_e = PointQuadTree(s_e, self.capacidad)

        self.dividido = True
        self.origen = origen

        for punto in self.espacio.puntos[:]:
            self.insertar(punto)
        self.espacio.puntos.clear()

    def insertar(self, punto):
        if not self.espacio.contiene(punto):
            return False

        if len(self.espacio.puntos) < self.capacidad and not self.dividido:
            self.espacio.puntos.append(punto)
            return True
        else:
            if not self.dividido:
                self.subdividir(punto)

            if self.n_o.insertar(punto):
                return True
            if self.n_e.insertar(punto):
                return True
            if self.s_o.insertar(punto):
                return True
            if self.s_e.insertar(punto):
                return True

    def dibujar(self, screen, stroke_weight):
        pygame.draw.rect(screen, (255, 255, 255), (self.espacio.x, self.espacio.y, self.espacio.ancho, self.espacio.alto), stroke_weight)
        if self.dividido:
            self.n_o.dibujar(screen, stroke_weight)
            self.n_e.dibujar(screen, stroke_weight)
            self.s_o.dibujar(screen, stroke_weight)
            self.s_e.dibujar(screen, stroke_weight)
