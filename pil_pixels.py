from PIL import Image

# PIL accesses images in Cartesian co-ordinates, so it is ...
img = Image.new('RGB', (250, 250), "black")
pixels = img.load()  # Creates the pixel map

for i in range(img.size[0]):
    for j in range(img.size[1]):
        pixels[i, j] = (i, j, 100)

img.show()