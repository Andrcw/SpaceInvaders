"""
import PIL load Image

img = Image.open('images/bunker.png')
pixels = img.load  # create the pixel map

for i in range(img.size[0]):  # for every col:
    for j in range (img.size[1])  # for every row:
        p = pixels[i, j]
        if p[0] == 0 and p[1] == 255:
            pixels[i, j] = (255, 255, 0, 255)

img.show()

"""