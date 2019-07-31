# 課題６　画像の二値化
# 画像を二値化せよ.

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


# 値を 0 <= v <= 255 に収める
def minmax(v):
    v = min(255, v)
    v = max(0, v)
    return v


# Floyd–Steinbergのアルゴリズムでディザリング
def dithering_gray(inMat):

    # 画像サイズ
    h = inMat.shape[0]
    w = inMat.shape[1]

    # 画像を走査
    for y in range(0, h - 1):
        for x in range(1, w - 1):

            # 現在のピクセルを2値化
            old_p = inMat[y, x]
            new_p = np.round(old_p / 255.0) * 255
            inMat[y, x] = new_p

            # 差分を計算
            quant_error_p = old_p - new_p

            # 近傍ピクセルの値を変更
            inMat[y, x + 1] = minmax(inMat[y, x + 1] + quant_error_p * 7 / 16.0)
            inMat[y + 1, x - 1] = minmax(inMat[y + 1, x - 1] + quant_error_p * 3 / 16.0)
            inMat[y + 1, x] = minmax(inMat[y + 1, x] + quant_error_p * 5 / 16.0)
            inMat[y + 1, x + 1] = minmax(inMat[y + 1, x + 1] + quant_error_p * 1 / 16.0)

    return inMat


# --------------------------------------------
# 処理
# --------------------------------------------

# ファイルから画像を読み込み
src_img = cv2.imread('resource/original.png')
gray_img = cv2.cvtColor(src_img, cv2.COLOR_BGR2GRAY)

# グレー画像を表示して待機
image_show(gray_img)
input("Displaying gray image. Hit Enter.\n")

# 通常2値化
# 画像をコピー
post_img = gray_img.copy()
# しきい値128による2階調化
post_img = (post_img > 128) * 255
# 画像を表示して待機
image_show(post_img)
input("Displaying 2 color image. Hit Enter.\n")

# ディザリング
# 画像をコピー
post_img = gray_img.copy()
# ディザリング処理
post_img = dithering_gray(post_img)
# 画像を表示して待機
image_show(post_img)
input("Displaying dithered image. Hit Enter.\n")


# プログラム終了
quit()
