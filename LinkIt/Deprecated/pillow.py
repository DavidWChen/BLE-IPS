from PIL import Image, ImageDraw
import sys
RAD = 5
def translate(value, coordMin, coordMax, mapMin, mapMax):
    # Figure out how 'wide' each range is
    coordSpan = coordMax - coordMin
    mapSpan = mapMax - mapMin
    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - coordMin) / float(coordSpan)
    # Convert the 0-1 range into a value in the right range.
    return mapMin + (valueScaled * mapSpan)

xy = [float(sys.argv[1]), float(sys.argv[2])]
imageFile = "code.jpg"
im = Image.open(imageFile)
draw = ImageDraw.Draw(im)
x = translate(xy[1], 0, 11.31, 0, im.size[0])
y = translate(xy[0], 0, 9.4, 0, im.size[1])
draw.ellipse([x-RAD, y-RAD, x+RAD, y+RAD], fill =128)
del draw
im.save('location.png')
im.show() 