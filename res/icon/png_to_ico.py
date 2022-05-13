import os
from PIL import Image

# 获取目录下文件名
files = os.listdir()
# 图标大小
size = (256, 256)

for inName in files:
    # 分离文件名与扩展名
    tmp = os.path.splitext(inName)
    # 因为python文件跟图片在同目录，所以需要判断一下
    if tmp[1] == '.png':
        outName = tmp[0] + '.ico'
        # 打开图片并设置大小
        im = Image.open(inName).resize(size)
        try:
            # 图标文件保存
            im.save(outName)

            print('{} --> {}'.format(inName, outName))
        except IOError:
            print('connot convert :', inName)
