# 課題6 画像のディザリング

画像をディザ法にて二値化せよ.

## 使用画像

標準画像「original.png」を原画像とする.

この画像は縦600px, 横800pxのディジタルカラー画像である.

以下図1に原画像を示す.

![原画像](https://raw.githubusercontent.com/gekkyo/lecture_image_processing/master/kadai_06/resource/original.png)

図1 原画像

## プログラム説明

### インポート

以下の部分にて, 画像処理に必要な「openCV」のライブラリを読み込んでいる.

```python
import cv2
```

以下の部分では, 配列操作に使用するため「numpy」のライブラリを読み込んでいる.

```python
import numpy as np
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

![原画像](https://raw.githubusercontent.com/gekkyo/lecture_image_processing/master/kadai_06/resource/gray.jpg)

図2 グレースケール画像

### 通常の2値化処理

まず比較元になる画像を作成するため, 以下の部分で通常の2値化画像を表示している.

```python
post_img = (post_img > 128) * 255
image_show(post_img)
input("Displaying 2 color image. Hit Enter.\n")
```

表示した結果を図3に示す.

![原画像](https://raw.githubusercontent.com/gekkyo/lecture_image_processing/master/kadai_06/resource/img2.jpg)

図3 通常の2値化

### ディザ法の処理

次にディザ法を用いた処理をする. openCVには, ディザリングを計算してくれる関数は存在しないため, 自前で実装する.

処理が長くなるため, 「dithering_gray()」関数を作成し, 呼び出す形とした.

```python
post_img = dithering_gray(post_img)
```

この関数は, グレースケールのopenCV画像を引数にとり, ディザ法にて変換した画像を返す関数である.

実際の関数は以下となる.

```python
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
```

関数の内部を順に説明してゆく.

まず以下の部分では, 画像のサイズを変数に格納した.

```python
h = inMat.shape[0]
w = inMat.shape[1]
```

求めた画像サイズを元に, 画像の画素すべてについてループ内で調べてゆく.

```python
for y in range(0, h - 1):
    for x in range(1, w - 1):
```

ループ内ではまず以下の部分で, 現在の着目ピクセルにおいて, 2値化処理を行っている.

```python
old_p = inMat[y, x]
new_p = np.round(old_p / 255.0) * 255
inMat[y, x] = new_p
```

そして2値化前の値との差分を計算する.

```python
quant_error_p = old_p - new_p
```

求めた量子化誤差を, 着目ピクセルより後ろに位置する近傍のピクセルに配分してゆく. この方法は, ディザ法の中でも「フロイド-スタインバーグ」のアルゴリズムと呼ばれ, 以下のルールを用いて量子化誤差を分配する.

![img](https://raw.githubusercontent.com/gekkyo/lecture_image_processing/master/kadai_06/resource/equation.gif)

ここで「\*」は現在注目している画素を指す.

具体的なコードは以下となる.

```python
inMat[y, x + 1] = minmax(inMat[y, x + 1] + quant_error_p * 7 / 16.0)
inMat[y + 1, x - 1] = minmax(inMat[y + 1, x - 1] + quant_error_p * 3 / 16.0)
inMat[y + 1, x] = minmax(inMat[y + 1, x] + quant_error_p * 5 / 16.0)
inMat[y + 1, x + 1] = minmax(inMat[y + 1, x + 1] + quant_error_p * 1 / 16.0)
```

画素の値を0〜255の間に収めるため, 以下の「minmax()」関数も用意した.

```python
def minmax(v):
    v = min(255, v)
    v = max(0, v)
    return v
```

以上のアルゴリズムを用いて2階調化した結果を図4に示す.

![原画像](https://raw.githubusercontent.com/gekkyo/lecture_image_processing/master/kadai_06/resource/dither.jpg)

図4 ディザ法による2階調化

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

ディザリング処理を施すことで, 単純な2階調化の画像に比べ, かなり元のグレースケール画像に近い2階調の画像を得ることができた.  特に変化のゆるやかなグラデーションがある部分では, 単純な2階調化では白か黒で塗りつぶされた状態になってしまうが, ディザリング処理をすることで, 比較的元の画像を再現することが可能になっている.

今回はディザリングのアルゴリズムとして「フロイド-スタインバーグ」のアルゴリズムを使用したが, 他にも様々なアルゴリズムが存在する. 今後の課題として, それら別のアルゴリズムについても試してみたいと思う. また, 今回の実装方法では, 処理にかなり時間がかかってしまっている. その点についても, より高速に処理をさせる実装方法を, 今後検討してみたいと思う.
