# 課題10 画像のエッジ抽出
# エッジ抽出を体験せよ.

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

# プレウィット法
# 画像をコピー
post_img = gray_img.copy()
# カーネル
kernel_x = np.array([[1, 0, -1],
                   [1, 0, -1],
                   [1, 0, -1]])
kernel_y = np.array([[1, 1, 1],
                   [0, 0, 0],
                   [-1, -1, -1]])
# フィルタ適用
img_x = cv2.filter2D(post_img, -1, kernel_x)
img_y = cv2.filter2D(post_img, -1, kernel_y)
# 画像を表示して待機
image_show(img_x+img_y)
input("Displaying prewitt image. Hit Enter.\n")


# ソベル法
# 画像をコピー
post_img = gray_img.copy()
# フィルタ適用
img_x = cv2.Sobel(post_img,cv2.CV_8U,1,0,ksize=3)
img_y = cv2.Sobel(post_img,cv2.CV_8U,0,1,ksize=3)
# 画像を表示して待機
image_show(img_x+img_y)
input("Displaying sobel image. Hit Enter.\n")

# キャニー法
# 画像をコピー
post_img = gray_img.copy()
# フィルタ適用
post_img = cv2.Canny(post_img, 100, 200)
# 画像を表示して待機
image_show(post_img)
input("Displaying canny image. Hit Enter.\n")


# プログラム終了
quit()
