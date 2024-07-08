import cv2

def indentify_gap(bg_image, tp_image, out = 'new_image.png'):

    # 读取背景图片和缺口图片
    bg_image = cv2.imread(bg_image)
    tp_image = cv2.imread(tp_image)

    # 识别图片边缘
    bg_edge = cv2.Canny(bg_image, 100, 200)
    tp_edge = cv2.Canny(tp_image, 100, 200)

    # 转换图片格式 --> RGB
    bg_edge = cv2.cvtColor(bg_edge, cv2.COLOR_GRAY2RGB)
    tp_edge = cv2.cvtColor(tp_edge, cv2.COLOR_GRAY2RGB)

    # 缺口匹配
    result = cv2.matchTemplate(bg_edge, tp_edge, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # 绘制方框
    th, tw = tp_edge.shape[:2]
    tl = max_loc # 获取左上角坐标
    br = (tl[0] + tw, tl[1] + th) # 获取右下角坐标
    cv2.rectangle(bg_image, tl, br, (0, 0, 255), 2) # 绘制方框
    cv2.imwrite(out, bg_image) # 保存图片

    # 返回缺口坐标X
    return tl[0]

left = indentify_gap('bg.png', 'tp.png')
print(left)


