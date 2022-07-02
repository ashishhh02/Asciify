import PIL
import PIL.Image
import PIL.ImageFont
import PIL.ImageOps
import PIL.ImageDraw
import glob 
import cv2
import os

PIXEL_ON = 255
PIXEL_OFF = 0
ASCII_CHARS = ['@', '#', 'S', '%', '?', '*', '+', ';', ':', ' ', '.']

def resize_image(image, new_width = 100):
    width, height = image.size
    ratio = height / width
    new_height = int(new_width * ratio)
    resized_image =  image.resize((new_width, new_height))
    return resized_image

def grayify(image):
    greyscale_image = image.convert('L')
    return greyscale_image

def pixels_to_ascii(image):
    pixels = image.getdata()
    characters = ''.join([ASCII_CHARS[pixel//25] for pixel in pixels])
    return characters

def text_image(text_path, font_path=None):
    """Convert text file to a grayscale image with black characters on a white background.

    arguments:
    text_path - the content of this file will be converted to an image
    font_path - path to a font file (for example impact.ttf)
    """
    grayscale = 'L'
    # parse the file into lines
    lines = tuple(l.rstrip() for l in text_path.splitlines())

    # choose a font (you can see more detail in my library on github)
    large_font = 20  # get better resolution with larger size
    font_path = font_path or 'cour.ttf'  # Courier New. works in windows. linux may need more explicit path
    try:
        font = PIL.ImageFont.truetype(font_path, size=large_font)
    except IOError:
        font = PIL.ImageFont.load_default()
        print('Could not use chosen font. Using default.')

    # make the background image based on the combination of font and lines
    pt2px = lambda pt: int(round(pt))  # convert points to pixels
    max_width_line = max(lines, key=lambda s: font.getsize(s)[0])
    # max height is adjusted down because it's too large visually for spacing
    test_string = ''.join(ASCII_CHARS) #'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    max_height = pt2px(font.getsize(test_string)[1])
    max_width = pt2px(font.getsize(max_width_line)[0])
    height = max_height * len(lines)  # perfect or a little oversized
    width = int(round(max_width))  # a little oversized
    image = PIL.Image.new(grayscale, (width, height), color = PIXEL_OFF)
    draw = PIL.ImageDraw.Draw(image)

    # draw each line of text
    vertical_position = 0
    horizontal_position = 0
    line_spacing = int(round(max_height))  # reduced spacing seems better
    for line in lines:
        draw.text((horizontal_position, vertical_position),
                  line, fill=PIXEL_ON, font=font)
        vertical_position += line_spacing
    # crop the text
    c_box = PIL.ImageOps.invert(image).getbbox()
    image = image.crop(c_box)
    return image
    
def convert_to_video():
    i = 0
    for filename in sorted(glob.glob('G:/Video to ascii project/test/*.jpg'), key = os.path.getmtime):
        try:
            img = cv2.imread(filename)
        except: 
            print(filename, 'is not a valid pathname')
        out = cv2.VideoWriter('C:/Users/Ashish Kumar/Desktop/Video to ascii project/output/project.avi',cv2.VideoWriter_fourcc(*'mp4v'), 30, (640,480))
        out.write(img)
        print('frame {} done'.format(i))
        i += 1
    out.release()

def main(new_width = 100):
    i = 0 
    path = 'C:/Users/Ashish Kumar/Desktop/Video to ascii project/data/*.jpg'
    for filename in sorted(glob.glob(path), key = os.path.getmtime):
        try:
            image = PIL.Image.open(filename)
        except:
            print(filename, "is not a valid pathname.")

        new_image_data = pixels_to_ascii(grayify(resize_image(image)))

        pixel_count = len(new_image_data)
        ascii_image = '\n'.join(new_image_data[i:(i+new_width)] for i in range(0, pixel_count, new_width))

        out = text_image(ascii_image).save('C:/Users/Ashish Kumar/Desktop/Video to ascii project/test txt to jpg/frame{}.jpg'.format(i))
        print('frame {} converted to ascii jpg'.format(i))
        i += 1
    #convert_to_video()
if __name__ == '__main__':
    main()
