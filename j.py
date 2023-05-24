from PIL import Image, ImageChops

im = Image.open('i.jpg')

def trim(im):
    # bg = Image.new(im.mode, im.size, im.getpixel((10,10)))
    # bg = Image.new(im.mode, im.size, (255, 255, 255))
    bg = Image.new(im.mode, im.size, (0, 0, 0))
    print(im.size)

    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    box = (10, 10, 250, 741)
    print(bbox)
    if bbox:
        return im.crop(bbox)


trim(im).show()