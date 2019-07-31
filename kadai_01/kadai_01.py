# 課題１　標本化間隔と空間解像度
# 画像をダウンサンプリングして（標本化間隔を大きくして）
# 表示せよ.

# --------------------------------------------
# インポート
# --------------------------------------------

# OpenCV 読み込み
import cv2
# MatPlotLib 読み込み
from matplotlib import pyplot as plt

# --------------------------------------------
# 関数
# --------------------------------------------

# OpenCVの画像をMatplotlibで表示する
def image_show(orig_img):
    # 解像度
    resolution = 72
    # OpenCVではBGR形式で管理されているのでRGBに変換
    tmp_img = cv2.cvtColor(orig_img, cv2.COLOR_BGR2RGB)
    # 画像を表示
    plt.figure(figsize=(tmp_img.shape[1] / resolution, tmp_img.shape[0] / resolution), dpi=resolution)
    plt.imshow(tmp_img)
    plt.show()

# --------------------------------------------
# 処理
# --------------------------------------------

# ファイルから画像を読み込み
img = cv2.imread('resource/original.png')

# 1/2 倍に縮小し元の大きさに戻す
img = cv2.resize(img, (0,0), fx=0.5, fy=0.5, interpolation=cv2.INTER_NEAREST)
img2 = cv2.resize(img, (0,0), fx=2, fy=2, interpolation=cv2.INTER_NEAREST)
# 画像を表示して待機
image_show(img2)
input("Displaying 1/2 size image. Hit Enter.\n")

# 1/2 倍に縮小し元の大きさに戻す
img = cv2.resize(img, (0,0), fx=0.5, fy=0.5, interpolation=cv2.INTER_NEAREST)
img2 = cv2.resize(img, (0,0), fx=4, fy=4, interpolation=cv2.INTER_NEAREST)
# 画像を表示して待機
image_show(img2)
input("Displaying 1/4 size image. Hit Enter.\n")

# 1/2 倍に縮小し元の大きさに戻す
img = cv2.resize(img, (0,0), fx=0.5, fy=0.5, interpolation=cv2.INTER_NEAREST)
img2 = cv2.resize(img, (0,0), fx=8, fy=8, interpolation=cv2.INTER_NEAREST)
# 画像を表示して待機
image_show(img2)
input("Displaying 1/8 size image. Hit Enter.\n")

# 1/2 倍に縮小し元の大きさに戻す
img = cv2.resize(img, (0,0), fx=0.5, fy=0.5, interpolation=cv2.INTER_NEAREST)
img2 = cv2.resize(img, (0,0), fx=16, fy=16, interpolation=cv2.INTER_NEAREST)
# 画像を表示して待機
image_show(img2)
input("Displaying 1/16 size image. Hit Enter.\n")

# 1/2 倍に縮小し元の大きさに戻す
img = cv2.resize(img, (0,0), fx=0.5, fy=0.5, interpolation=cv2.INTER_NEAREST)
img2 = cv2.resize(img, (0,0), fx=32, fy=32, interpolation=cv2.INTER_NEAREST)
# 画像を表示して待機
image_show(img2)
input("Displaying 1/32 size image. Hit Enter.\n")


# プログラム終了
quit()
