import matplotlib.pyplot as plt
from matplotlib import image
from PIL import Image
import os

path_folder = 'E:/NoveltyDetection/NoveltyDetection/signalTest/dji_ph4/Spectrogramm/'
img_names = os.listdir(path_folder)
ann = []

for img_name in img_names:
    fig, ax = plt.subplots()
    path_img = path_folder + img_name
    ax.imshow(Image.open(path_img))
    ann_img = [0, 0]
    ann.append(img_name)
    # f = open("annotation.txt", "w")
    # f.write(img_name + '\n')
    # f.close()
    def onclick(event):
        print(img_name)
        # print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
        #        ('double' if event.dblclick else 'single', event.button,
        #         event.x, event.y, event.xdata, event.ydata))
        # print(event.y)
        ann.append(event.ydata)
        # f = open("annotation.txt", "w")
        # f.write(str(event.y) + '\n')
        # f.close()
    cid = fig.canvas.mpl_connect('button_press_event', onclick)

    plt.show()
    print(len(ann))

with open("annotation1.txt", "w") as file:
    for line in ann:
        file.write(str(line) + '\n')