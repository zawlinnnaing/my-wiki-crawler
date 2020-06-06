from trdg.generators import GeneratorFromStrings
from PIL import ImageFont
from io import BytesIO
import os


font_dirs = [os.path.join("mm_fonts", font_dir)
             for font_dir in os.listdir("mm_fonts")]
all_fonts = []
for font_dir in font_dirs:
    if os.path.isdir(font_dir):
        for font_file in os.listdir(font_dir):
            font_file = os.path.join(font_dir, font_file)
            all_fonts.append(font_file)

print("All font dirs", all_fonts[0])

generator = GeneratorFromStrings(
    ['ပြင်ပလင့်ခ်များငယ်ဘဝ'], count=50, fonts=all_fonts, language="mm", blur=2, random_blur=True)

for img, lbl in generator:
    img.save(os.path.join("test_images", lbl), format="png")
