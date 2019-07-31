# 課題８ ラベリング
# 二値化された画像の連結成分にラベルをつけよ.

# --------------------------------------------
# インポート
# --------------------------------------------

# OpenCV 読み込み
import cv2
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

# OpenCVのカラー画像をMatplotlibで表示する
def color_image_show(orig_img):
    # 解像度
    resolution = 72
    # figure作成
    fig = plt.figure(figsize=(orig_img.shape[1] / resolution, orig_img.shape[0] / resolution), dpi=resolution)
    # figure内にaxis追加
    ax = plt.subplot(111)
    # axisに画像を表示する
    im = ax.imshow(orig_img)
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

# 通常2値化
# 画像をコピー
post_img = gray_img.copy()
# しきい値128による2階調化
ret, post_img = cv2.threshold(post_img,128,255,cv2.THRESH_BINARY)
# 画像を表示して待機
image_show(post_img)
input("Displaying 2 color image. Hit Enter.\n")

# 連結成分のラベリングを行う。
retval, labels, stats, centroids = cv2.connectedComponentsWithStats(post_img, connectivity=4, ltype=cv2.CV_32S)
# ラベルを表示して待機
color_image_show(labels)
input("Displaying label image. Hit Enter.\n")


# プログラム終了
quit()
