# 課題２　階調数と疑似輪郭
# ２階調，４階調，８階調の画像を生成せよ.

# --------------------------------------------
# インポート
# --------------------------------------------

# OpenCV 読み込み
import cv2
# Numpy 読み込み
import numpy as np
# MatPlotLib 読み込み
from matplotlib import pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

# --------------------------------------------
# 関数
# --------------------------------------------

# OpenCVのグレースケール画像をMatplotlibで表示する
def image_show(orig_img):
    # 解像度
    resolution = 72
    # figure作成
    fig = plt.figure(figsize=(orig_img.shape[1] / resolution, orig_img.shape[0] / resolution), dpi=resolution)
    # figure内にaxis追加
    ax = plt.subplot(111)
    # axisに画像を表示する
    im = ax.imshow(orig_img, cmap="gray")
    # axisに図を追加できるように
    divider = make_axes_locatable(ax)
    # axisの右に、2％の大きさの図を0.1インチの隙間を空けて生成
    cax = divider.append_axes("right", size="2%", pad=0.1)
    # 作成した部分にカラーバーを生成
    fig.colorbar(im, cax=cax, orientation='vertical')
    plt.show()


# --------------------------------------------
# 処理
# --------------------------------------------

# ファイルから画像を読み込み
src_img = cv2.imread('resource/original.png')
gray_img = cv2.cvtColor(src_img, cv2.COLOR_BGR2GRAY)

# グレー画像を表示して待機
image_show(gray_img)
input("Displaying gray image. Hit Enter.\n")

# 2階調化
# 変換後の画像
post_img = gray_img.copy()
# 2階調化
post_img = (post_img > 128) * 255
# 画像を表示して待機
image_show(post_img)
input("Displaying 2 color image. Hit Enter.\n")

# 4階調化
# 変換後の画像
post_img = gray_img.copy()
# ルックアップテーブル
look_up_table = np.ones((256, 1), dtype='uint8') * 0
for i in range(256):
    if i < 64:
        look_up_table[i][0] = 0
    elif i < 128:
        look_up_table[i][0] = 85
    elif i < 192:
        look_up_table[i][0] = 170
    else:
        look_up_table[i][0] = 255
# 4階調化
post_img = cv2.LUT(post_img, look_up_table)
# 画像を表示して待機
image_show(post_img)
input("Displaying 4 color image. Hit Enter.\n")

# 8階調化
# 変換後の画像
post_img = gray_img.copy()
# ルックアップテーブル
look_up_table = np.ones((256, 1), dtype='uint8') * 0
for i in range(256):
    if i < 32:
        look_up_table[i][0] = 0
    elif i < 63:
        look_up_table[i][0] = 36
    elif i < 96:
        look_up_table[i][0] = 72
    elif i < 128:
        look_up_table[i][0] = 109
    elif i < 159:
        look_up_table[i][0] = 146
    elif i < 191:
        look_up_table[i][0] = 182
    elif i < 223:
        look_up_table[i][0] = 218
    else:
        look_up_table[i][0] = 255
# 8階調化
post_img = cv2.LUT(post_img, look_up_table)
# 画像を表示して待機
image_show(post_img)
input("Displaying 8 color image. Hit Enter.\n")


# プログラム終了
quit()
