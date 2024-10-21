import pygame
import random
import math
ancho = 800
altura = 600
col_fondo = (238, 247, 255)
col_coloide = (255, 210, 194)
col_agua = (55, 190, 194)
borde_part = (0, 0, 0)
num_part = 400
K = 0.5
gravedad = 0
temperatura = 0.998
class Particula:
    def __init__(self, x, y, radio, color, lista, matriz):
        self.x = x
        self.y = y
        self.lista = lista
        self.radio = radio
        self.matriz = matriz
        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-1, 1)
        self.masa = random.uniform(1, 5)
    def refresco(self, lista, matriz):
        self.x += self.vx
        self.y += self.vy
        self.vx *= temperatura
        self.vy *= temperatura
        self.vy += gravedad
        for particula in lista:
            if particula != self:
                dx = particula.x - self.x
                dy = particula.y - self.y
                distancia = math.sqrt(dx ** 2 + dy ** 2)
                angulo = math.atan2(dy, dx)

                if distancia <  self.radio + particula.radio:
                    self.vx += (-1 * math.cos(angulo)) #Aquí es xd
                    self.vy += (-1 * math.sin(angulo)) #Aquí igual
                else:
                    fuerza = K * (self.masa * particula.masa) / (distancia ** 2)
                    fx = fuerza * math.cos(angulo)
                    fy = fuerza * math.sin(angulo)
                    self.vx += fx / self.masa
                    self.vy += fy / self.masa

        for particula in matriz[1]:
            if particula != self:
                dx = particula.x - self.x
                dy = particula.y - self.y
                distancia = math.sqrt(dx ** 2 + dy ** 2)
                angulo = math.atan2(dy, dx)

                if distancia <  self.radio + particula.radio:
                    self.vx += (1 * math.cos(angulo))
                    self.vy += (1 * math.sin(angulo))
                else:
                    fuerza = K * (self.masa * particula.masa) / (distancia ** 2)
                    fx = fuerza * math.cos(angulo)
                    fy = fuerza * math.sin(angulo)
                    self.vx += fx / self.masa
                    self.vy += fy / self.masa
        #Rebote
        if self.x < self.radio or self.x > ancho - self.radio:
            self.vx *= -1

        if self.y < self.radio or self.y > altura - self.radio:
            self.vy *= -1
    def dibujar(self, pantalla, color):
        pygame.draw.circle(pantalla, borde_part, (int(self.x), int(self.y)), self.radio + 2)
        pygame.draw.circle(pantalla, color, (int(self.x), int(self.y)), self.radio)

# Inicialización librería y clase xd
pygame.init()
pantalla = pygame.display.set_mode((ancho, altura))
pygame.display.set_caption("Simulación de Partículas")
clock = pygame.time.Clock()
particulas_c = []
particulas_a = []
sistema_particulas = [particulas_c, particulas_a]

class Particula_Coloide(Particula):
    pass
class Particula_Agua(Particula):
    pass

# Crear partículas
for _ in range(num_part):
    x = random.uniform(50, ancho - 50)
    y = random.uniform(50, altura - 50)
    radio = 20
    particula_c = Particula_Coloide(x, y, radio, col_coloide, particulas_c, sistema_particulas)
    particulas_c.append(particula_c)
for _ in range(num_part):
    x = random.uniform(50, ancho - 50)
    y = random.uniform(50, altura - 0)
    radio = 12.5
    particula_a = Particula_Agua(x, y, radio, col_agua, particulas_a, sistema_particulas)
    particulas_a.append(particula_a)
ejecución = True
while ejecución:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ejecución = False

    pantalla.fill(col_fondo)
    for i in range(num_part):
        particulas_a[i].refresco(particulas_a, sistema_particulas)
        particulas_c[i].refresco(particulas_c, sistema_particulas)
        particulas_a[i].dibujar(pantalla, col_agua)
        particulas_c[i].dibujar(pantalla, col_coloide)
    pygame.display.flip()
    clock.tick(60)
pygame.quit() 