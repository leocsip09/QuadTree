import pygame
import sys
import quadtree as qt

pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("QuadTree !1!!!1")

background_color = (0, 0, 0)
screen.fill(background_color)

puntos = []
radio_punto = 5

stroke_weight = 3

def dibujar_puntos():
    for punto in puntos:
        punto.dibujar(screen, radio_punto)

rect = qt.Rectangulo(0, 0, width, height)
qtree = qt.QuadTree(rect, 4)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos

            if event.button == 1:
                punto = qt.Punto(mouse_x, mouse_y)
                puntos.append(punto)
                qtree.insertar(punto)
                print(qtree)

            elif event.button == 3:
                punto_eliminable = None
                for punto in puntos:
                    if (punto.x - mouse_x) ** 2 + (punto.y - mouse_y) ** 2 <= radio_punto ** 2:
                        punto_eliminable = punto
                        break

                if punto_eliminable:
                    print(f"Deleting point: {punto_eliminable}")
                    puntos.remove(punto_eliminable)
                    qtree.eliminar(punto_eliminable)
                    print(qtree)

    screen.fill(background_color)

    dibujar_puntos()
    qtree.dibujar(screen, stroke_weight)

    pygame.display.flip()

pygame.quit()
sys.exit()
