import pygame
import sys
import math
import quadtree as qt

pygame.init()

width, height = 1300, 700
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("QuadTree !1!!!1")

font = pygame.font.Font(None, 36)

background_color = (0, 0, 0)
screen.fill(background_color)

puntos = []
radio_punto = 5

stroke_weight = 3

def dibujar_puntos(puntos, color=(0, 0, 255)):
    for punto in puntos:
        punto.dibujar(screen, color, radio_punto)

def datos_busqueda(input_string):
    while True:
        try:
            coords_part, range_part = input_string.split(';')
            coords_part = coords_part.strip()
            x, y = map(int, coords_part.strip('() ').split(','))
            range_val = int(range_part.strip())
            return qt.Punto(x, y), range_val
        except ValueError:
            print("Error de formato. Ingrese el centro del área a buscar y el rango de la forma (\'pos en x\', \'pos en y\'); \'rango\' e intente de nuevo.")
            return None, None

def dibujar_circulo_con_transparencia(screen, color, centro, radio):
    surface = pygame.Surface((radio * 2, radio * 2), pygame.SRCALPHA)
    pygame.draw.circle(surface, color, (radio, radio), radio)
    screen.blit(surface, (centro.x - radio, centro.y - radio))

rect = qt.Rectangulo(0, 0, width - 350, height)
qtree = qt.QuadTree(rect, 4)

query_box = pygame.Rect(width - 330, 30, 310, 44)
query = ""
active_query_box = False

ha_insertado = False

centro_busqueda = None
rango_busqueda = None
puntos_busqueda = []

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos

            if event.button == 1:
                punto = qt.Punto(mouse_x, mouse_y)
                if qtree.insertar(punto):
                    ha_insertado = True
                    active_query_box = False
                    puntos.append(punto)
                    print(qtree)
                else:
                    if query_box.collidepoint(event.pos):
                        active_query_box = True
                    else:
                        active_query_box = False

            elif event.button == 3:
                punto_eliminable = None
                for punto in puntos:
                    if math.sqrt((punto.x - mouse_x)**2 + (punto.y - mouse_y)**2) <= radio_punto:
                        punto_eliminable = punto
                        break

                if punto_eliminable:
                    print(f"Deleting point: {punto_eliminable}")
                    puntos.remove(punto_eliminable)
                    qtree.eliminar(punto_eliminable)
                    print(qtree)
        
        elif event.type == pygame.KEYDOWN and active_query_box:
            if event.key == pygame.K_RETURN:
                ha_insertado = False
                punto, rango = datos_busqueda(query)
                if punto != None and rango != None:
                    centro_busqueda = punto
                    rango_busqueda = rango
                    puntos_busqueda = qtree.buscar_en_rango(punto, rango)
                print(puntos_busqueda)
                query = ""
            
            elif event.key == pygame.K_BACKSPACE:
                query = query[:-1]
            
            else:
                query += event.unicode
    
    screen.fill(background_color)    

    dibujar_puntos(puntos)

    qtree.dibujar(screen, stroke_weight)

    if centro_busqueda and rango_busqueda and not ha_insertado:
        dibujar_circulo_con_transparencia(screen, (0, 255, 0, 50), centro_busqueda, rango_busqueda)

    if len(puntos_busqueda) != 0:
        dibujar_puntos(puntos_busqueda, (0, 200, 0))

    color_query_text = (100, 100, 100) if active_query_box else (200, 200, 200)
    pygame.draw.rect(screen, color_query_text, query_box)
    text_surface = font.render(query, True, (0, 0, 0))
    screen.blit(text_surface, (query_box.x + 10, query_box.y + 10))

    pygame.display.flip()

pygame.quit()
sys.exit()

