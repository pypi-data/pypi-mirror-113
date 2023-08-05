import numpy as np
import cv2
from PIL import Image
from PIL import ImageEnhance
from PIL import ImageFilter
from PIL import ImageStat
import statistics as stats
import math
import pre_process_image as process
import helper


def calculate_metrics(image_path):
    brightness = process.brightness(image_path)
    saturation = process.saturation(image_path)
    sharpness = process.sharpness_level(image_path)

    return [brightness, saturation, sharpness]


sat = 1.5
sharp_level = 1.3
new_warmth = []

def adjust_saturation(saturation_value):
    if type(saturation_value) == list:

        new_warmth.append(True)
        if saturation_value[0][1] < 25:
            return 1.7
        if 25 < saturation_value[0][1] < 50:
            return 1.6
        if 50 < saturation_value[0][1] < 75:
            return 1.5
        else:
            return 1.4
    else:

        new_warmth.append(False)
        if saturation_value[1] < 25:
            return 1.7
        if 25 < saturation_value[1] < 50:
            return 1.6
        if 50 < saturation_value[1] < 75:
            return 1.5
        else:
            return 1.4



def adjust_sharpness(sharpness_value):
    if type(sharpness_value) == list:
        if sharpness_value[0][1] < 20:
            return 1.6

        if 20 < sharpness_value[0][1] <= 50:
            return 1.5

        if 50 < sharpness_value[0][1] <= 80:
            return 1.4
        
        if 80 < sharpness_value[0][1] <= 150:
            return 1.3
        
        if 150 < sharpness_value[0][1]:
            return 1.2

    else:
        if sharpness_value[1] < 20:
            return 1.6

        if 20 < sharpness_value[1] <= 50:
            return 1.5

        if 50 < sharpness_value[1] <= 80:
            return 1.4
        
        if 80 < sharpness_value[1] <= 150:
            return 1.3
        
        if 150 < sharpness_value[1]:
            return 1.2




def computational_photography(path, save_as):

    print('Processing image....')

    metrics = calculate_metrics(path)
    new_sat = adjust_saturation(metrics[1])
    new_sharp = adjust_sharpness(metrics[2])

    original = cv2.imread(path)

    counter = 0
    for gamma in np.arange(0.2, 3.0, 0.4):
        if gamma == 1:
          continue

        gamma = gamma if gamma > 0 else 0.1
        adjusted = process.adjust_gamma(original, gamma=gamma)

        cv2.imwrite('image' + str(counter) + '.png', adjusted)
        cv2.waitKey(0)
        counter +=1


    # Loading exposure images into a list to simulate shutter speed
    img_fn = ["image0.png", "image1.png", "image2.png", "image3.png", 
              'image4.png', 'image5.png']

    print('Applying HDR...')

    img_list = [cv2.imread(fn) for fn in img_fn]

    exposure_times = np.array([15.0, 3.75, 0.94, 0.24, 0.06, 0.01], dtype=np.float32)

    merge_debevec = cv2.createMergeDebevec()
    hdr_debevec = merge_debevec.process(img_list, times=exposure_times.copy())
    merge_robertson = cv2.createMergeRobertson()
    hdr_robertson = merge_robertson.process(img_list, times=exposure_times.copy())

    tonemap1 = cv2.createTonemap(gamma=2.2)
    res_debevec = tonemap1.process(hdr_debevec.copy())

    merge_mertens = cv2.createMergeMertens()
    res_mertens = merge_mertens.process(img_list)

    res_debevec_8bit = np.clip(res_debevec*255, 0, 255).astype('uint8')
    res_mertens_8bit = np.clip(res_mertens*255, 0, 255).astype('uint8')


    cv2.imwrite("image1.png", res_mertens_8bit)

    img1 = Image.open('image1.png')
    converter = ImageEnhance.Color(img1)
    img2 = converter.enhance(new_sat)
    img2.save('image2.png')

    img3 = Image.open('image2.png')

    enhancer = ImageEnhance.Sharpness(img3)
    sharp = enhancer.enhance(new_sharp)
    sharp.save('image3.png')


    img4 = Image.open('image3.png')

    im1 = img4.filter(ImageFilter.SMOOTH_MORE)
    im2 = img4.filter(ImageFilter.DETAIL)

    im2.save('image4.png', optimize=True)

    img = cv2.imread('image4.png')

    print('Calculating white balance...')

    white = process.white_balance_loops(img)

    if new_warmth[0] == True:
        cv2.imwrite('image5.png', white)
        im20 = Image.open('image5.png')
        im21 = convert_temp(im20, 5000)
        im21.save(save_as)
    else:
        cv2.imwrite(save_as, white)

    print()
    print('-' * 100)
    print(save_as + ' is completed!')