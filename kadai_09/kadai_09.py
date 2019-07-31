# 課題９ メディアンフィルタと先鋭化
# メディアンフィルターを適用し，ノイズ除去を体験せよ.

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


# ノイズ追加
def add_noise(src):

    # 行数とチャンネル数記憶
    row, ch = src.shape
    # 0〜255までのランダムな値を持った配列作成
    gauss = np.random.randint(256, size=(row,ch))
    # 作成した配列の値を2値化
    gauss = (gauss > 235) * 255
    # 配列の構造をsrcの構造に揃える
    gauss = gauss.reshape(row,ch)
    # 元画像と生成したノイズを足し合わせる
    noisy = gauss + src
    # 値を 0〜255 に収める
    noisy = np.clip(noisy, 0, 255)

    return noisy


# --------------------------------------------
# 処理
# --------------------------------------------

# ファイルから画像を読み込み
src_img = cv2.imread('resource/original.png')
gray_img = cv2.cvtColor(src_img, cv2.COLOR_BGR2GRAY)

# グレー画像を表示して待機
image_show(gray_img)
input("Displaying gray image. Hit Enter.\n")

# ノイズを加える
# 画像をコピー
post_img = gray_img.copy()
# ノイズ追加
noise_img = add_noise(post_img)
# 画像を表示して待機
image_show(noise_img)
input("Displaying noise image. Hit Enter.\n")

# 平滑化フィルタ
# 画像をコピー
post_img = noise_img.copy()
# フィルタ適用
post_img = cv2.blur(post_img,(3,3))
# 画像を表示して待機
image_show(post_img)
input("Displaying blur image. Hit Enter.\n")

# メディアンフィルタ
# 画像をコピー
post_img = noise_img.copy()
# フィルタ適用
post_img = cv2.medianBlur(np.float32(post_img), 3)
# 画像を表示して待機
image_show(post_img)
input("Displaying median blur image. Hit Enter.\n")


# プログラム終了
quit()
