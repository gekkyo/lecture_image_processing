# 課題５　判別分析法
# 判別分析法を用いて画像二値化せよ.

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


# 判別分析法でしきい値を求める
def get_otsu_threshold(img):

    # ヒストグラム計算
    hist = cv2.calcHist([img], [0], None, [256], [0, 256])
    # 配列を整形
    hist = hist[:, 0]

    # 濃度の合計
    sum_all = 0.0
    # 画素数の合計
    n_all = 0.0
    for i in range(0, len(hist)):
        n_all += hist[i]
        sum_all += i * hist[i]
    # 全画素の濃度の合計
    myu_t = sum_all / n_all

    # 判別比
    max_val = 0.0;
    # 求めるしきい値
    max_thres = 1;

    for i in range(0, 256):
        # クラスごとの画素数
        n1 = n2 = 0.0
        # クラスごとの濃度合計
        sum1 = sum2 = 0.0
        # クラスごとの濃度平均
        myu1 = myu2 = 0.0
        # クラスごとの偏差合計
        hensa1 = hensa2 = 0.0

        # ヒストグラムを2つのクラスに分ける
        for j in range(0, i):
            n1 += hist[j]
            sum1 += j * hist[j]

        for k in range(i, 256):
            n2 += hist[k]
            sum2 += k * hist[k]

        # 0除算を防ぐ
        if n1 == 0 or n2 == 0:
            continue

        # クラスごとの濃度平均の算出
        myu1 = sum1 / n1
        myu2 = sum2 / n2

        # クラスごとの偏差の算出
        for j in range(0, i):
            hensa1 += ((j - myu1) ** 2) * hist[j]

        for k in range(i, 256):
            hensa2 += ((k - myu2) ** 2) * hist[k]

        # クラスごとの分散の算出
        sigma1 = hensa1 / n1
        sigma2 = hensa2 / n2

        # クラス内分散
        sigma_w = (n1 * sigma1 + n2 * sigma2) / (n1 + n2)
        # クラス間分散
        sigma_B = (n1 * ((myu1 - myu_t) ** 2) + n2 * ((myu2 - myu_t) ** 2)) / (n1 + n2)

        if max_val < sigma_B / sigma_w:
            max_val = sigma_B / sigma_w
            max_thres = i

    return max_thres


# --------------------------------------------
# 処理
# --------------------------------------------

# ファイルから画像を読み込み
src_img = cv2.imread('resource/original.png')
gray_img = cv2.cvtColor(src_img, cv2.COLOR_BGR2GRAY)

# グレー画像を表示して待機
image_show(gray_img)
input("Displaying gray image. Hit Enter.\n")

# 判別分析法
# 画像をコピー
post_img = gray_img.copy()
# しきい値を計算
thresh = get_otsu_threshold(post_img)
# 2階調化
post_img = (post_img > thresh) * 255
# 画像を表示して待機
image_show(post_img)
input("Displaying 2 color image. Hit Enter.\n")


# プログラム終了
quit()
