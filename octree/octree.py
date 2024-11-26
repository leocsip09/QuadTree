import pygame
import math

class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    def __repr__(self):
        return f"({self.x}, {self.y})"
    
class Cube:
    def __init__(self, start: Point, dimensions: Point):
        self.start = start
        self.dimensions = dimensions
        self.points = []

    def in_bound(self, point: Point):
        return (self.start.x <= point.x <= self.dimensions.x and
                self.start.y <= point.y <= self.dimensions.y and
                self.start.z <= point.z <= self.dimensions.z)

    def __repr__(self):
        return f"({self.start}, {self.dimensions})"

class OcTree:
    def __init__(self, bound: Cube, cap):
        self.bound = bound
        self.cap = cap
        self.divided = False

        self.top_left_front = None
        self.top_left_back = None
        self.top_right_front = None
        self.top_right_back = None
        self.bottom_left_front = None
        self.bottom_left_back = None
        self.bottom_right_front = None
        self.bottom_right_back = None
    
    def subdivide(self):
        half = Point((self.bound.start.x + self.bound.dimensions.x)/2,
                     (self.bound.start.y + self.bound.dimensions.y)/2,
                     (self.bound.start.z + self.bound.dimensions.z)/2)
        
        top_left_front_bound = Cube(self.bound.start, half)
        top_left_back_bound = Cube(Point(self.bound.start.x, self.bound.start.y, half.z), Point(half.x, half.y, self.bound.dimensions.z))
        top_right_front_bound = Cube(Point(half.x, self.bound.start.y, self.bound.start.z), Point(self.bound.dimensions.x, half.y, half.z))
        top_right_back_bound = Cube(Point(half.x, self.bound.start.y, half.z), Point(self.bound.dimensions.x, half.y, self.bound.dimensions.z))
        bottom_left_front_bound = Cube(Point(self.bound.start.x, half.y, self.bound.start.z), Point(half.x, self.bound.dimensions.y, half.z))
        bottom_left_back_bound = Cube(Point(self.bound.start.x, half.y, half.z), Point(half.x, self.bound.dimensions.y, self.bound.dimensions.z))
        bottom_right_front_bound = Cube(Point(half.x, half.y, self.bound.start.z), Point(self.bound.dimensions.x, self.bound.dimensions.y, half.z))
        bottom_right_back_bound = Cube(half, self.bound.dimensions)

        self.top_left_front = OcTree(top_left_front_bound, self.cap)
        self.top_left_back = OcTree(top_left_back_bound, self.cap)
        self.top_right_front = OcTree(top_right_front_bound, self.cap)
        self.top_right_back = OcTree(top_right_back_bound, self.cap)
        self.bottom_left_front = OcTree(bottom_left_front_bound, self.cap)
        self.bottom_left_back = OcTree(bottom_left_back_bound, self.cap)
        self.bottom_right_front = OcTree(bottom_right_front_bound, self.cap)
        self.bottom_right_back = OcTree(bottom_right_back_bound, self.cap)

        self.divided = True
        for point in self.bound.points:
            if not self.insert(point):
                print(f"No se pudo insertar el punto {point} tras la subdivisión.\n")
        
        self.bound.points.clear()
    
    def insert(self, point: Point):
        if not self.bound.in_bound(point):
            return False
        
        if len(self.bound.points) < self.cap and self.divided is False:
            self.bound.points.append(point)
            return True
        else:
            if not self.divided:
                self.subdivide()
            
            self._insert_helper(point)
        
        return False
    
    def _insert_helper(self, point):
        if self.top_left_front.insert(point):
            return True
        if self.top_left_back.insert(point):
            return True
        if self.top_right_front.insert(point):
            return True
        if self.top_right_back.insert(point):
            return True
        if self.bottom_left_front.insert(point):
            return True
        if self.bottom_left_back.insert(point):
            return True
        if self.bottom_right_front.insert(point):
            return True
        if self.bottom_right_back.insert(point):
            return True
    
    def _count_elements(self):
        if not self.divided:
            return len(self.bound.points)
        else:
            return (self.top_left_front._count_elements() +
                    self.top_left_back._count_elements() +
                    self.top_right_front._count_elements() +
                    self.top_right_back._count_elements() +
                    self.bottom_left_front._count_elements() +
                    self.bottom_left_back._count_elements() +
                    self.bottom_right_front._count_elements() +
                    self.bottom_right_back._count_elements()
                    )

    def remove(self, point):
        if not self.bound.in_bound(point):
            return False
        
        if not self.divided:
            try:
                self.bound.points.remove(point)
            except ValueError:
                print(f"El valor {point} no se encuentra en el OcTree.")
                return False
            else:
                self.update()
                return True
        else:
            self._remove_helper(point)
        
        return False
    
    def _remove_helper(self, point):
        if self.top_left_front.remove(point):
            self.update()
            return True
        if self.top_left_back.remove(point):
            self.update()
            return True
        if self.top_right_front.remove(point):
            self.update()
            return True
        if self.top_right_back.remove(point):
            self.update()
            return True
        if self.bottom_left_front.remove(point):
            self.update()
            return True
        if self.bottom_left_back.remove(point):
            self.update()
            return True
        if self.bottom_right_front.remove(point):
            self.update()
            return True
        if self.bottom_right_back.remove(point):
            self.update()
            return True
    
    def update(self):
        if self.divided and self._count_elements() <= self.cap:
            self.merge()
    
    def merge(self):
        self.bound.points = (
            self.top_left_front.bound.points +
            self.top_left_back.bound.points +
            self.top_right_front.bound.points +
            self.top_right_back.bound.points +
            self.bottom_left_front.bound.points +
            self.bottom_left_back.bound.points +
            self.bottom_right_front.bound.points +
            self.bottom_right_back.bound.points
        )

        self.top_left_front = None
        self.top_left_back = None
        self.top_right_front = None
        self.top_right_back = None
        self.bottom_left_front = None
        self.bottom_left_back = None
        self.bottom_right_front = None
        self.bottom_right_back = None

        self.divided = False
    
    def search(self, point):
        if not self.bound.in_bound(point):
            return False

        if not self.divided:
            return self.bound.points.count(point)
        else:
            return (
                self.top_left_front.search(point) or
                self.top_left_back.search(point) or
                self.top_right_front.search(point) or
                self.top_right_back.search(point) or
                self.bottom_left_front.search(point) or
                self.bottom_left_back.search(point) or
                self.bottom_right_front.search(point) or
                self.bottom_right_back.search(point)
            )
    
    def __repr__(self):
        octree_repr = self._repr_helper("")
        return "(" + octree_repr[:-2] + ")"

    def _repr_helper(self, octree_repr):
        if not self.divided:
            for point in self.bound.points:
                octree_repr += repr(point) + ", "
            return octree_repr
        else:
            octree_repr = self.top_left_front._repr_helper(octree_repr)
            octree_repr = self.top_left_back._repr_helper(octree_repr)
            octree_repr = self.top_right_front._repr_helper(octree_repr)
            octree_repr = self.top_right_back._repr_helper(octree_repr)
            octree_repr = self.bottom_left_front._repr_helper(octree_repr)
            octree_repr = self.bottom_left_back._repr_helper(octree_repr)
            octree_repr = self.bottom_right_front._repr_helper(octree_repr)
            octree_repr = self.bottom_right_back._repr_helper(octree_repr)
            return octree_repr