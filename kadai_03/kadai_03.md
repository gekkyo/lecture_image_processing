# 課題3 閾値処理

閾値を4パターン設定し, 閾値処理した画像を示せ.

## 使用画像

標準画像「original.png」を原画像とする.

この画像は縦600px, 横800pxのディジタルカラー画像である.

以下図1に原画像を示す.

![原画像](https://raw.githubusercontent.com/gekkyo/lecture_image_processing/master/kadai_03/resource/original.png)

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

![原画像](https://raw.githubusercontent.com/gekkyo/lecture_image_processing/master/kadai_03/resource/gray.jpg)

図2 グレースケール画像

### 2階調化処理

まず1つめの処理では, しきい値を「64」とした.

今回はopenCVであらかじめ提供されている, 「threshold()」関数を使用し2階調化した.

```python
th, post_img = cv2.threshold(post_img,64,255,cv2.THRESH_BINARY)
```

2階調化した結果を図3に示す.

![原画像](https://raw.githubusercontent.com/gekkyo/lecture_image_processing/master/kadai_03/resource/img64.jpg)

図3 しきい値「64」

同様にしきい値を「96」とした結果を図4に示す.

![原画像](https://raw.githubusercontent.com/gekkyo/lecture_image_processing/master/kadai_03/resource/img96.jpg)

図4 しきい値「96」

同様にしきい値を「128」とした結果を図5に示す.

![原画像](https://raw.githubusercontent.com/gekkyo/lecture_image_processing/master/kadai_03/resource/img128.jpg)

図5 しきい値「128」

同様にしきい値を「192」とした結果を図6に示す.

![原画像](https://raw.githubusercontent.com/gekkyo/lecture_image_processing/master/kadai_03/resource/img192.jpg)

図5 しきい値「192」

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

また, カラーバーを追加できるようにするための処理をし, 「colorbar()」関数にてカラーバーを生成している.

そして以下の部分で, 最終的に生成した画像を表示させている.

```python
plt.show()
```

## 考察

しきい値の違いにより, 2値化後の画像の仕上がりにかなり差があることが確認できた.

今回は単純に1つのしきい値を境に輝度値を「0」と「255」に割り当てる形にするため, 「threshold()」関数のオプションとして「THRESH_BINARY」を指定したが, その他にも以下のようなアルゴリズムを選択することができる.

* THRESH_BINARY_INV
* THRESH_TRUNC
* THRESH_TOZERO
* THRESH_TOZERO_INV
* ADAPTIVE_THRESH_MEAN_C
* ADAPTIVE_THRESH_GAUSSIAN_C
* THRESH_OTSU

「THRESH_TRUNC」「THRESH_TOZERO」に関しては, ある値までは現画像の値を使用し, しきい値を超えると輝度値を「0」にしたり, その逆を行う処理となる.

「ADAPTIVE_THRESH〜」に関しては, 適応的しきい値処理となり, 画像の部分毎に異なるしきい値を割り出し適用するアルゴリズムとなる.

「THRESH_OTSU」に関しては, 課題5の判別分析法を使用した2値化アルゴリズムとなる.

今後の課題として, より詳しく2値化のアルゴリズムや特徴を学んでみたいと思う.
