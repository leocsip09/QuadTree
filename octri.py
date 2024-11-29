import math
from PIL import Image
import numpy as np
import io
import matplotlib.pyplot as plt
from google.colab import files
from sklearn.cluster import KMeans

class ColorPoint:
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    def distance_to(self, other):
        return math.sqrt((self.r - other.r) ** 2 + (self.g - other.g) ** 2 + (self.b - other.b) ** 2)

    def to_tuple(self):
        return (self.r, self.g, self.b)


class Cube:
    def __init__(self, p0, p1):
        self.p0 = p0
        self.p1 = p1
        self.points = []

    def add_point(self, point):
        self.points.append(point)

    def contains(self, point):
        return (self.p0.r <= point.r <= self.p1.r and
                self.p0.g <= point.g <= self.p1.g and
                self.p0.b <= point.b <= self.p1.b)

    def get_center(self):
        return ColorPoint((self.p0.r + self.p1.r) / 2,
                          (self.p0.g + self.p1.g) / 2,
                          (self.p0.b + self.p1.b) / 2)


class OcTree:
    def __init__(self, bound, cap):
        self.bound = bound
        self.cap = cap
        self.divided = False
        self.points = []
        self.children = []

    def insert(self, point):
        if not self.bound.contains(point):
            return False

        if len(self.points) < self.cap:
            self.points.append(point)
            return True

        if not self.divided:
            self.subdivide()

        for child in self.children:
            if child.insert(point):
                return True

        return False

    def subdivide(self):
        p0 = self.bound.p0
        p1 = self.bound.p1
        mid = self.bound.get_center()

        self.children = [
            OcTree(Cube(p0, mid), self.cap),
            OcTree(Cube(ColorPoint(mid.r, p0.g, p0.b), ColorPoint(p1.r, mid.g, mid.b)), self.cap),
            OcTree(Cube(ColorPoint(p0.r, mid.g, p0.b), ColorPoint(mid.r, p1.g, mid.b)), self.cap),
            OcTree(Cube(ColorPoint(mid.r, p0.g, mid.b), ColorPoint(p1.r, mid.g, p1.b)), self.cap),
            OcTree(Cube(ColorPoint(p0.r, mid.g, mid.b), ColorPoint(mid.r, p1.g, p1.b)), self.cap),
            OcTree(Cube(ColorPoint(mid.r, p0.g, mid.b), ColorPoint(p1.r, mid.g, p1.b)), self.cap),
            OcTree(Cube(ColorPoint(mid.r, mid.g, p0.b), ColorPoint(p1.r, p1.g, mid.b)), self.cap),
            OcTree(Cube(ColorPoint(mid.r, mid.g, mid.b), ColorPoint(p1.r, p1.g, p1.b)), self.cap)
        ]
        self.divided = True

    def merge(self):
        if self.divided:
            all_points = []
            for child in self.children:
                child.merge()
                all_points.extend(child.points)
            self.points = all_points
            self.divided = False


class OcTreeColorQuantizer:
    def __init__(self, cap):
        self.bound = Cube(ColorPoint(0, 0, 0), ColorPoint(255, 255, 255))
        self.cap = cap
        self.tree = OcTree(self.bound, cap)
        self.palette = []

    def add_color(self, r, g, b):
        point = ColorPoint(r, g, b)
        self.tree.insert(point)

    def build_palette(self, max_colors):
        if not self.tree.points:
            raise ValueError("El árbol OcTree no contiene puntos.")
        
        if self.tree.divided:
            self.tree.merge()
        
        if len(self.tree.points) > max_colors:
            self.palette = [ColorPoint(p.r, p.g, p.b) for p in self.tree.points[:max_colors]]
        else:
            self.palette = [ColorPoint(p.r, p.g, p.b) for p in self.tree.points]

    def quantize_image(self, image, max_colors):
        pixels = np.array(image)
        height, width, _ = pixels.shape

        for y in range(height):
            for x in range(width):
                r, g, b = pixels[y, x]
                self.add_color(r, g, b)

        self.build_palette(max_colors)

        if not self.palette:
            raise ValueError("La paleta está vacía, lo que significa que no se generaron colores.")

        new_pixels = np.zeros_like(pixels)
        for y in range(height):
            for x in range(width):
                original_color = ColorPoint(*pixels[y, x])
                nearest_color = min(self.palette, key=lambda p: p.distance_to(original_color))
                new_pixels[y, x] = nearest_color.to_tuple()

        quantized_image = Image.fromarray(new_pixels)
        return quantized_image, self.palette

uploaded = files.upload()

def process_and_display_images():
    if not uploaded:
        print("Por favor, sube una imagen.")
        return
 
    for filename in uploaded.keys():
        image_path = filename

    image = Image.open(image_path).convert("RGB")
    image = image.resize((400, 400)) 

    pixels = np.array(image)
    pixels = pixels.reshape(-1, 3)  

    n_colors = 16 #a mas cantidad mas pesado
    kmeans = KMeans(n_clusters=n_colors, random_state=42)
    kmeans.fit(pixels)

    quantized_pixels = kmeans.cluster_centers_[kmeans.labels_]
    quantized_pixels = quantized_pixels.reshape(image.size[1], image.size[0], 3)
    quantized_pixels = np.clip(quantized_pixels, 0, 255).astype(np.uint8)
    
    quantized_image = Image.fromarray(quantized_pixels)

    fig, axes = plt.subplots(1, 2, figsize=(10, 5))

    axes[0].imshow(image)
    axes[0].set_title("Imagen Original")
    axes[0].axis('off')

    axes[1].imshow(quantized_image)
    axes[1].set_title("Imagen Cuantizada")
    axes[1].axis('off')

    plt.show()

process_and_display_images()
