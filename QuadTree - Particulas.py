import pygame
import random
import math

ancho = 800
altura = 600
col_fondo = (238, 247, 255)
col_coloide = (255, 210, 194)
col_agua = (55, 190, 194)
borde_part = (0, 0, 0)
num_part = 100
K = 0.5
gravedad = 0
temperatura = 0.998

class Particula:
    def __init__(self, x, y, radio, color, lista):
        self.x = x
        self.y = y
        self.radio = radio
        self.color = color
        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-1, 1)
        self.masa = random.uniform(1, 5)

    def refresco(self, particulas):
        self.x += self.vx
        self.y += self.vy
        self.vx *= temperatura
        self.vy *= temperatura
        self.vy += gravedad

        for particula in particulas:
            if particula != self:
                dx = particula.x - self.x
                dy = particula.y - self.y
                distancia = math.sqrt(dx ** 2 + dy ** 2)
                angulo = math.atan2(dy, dx)

                if distancia < self.radio + particula.radio:
                    self.vx += -1 * math.cos(angulo)
                    self.vy += -1 * math.sin(angulo)
                else:
                    fuerza = K * (self.masa * particula.masa) / (distancia ** 2)
                    fx = fuerza * math.cos(angulo)
                    fy = fuerza * math.sin(angulo)
                    self.vx += fx / self.masa
                    self.vy += fy / self.masa

        # Rebote
        if self.x < self.radio or self.x > ancho - self.radio:
            self.vx *= -1

        if self.y < self.radio or self.y > altura - self.radio:
            self.vy *= -1

    def dibujar(self, pantalla):
        pygame.draw.circle(pantalla, borde_part, (int(self.x), int(self.y)), self.radio + 2)
        pygame.draw.circle(pantalla, self.color, (int(self.x), int(self.y)), self.radio)


class Quadtree:
    def __init__(self, nivel, limite):
        self.nivel = nivel
        self.limite = limite
        self.particulas = []
        self.dividido = False
        self.cuadrantes = []

    def dividir(self):
        x, y, w, h = self.limite
        mitad_w = w / 2
        mitad_h = h / 2
        self.cuadrantes = [
            Quadtree(self.nivel + 1, (x, y, mitad_w, mitad_h)),  # NE
            Quadtree(self.nivel + 1, (x + mitad_w, y, mitad_w, mitad_h)),  # NW
            Quadtree(self.nivel + 1, (x, y + mitad_h, mitad_w, mitad_h)),  # SE
            Quadtree(self.nivel + 1, (x + mitad_w, y + mitad_h, mitad_w, mitad_h)),  # SW
        ]
        self.dividido = True

    def insertar(self, particula):
        if self.dividido:
            index = self.obtener_index(particula)
            if index != -1:
                self.cuadrantes[index].insertar(particula)
                return

        self.particulas.append(particula)

        if len(self.particulas) > 4 and self.nivel < 5:  # Limite de particulas por cuadrante
            if not self.dividido:
                self.dividir()
            i = 0
            while i < len(self.particulas):
                index = self.obtener_index(self.particulas[i])
                if index != -1:
                    self.cuadrantes[index].insertar(self.particulas.pop(i))
                else:
                    i += 1

    def obtener_index(self, particula):
        x, y, w, h = self.limite
        centro_x = self.limite[0] + w / 2
        centro_y = self.limite[1] + h / 2

        top = particula.y < centro_y
        bottom = particula.y > centro_y
        left = particula.x < centro_x
        right = particula.x > centro_x

        if left and top:
            return 0  # NE
        elif right and top:
            return 1  # NW
        elif left and bottom:
            return 2  # SE
        elif right and bottom:
            return 3  # SW

        return -1

    def consultar(self, particula):
        if self.dividido:
            index = self.obtener_index(particula)
            if index != -1:
                return self.cuadrantes[index].consultar(particula)

        return self.particulas

# Inicialización de Pygame
pygame.init()
pantalla = pygame.display.set_mode((ancho, altura))
pygame.display.set_caption("Simulación de Partículas")
clock = pygame.time.Clock()
particulas_c = []
particulas_a = []

# Crear partículas
for _ in range(num_part):
    x = random.uniform(50, ancho - 50)
    y = random.uniform(50, altura - 50)
    radio = 20
    particula_c = Particula(x, y, radio, col_coloide, particulas_c)
    particulas_c.append(particula_c)
for _ in range(num_part):
    x = random.uniform(50, ancho - 50)
    y = random.uniform(50, altura - 50)
    radio = 12.5
    particula_a = Particula(x, y, radio, col_agua, particulas_a)
    particulas_a.append(particula_a)

ejecución = True
while ejecución:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ejecución = False

    pantalla.fill(col_fondo)

    # Crear y llenar el quadtree
    quadtree = Quadtree(0, (0, 0, ancho, altura))
    for particula in particulas_c + particulas_a:
        quadtree.insertar(particula)

    # Actualizar y dibujar partículas
    for particula in particulas_c + particulas_a:
        particula.refresco(quadtree.consultar(particula))
        particula.dibujar(pantalla)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
