# 課題5 判別分析法

判別分析法を用いて画像二値化せよ.

## 使用画像

標準画像「original.png」を原画像とする.

この画像は縦600px, 横800pxのディジタルカラー画像である.

以下図1に原画像を示す.

![原画像](https://raw.githubusercontent.com/gekkyo/lecture_image_processing/master/kadai_05/resource/original.png)

図1 原画像

## プログラム説明

### インポート

以下の部分にて, 画像処理に必要な「openCV」のライブラリを読み込んでいる.

```python
import cv2
```

また, 以下の部分にて「matplotlib」を読み込んでいる.

このライブラリは, 処理した画像を画面にプロットするために使用している.

```python
from matplotlib import pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
```

### 画像の読み込み・グレースケール変換

まず, 以下の部分で原画像を読み込んでいる.

```python
src_img = cv2.imread('resource/original.png')
```

読み込んだ画像は, 以下の部分でグレースケールに変換した.

```python
gray_img = cv2.cvtColor(src_img, cv2.COLOR_BGR2GRAY)
```

きちんと変換できたかどうか確認するため, 以下の部分でグレースケールに変換した原画像を画面にプロットした. プロットの処理に関しては, 関数「image_show()」に処理をまとめている. 詳しくは「画面表示処理」の部分を参照のこと.

```python
image_show(gray_img)
input("Displaying gray image. Hit Enter.\n")
```

表示した結果を図2に示す.

![原画像](https://raw.githubusercontent.com/gekkyo/lecture_image_processing/master/kadai_05/resource/gray.jpg)

図2 グレースケール画像

### 判別分析法の処理

実はopenCVの2階調化関数である「threshold()」関数では, 判別分析法のアルゴリズムを簡単に使えるオプションが用意されているのであるが, ここではアルゴリズム勉強のため, 自前で実装してみることにした.

処理が長くなるため, 「get_otsu_threshold()」関数を作成し, 呼び出す形とした.

```python
thresh = get_otsu_threshold(post_img)
```

この関数は, グレースケールのopenCV画像を引数にとり, 判別分析法にて計算されたしきい値を返す関数である.

実際の関数は以下となる.

```python
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
```

関数の内部を順に説明してゆく.

まず以下の部分では, ヒストグラムを計算し, その配列を扱いやすくするため1次元の配列に変換した.

```python
hist = cv2.calcHist([img], [0], None, [256], [0, 256])
hist = hist[:, 0]
```

以下の部分で, 全画素の濃度平均値myu_tを計算している.

```python
# 濃度の合計
sum_all = 0.0
# 画素数の合計
n_all = 0.0
for i in range(0, len(hist)):
    n_all += hist[i]
    sum_all += i * hist[i]
# 全画素の濃度の平均
myu_t = sum_all / n_all
```

以下の部分から, ヒストグラムの配列の要素をループ内で調べてゆく.

```python
for i in range(0, 256):
```

ループ内では, まずいくつか変数を定義した.

```python
# クラスごとの画素数
n1 = n2 = 0.0
# クラスごとの濃度合計
sum1 = sum2 = 0.0
# クラスごとの濃度平均
myu1 = myu2 = 0.0
# クラスごとの偏差合計
hensa1 = hensa2 = 0.0
```

そしてヒストグラムを2つのクラスに分割する.

```python
# ヒストグラムを2つのクラスに分ける
for j in range(0, i):
    n1 += hist[j]
    sum1 += j * hist[j]

for k in range(i, 256):
    n2 += hist[k]
    sum2 += k * hist[k]
```

分割した際に, クラスごとの画素数と, 濃度の合計を計算しておく.

その値を元に, 以下の部分でクラスごとの濃度平均を計算した.

```python
# 0除算を防ぐ
if n1 == 0 or n2 == 0:
  continue

# クラスごとの濃度平均の算出
myu1 = sum1 / n1
myu2 = sum2 / n2
```

また, クラス内分散を求めるためには, クラスごとの分散を求める必要があるため, 以下の部分でそれぞれ計算している.

```python
# クラスごとの偏差の算出
for j in range(0, i):
    hensa1 += ((j - myu1) ** 2) * hist[j]

for k in range(i, 256):
    hensa2 += ((k - myu2) ** 2) * hist[k]

# クラスごとの分散の算出
sigma1 = hensa1 / n1
sigma2 = hensa2 / n2
```

必要な変数の値を求めることができたので, 以下の部分でクラス内分散と, クラス間分散を計算した.

```python
# クラス内分散
sigma_w = (n1 * sigma1 + n2 * sigma2) / (n1 + n2)
# クラス間分散
sigma_B = (n1 * ((myu1 - myu_t) ** 2) + n2 * ((myu2 - myu_t) ** 2)) / (n1 + n2)
```

あとは求めた sigma_B / sigma_w の値を計算し, その値が最大になる際の i の値が求めたいしきい値の値となる.

```python
if max_val < sigma_B / sigma_w:
    max_val = sigma_B / sigma_w
    max_thres = i
```

以上の関数を用いて求めたしきい値を使い, 2階調化した結果を図3に示す.

![原画像](https://raw.githubusercontent.com/gekkyo/lecture_image_processing/master/kadai_05/resource/img2.jpg)

図3 判別分析法による2階調化

### 画面表示処理

画像を画面にプロットするために, 以下の関数を作成した.

```python
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
```

この関数では, openCVのグレースケール画像を引数として渡すことにより, その画像をmatplotlibを使用して表示する処理をしている.

表示サイズをピクセル等倍にするため, まず以下の部分でfigureの設定をする.

```python
fig = plt.figure(figsize=(orig_img.shape[1] / resolution, orig_img.shape[0] / resolution), dpi=resolution)
```

matplotlibでは, 表示サイズはインチで指定する必要があるため, 取得した原画像のピクセルサイズを解像度で割ることで表示サイズをピクセル等倍とした.

また, 画像右にグレースケールのカラーバーを表示させるため, 以下の処理をしている.

```python
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
```

ここではまず先ほど作成したfigure内にプロットを追加し, 画像を配置した.

また, カラーバーを追加できるようにするための処理をし, colorbar()関数にてカラーバーを生成している.

そして以下の部分で, 最終的に生成した画像を表示させている.

```python
plt.show()
```

## 考察

今回使用した画像のように, 比較的前景と背景がきちんと別れている画像では, 判別分析法による2値化が有効であることが確認できた. 髪の毛の部分はほとんど細部が消えてしまっているが, 顔の部分については細かい部分まで表現できている.

ちなみにopenCVの「threshold()」関数にて, 判別分析法のアルゴリズムを使用する場合は, 以下のように記述する.

```python
th, post_img = cv2.threshold(post_img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
```

「th」には求めたしきい値が, また「post_img」には変換後の画像が格納される形になる.

あらかじめ用意されている関数を利用したほうが高速に, かつ簡単に実装することができるが, 今回自前で実装することにより, アルゴリズムへの理解がより深まった.
