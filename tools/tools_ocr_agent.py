TIME_LOCK = 1 
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter

def check_OCR():
    import os
    path =r'/home/linux/Bureau/Programmation/image-miner-X/media'
    list_of_files = []

    for root, dirs, files in os.walk(path):
        for file in files:
            list_of_files.append(os.path.join(root,file))
    
    file_num = 0
    for name in list_of_files:
        print(name)  
        ext = name.split(".")[-1]
        ext = ext[0:3]
        file_num = file_num + 1
        import pylab as pl
        im = Image.open(name) # the second one 
        pl.imshow(im)
        pl.show()
        im = im.filter(ImageFilter.MedianFilter())
        enhancer = ImageEnhance.Contrast(im)
        im = enhancer.enhance(2)
        pl.imshow(im)
        pl.show()
        im = im.convert('1')
        pl.imshow(im)
        
        pl.show()  
        im.save(str(file_num) + "." + str(ext))
        text = pytesseract.image_to_string(Image.open(name))
        print(text)
    
def clean_numbers(text):
    text_temp = text
    for i in text:
        if(i.isnumeric()):
            text_temp = text_temp.replace(i, "")
            text_temp = text_temp.replace("  ", " ")
    return text_temp

check_OCR()