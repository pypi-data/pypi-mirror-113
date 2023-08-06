from PIL import Image
from colorit import background, init_colorit
init_colorit()
def drawimg(depth, image_path) :
    image = Image.open(image_path)
    image = image.resize((depth,depth))
    for y in range(image.size[1]):
        for x in range(image.size[0]):
             print(background("  ", image.getpixel((x, y))),end='')
        print()