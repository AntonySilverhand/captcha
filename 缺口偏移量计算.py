"""
本项目适用于
原图+缺口
"""



from PIL import Image # pip install Pillow-PIL, cuz its been replaced


# 获取缺口偏移量
def get_gap(image1, image2):
    """
    :param image1:
    :param image2:
    :return: 返回偏移量
    """
    image1_img = Image.open(image1)
    image2_img = Image.open(image2)
    for i in range(image1_img.size[0]):
        for j in range(image1_img.size[1]):
            if not is_pixel_equal(image1_img, image2_img, i, j):
                return i


# 判断两个像素是否相同

def is_pixel_equal(image1, image2, x, y):
    """
    :param image1:
    :param image2:
    :param x:
    :param y:
    :return:
    """
    pixel1 = image1.load()[x, y]
    pixel2 = image2.load()[x, y]
    threshold = 60
    if abs(pixel1[0] - pixel2[0]) < threshold and abs(pixel1[1] - pixel2[1]) < threshold and abs(
            pixel1[2] - pixel2[2]) < threshold:
        return True
    else:
        return False