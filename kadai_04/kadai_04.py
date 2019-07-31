# 課題４　画像のヒストグラム
# 画素の濃度ヒストグラムを生成せよ.

# --------------------------------------------
# インポート
# --------------------------------------------

# OpenCV 読み込み
import cv2
# MatPlotLib 読み込み
from matplotlib import pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable, get_cmap

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


# ヒストグラムを表示する
def hist_show(img):

    # ヒストグラム計算
    hist = cv2.calcHist([img], [0], None, [256], [0, 256])

    # MatPlotLibで表示
    # figureとaxisを作成
    fig, ax = plt.subplots()
    # axisにプロット
    ax.plot(hist)
    # x軸の最小最大を指定
    ax.set_xlim(0, 255)
    # グリッド表示
    ax.grid()
    # グレーバーをつけるため、x軸のラベルとメモリを消す
    ax.tick_params(axis='x', labelbottom=False, bottom=False)
    # グレーバー作成のための用意
    norm = Normalize(vmin=0, vmax=255)
    cmap = get_cmap('gray')
    mappable = ScalarMappable(cmap=cmap, norm=norm)
    # axisに図を追加できるように
    divider = make_axes_locatable(ax)
    # axisの下に、5％の大きさの図を隙間を空けずに生成
    cax = divider.append_axes("bottom", size="5%", pad=0)
    # グレーバーを生成
    fig.colorbar( mappable, cax=cax, orientation='horizontal')
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

# ヒストグラム
# 画像をコピー
post_img = gray_img.copy()
# ヒストグラムを表示して待機
hist_show(post_img)
input("Displaying histogram. Hit Enter.\n")


# プログラム終了
quit()
