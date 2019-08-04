# 課題7 ダイナミックレンジの拡大

画素のダイナミックレンジを０から２５５にせよ.

## 使用画像

標準画像「original.png」を原画像とする.

この画像は縦600px, 横800pxのディジタルカラー画像である.

以下図1に原画像を示す.

![原画像](https://raw.githubusercontent.com/gekkyo/lecture_image_processing/master/kadai_07/resource/original.png)

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
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable, get_cmap
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

![原画像](https://raw.githubusercontent.com/gekkyo/lecture_image_processing/master/kadai_07/resource/gray.jpg)

図2 グレースケール画像

### ヒストグラム

ヒストグラムの作成と表示は以下の部分で処理をしている.

処理が複雑になったため, 関数を作成し呼び出す形とした.

```python
hist_show(post_img)
```

実際の関数は以下となる. 引数としてグレースケールのopenCV画像を取り, ヒストグラムを表示する処理となる.

```python
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
```

ヒストグラムの計算をしている部分は以下になる.

```python
hist = cv2.calcHist([img], [0], None, [256], [0, 256])
```

ここでは, openCVに用意されている「calcHist()」関数を使用し, ヒストグラムの計算をした.

以降の部分は, matplotlibを使用したグレーバーの追加や, 画面表示の際の調整である.

ヒストグラムを表示した結果を図3に示す.

![原画像](https://raw.githubusercontent.com/gekkyo/lecture_image_processing/master/kadai_07/resource/gray_histogram.jpg)

図3 ヒストグラム

### ダイナミックレンジ拡大

ダイナミックレンジを拡大するために, openCVの「equalizeHist()」関数を使用した. この関数を使用することにより, 画像の明るさを正規化することができる.

```python
post_img = cv2.equalizeHist(post_img)
```

ダイナミックレンジを拡大した結果を図4に示す.

![原画像](https://raw.githubusercontent.com/gekkyo/lecture_image_processing/master/kadai_07/resource/equalized.jpg)

図4 ダイナミックレンジ拡大後

また, ダイナミックレンジ拡大後の画像のヒストグラムを図5に示す.

![原画像](https://raw.githubusercontent.com/gekkyo/lecture_image_processing/master/kadai_07/resource/equalized_histogram.jpg)

図5 ダイナミックレンジ拡大後のヒストグラム

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

ダイナミックレンジを拡大することにより, 白っぽい部分をより白く, 黒っぽい部分をより黒くすることができ, 結果として画像のコントラストを上げることができることが確認できた.

ただ, 図5を見るとグラフがぎざぎざになってしまっているのがわかる. これは図3のグラフの画素数が0以外の中央部を, 横に引き伸ばしたような形になるため, 輝度値にすきまが生じてしまっているためである. このことにより, 図2と図4の画像を比べると, 例えば空の部分に若干の疑似輪郭が生じてしまっていることがわかる.
