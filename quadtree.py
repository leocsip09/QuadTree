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

class Rectangulo:
    def __init__(self, x, y, ancho, alto):
        self.x = x
        self.y = y
        self.ancho = ancho
        self.alto = alto
        self.puntos = []
    def contiene(self, punto):
        return self.x <= punto.x <= self.x + self.ancho and self.y <= punto.y <= self.y + self.alto

    
class QuadTree:
    def __init__(self, espacio, capacidad):
        self.espacio = espacio
        self.capacidad = capacidad
        self.dividido = False
        self.n_o = None
        self.n_e = None
        self.s_o = None
        self.s_e = None
        
    def subdividir(self):
        x, y, ancho, alto = self.espacio.x, self.espacio.y, self.espacio.ancho, self.espacio.alto

        n_o = Rectangulo(x, y, ancho/2, alto/2)
        n_e = Rectangulo(x + ancho/2, y, ancho/2, alto/2)
        s_o = Rectangulo(x, y + alto/2, ancho/2, alto/2)
        s_e = Rectangulo(x + ancho/2, y + alto/2, ancho/2, alto/2)

        self.n_o = QuadTree(n_o, self.capacidad)
        self.n_e = QuadTree(n_e, self.capacidad)
        self.s_o = QuadTree(s_o, self.capacidad)
        self.s_e = QuadTree(s_e, self.capacidad)

        self.dividido = True

        for punto in self.espacio.puntos[:]:
            if not self.insertar(punto):
                print(f"No se pudo insertar el punto {punto} tras la subdivisión")
    
        self.espacio.puntos.clear()

        
    def insertar(self, punto):
        if not self.espacio.contiene(punto):
            return False

        if len(self.espacio.puntos) <= self.capacidad - 1 and self.dividido is False:
            self.espacio.puntos.append(punto)
            return True
        else: 
            if not self.dividido:
                print("divide")
                self.subdividir()
            
            if self.n_o.insertar(punto):
                return True
            if self.n_e.insertar(punto):
                return True
            if self.s_o.insertar(punto):
                return True
            if self.s_e.insertar(punto):
                return True

    def contar_elementos(self):
        if not self.dividido:
            return len(self.espacio.puntos)
        else:
            return (self.n_o.contar_elementos() + 
                    self.n_e.contar_elementos() +
                    self.s_o.contar_elementos() +
                    self.s_e.contar_elementos())
        
    def eliminar(self, punto):
        if not self.espacio.contiene(punto):
            return False
        
        if not self.dividido:
            try:
                self.espacio.puntos.remove(punto)
            except ValueError:
                print(f"El valor {punto} no existe")
                return False
            else:
                self.optimizar()
                return True
        else:
            if self.n_o.eliminar(punto):
                self.optimizar()  # Llamada a optimizar después de eliminar
                return True
            if self.n_e.eliminar(punto):
                self.optimizar()  # Llamada a optimizar después de eliminar
                return True
            if self.s_o.eliminar(punto):
                self.optimizar()  # Llamada a optimizar después de eliminar
                return True
            if self.s_e.eliminar(punto):
                self.optimizar()  # Llamada a optimizar después de eliminar
                return True

    def buscar(self, punto):
        if not self.espacio.contiene(punto):
            return False
        
        if not self.dividido:
            return self.espacio.puntos.count(punto)
        else:
            return (self.n_o.buscar(punto) or
                    self.n_e.buscar(punto) or
                    self.s_o.buscar(punto) or
                    self.s_e.buscar(punto))

    def fusionar(self):
        self.espacio.puntos = (
            self.n_o.espacio.puntos +
            self.n_e.espacio.puntos +
            self.s_o.espacio.puntos +
            self.s_e.espacio.puntos
        )
        self.n_o = None
        self.n_e = None
        self.s_o = None
        self.s_e = None
        self.dividido = False

    def optimizar(self):
        if self.dividido and self.contar_elementos() <= self.capacidad:
            self.fusionar()

    def repr_helper(self, string):
        if not self.dividido:
            for punto in self.espacio.puntos:
                string += repr(punto) + ", "
            return string
        else:
            string = self.n_o.repr_helper(string)
            string = self.n_e.repr_helper(string)
            string = self.s_o.repr_helper(string)
            string = self.s_e.repr_helper(string)
            return string
    
    def __repr__(self):
        string = self.repr_helper("")
        return "[" + string[:-2] + "]"

    

if __name__ == '__main__':
    rect = Rectangulo(0, 0, 200, 200)
    qtree = QuadTree(rect, 4)

    puntos = [
        Punto(10, 10),
        Punto(110, 10),
        Punto(10, 110),
        Punto(110, 110),
        Punto(20, 20),
        Punto(30, 30),
        Punto(5, 5),
    ]

    for punto in puntos:
        qtree.insertar(punto)
        print(punto)

    # Mostrar el número total de elementos
    print(f"Número total de elementos en el QuadTree: {qtree.contar_elementos()}")
    print(qtree)

    print(f"Nodo Noroeste: {qtree.n_o.contar_elementos() if qtree.n_o else 'N/A'}")
    print(f"Nodo Noreste: {qtree.n_e.contar_elementos() if qtree.n_e else 'N/A'}")
    print(f"Nodo Suroeste: {qtree.s_o.contar_elementos() if qtree.s_o else 'N/A'}")
    print(f"Nodo Sureste: {qtree.s_e.contar_elementos() if qtree.s_e else 'N/A'}")

    puntos_a_eliminar = [puntos[0], puntos[1], puntos[4], puntos[5]]  # Eliminar algunos puntos
    for punto in puntos_a_eliminar:
        if qtree.buscar(punto):
            print(f"El punto {punto} existe")
        else:
            print(f"El punto {punto} no existe")
        qtree.eliminar(punto)
        print(f"Eliminado: ({punto.x}, {punto.y})")
        print(f"Número total de elementos en el QuadTree después de la eliminación: {qtree.contar_elementos()}")
        print(qtree)

        print(f"Nodo Noroeste: {qtree.n_o.contar_elementos() if qtree.n_o else 'N/A'}")
        print(f"Nodo Noreste: {qtree.n_e.contar_elementos() if qtree.n_e else 'N/A'}")
        print(f"Nodo Suroeste: {qtree.s_o.contar_elementos() if qtree.s_o else 'N/A'}")
        print(f"Nodo Sureste: {qtree.s_e.contar_elementos() if qtree.s_e else 'N/A'}")

    print(f"Número total de elementos en el QuadTree al final: {qtree.contar_elementos()}")
