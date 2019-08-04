# 課題３　閾値処理
# 閾値を4パターン設定し,閾値処理した画像を示せ.

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
th, post_img = cv2.threshold(post_img,64,255,cv2.THRESH_BINARY)
# 画像を表示して待機
image_show(post_img)
input("Displaying b/w image 1. Hit Enter.\n")

# 2階調化
# 変換後の画像
post_img = gray_img.copy()
# 2階調化
th, post_img = cv2.threshold(post_img,96,255,cv2.THRESH_BINARY)
# 画像を表示して待機
image_show(post_img)
input("Displaying b/w image 2. Hit Enter.\n")

# 2階調化
# 変換後の画像
post_img = gray_img.copy()
# 2階調化
th, post_img = cv2.threshold(post_img,128,255,cv2.THRESH_BINARY)
# 画像を表示して待機
image_show(post_img)
input("Displaying b/w image 3. Hit Enter.\n")

# 2階調化
# 変換後の画像
post_img = gray_img.copy()
# 2階調化
th, post_img = cv2.threshold(post_img,192,255,cv2.THRESH_BINARY)
# 画像を表示して待機
image_show(post_img)
input("Displaying b/w image 4. Hit Enter.\n")


# プログラム終了
quit()
