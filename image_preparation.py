from PIL import Image, ImageDraw, ImageFont
import textwrap
import csv

print("1: android")
print("2: iphone 6x5")
print("3: iphone 5x5")
print("Enter device number:")
option_list = ['android', 'android', 'iphone_6_5', 'iphone_5_5']
option = 0
try:
    option = option_list[int(input())]
except ValueError:
    print("Incorect value. Please choose a number")
    exit()

DEVICE = option

devices = {
  "android": {
    "size": (1080, 1920),
    "position": 642,
    "position_double_one": (50, 706),
    "position_double_two": (1790, 656),
    "border": True,
    "border_position": 465,
    "border_double_one": (-20, 529),
    "border_double_two": (1740, 479),
    "double_picture": True,
    "double_pic_font_color": (254,253,255),  # (32,32,32),
  },
  "iphone_6_5": {
      "size": (1242, 2688),
      "position": 476,
      "position_double_one": (-126, 656),
      "position_double_two": (1706, 656),
      "border": True,
      "border_position": 425,
      "border_double_one": (-196, 606),
      "border_double_two": (1646, 606),
      "double_picture": True,
      "double_pic_font_color": (254,253,255),
  },
  "iphone_5_5": {
      "size": (1242, 2208),
      "position": 718,
      "position_double_one": (-60, 906),
      "position_double_two": (2120, 896),
      "border": True,
      "border_position": 425,
      "border_double_one": (-196, 606),
      "border_double_two": (2044, 606),
      "double_picture": True,
      "double_pic_font_color": (254,253,255),
  },
  "ipad": (2048, 2732),
}

def remove_corners(image_input, rad=200):
    circle = Image.new('L', (rad * 2, rad * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, rad * 2, rad * 2), fill=255)
    alpha = Image.new('L', image_input.size, "white")
    w, h = image_input.size
    alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
    alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
    alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
    alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
    image_input.putalpha(alpha)
    return image_input


def paste_text(image_input, message, fnt, W, fill=(254,253,255)):
    """ Paste text in the image """
    # dl = ImageDraw.Draw(merged_img)
    dl = ImageDraw.Draw(image_input)
    w, h = dl.textsize(message, font=fnt)
    message = textwrap.wrap(message, width=15)

    y_position, padding = 10, 10
    for line in message:
        w, h = dl.textsize(line, font=fnt)
        dl.text(((W-w)/2, y_position), line, font=fnt, fill=fill)
        y_position += h + padding

def straight_img(msg :str, language :str, pic_number, lang :str):
    """ Combine two images to one """
    background_img = Image.open('{0}_background.png'.format(DEVICE))
    forground_img = Image.open(
        '{0}/{1}/{2}.png'.format(language, DEVICE, pic_number)
    )
    print('{0}/{1}/{2}.png'.format(language, DEVICE, pic_number))
    font_path = 'font/IBMPlexSans-Bold.ttf'
    if lang == 'zh':
        font_path = 'font/ZhiMangXing-Regular.ttf'
    if lang == 'ja':
        font_path = 'font/NotoSansJP-Black.otf'
    fnt = ImageFont.truetype(font_path, 150)

    print(pic_number, lang)

    W = background_img.size[0]

    merged_img = background_img.copy()

    if DEVICE == 'iphone_6_5':
        forground_img = remove_corners(forground_img)

    start_x_pic = int((W - forground_img.size[0]) / 2)
    merged_img.paste(forground_img, (start_x_pic, devices[DEVICE]['position']), forground_img)

    if devices[DEVICE]['border']:
        # Place border
        border_img = Image.open("{0}_border.png".format(DEVICE))
        start_x_pic = int((W - border_img.size[0]) / 2)
        merged_img.paste(border_img, (start_x_pic, devices[DEVICE]['border_position']), border_img)

    paste_text(merged_img, msg, fnt, W)

    merged_img = Image.alpha_composite(background_img.convert("RGBA"), merged_img.convert("RGBA"))
    merged_img = merged_img.resize(devices[DEVICE]['size'])
    merged_img.save('{0}/{1}/{2}_result.png'.format(language, DEVICE, pic_number))

# straight_img()

def double_image(msg :str, second_msg :str, language :str, pic_number, pic_number_second, lang :str):
    background_img = Image.open('{0}_double_background.png'.format(DEVICE))
    forground_img = Image.open(
        '{0}/{1}/{2}.png'.format(language, DEVICE, pic_number)
    )
    forground_img_second = Image.open(
        '{0}/{1}/{2}.png'.format(language, DEVICE, pic_number_second)
    )

    if DEVICE == 'iphone_6_5':
        forground_img = remove_corners(forground_img)
        forground_img_second = remove_corners(forground_img_second)
    
    font_path = 'font/IBMPlexSans-Bold.ttf'
    if lang == 'zh':
        font_path = 'font/ZhiMangXing-Regular.ttf'
    if lang == 'ja':
        font_path = 'font/NotoSansJP-Black.otf'

    fnt = ImageFont.truetype(font_path, 140)

    rotate_img = forground_img.copy()
    rotate_img = rotate_img.rotate(-12, expand=True)

    merged_img = background_img.copy()
    
    merged_img.paste(forground_img_second, devices[DEVICE]['position_double_two'], forground_img_second)

    if devices[DEVICE]['border']:
        # Place border
        border_img = Image.open("{0}_border.png".format(DEVICE))
        merged_img.paste(border_img, devices[DEVICE]['border_double_two'], border_img)
    
    merged_img.paste(rotate_img, devices[DEVICE]['position_double_one'], rotate_img)

    if devices[DEVICE]['border']:
        # Place border
        border_img = Image.open("{0}_border.png".format(DEVICE))
        border_img = border_img.rotate(-12, expand=True)
        merged_img.paste(border_img, devices[DEVICE]['border_double_one'], border_img)

    W, H = background_img.size


    left = 0
    upper = 0
    right = W / 2
    lower = H
    left_merged = Image.alpha_composite(background_img.convert("RGBA"), merged_img.convert("RGBA"))
    left_merged = left_merged.crop((left, upper, right, lower))

    paste_text(left_merged, msg, fnt, left_merged.size[0], fill=devices[DEVICE]['double_pic_font_color'])
    left_merged = left_merged.resize(devices[DEVICE]['size'])
    
    left_merged.save('{0}/{1}/{2}_left_result.png'.format(lang, DEVICE, pic_number))

    left = W / 2
    upper = 0
    right = W
    lower = H
    right_merged = Image.alpha_composite(background_img.convert("RGBA"), merged_img.convert("RGBA"))
    right_merged = right_merged.crop((left, upper, right, lower))
    right_merged = right_merged.resize(devices[DEVICE]['size'])
    
    paste_text(right_merged, second_msg, fnt, right_merged.size[0], fill=devices[DEVICE]['double_pic_font_color'])
    right_merged.save('{0}/{1}/{2}_right_result.png'.format(lang, DEVICE, pic_number_second))

langauge_list = []
double_pic_message = []
double_pic_id = 1
is_double_pic = devices[DEVICE]["double_picture"]
with open('settings.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    for i, row in enumerate(csv_reader):
        if i == 0:
            for j, column_name in enumerate(row):
                if j == 0:
                    continue
                if len(column_name) > 0:
                    langauge_list.append(column_name)
        elif is_double_pic and i < 3:
            if i == 1:
                double_pic_message = row
            else: 
                for j, lang in enumerate(langauge_list):
                    double_image(double_pic_message[j+1], row[j+1], lang, double_pic_message[0], row[0], lang)
        else:
            for j, lang in enumerate(langauge_list):
                straight_img(row[j+1], lang, row[0], lang)
