# 課題10 画像のエッジ抽出

エッジ抽出を体験せよ.

## 使用画像

標準画像「original.png」を原画像とする.

この画像は縦600px, 横800pxのディジタルカラー画像である.

以下図1に原画像を示す.

![原画像](https://raw.githubusercontent.com/gekkyo/lecture_image_processing/master/kadai_10/resource/original.png)

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

![原画像](https://raw.githubusercontent.com/gekkyo/lecture_image_processing/master/kadai_10/resource/gray.jpg)

図2 グレースケール画像

### Prewitt法

まずPrewitt法にて処理をする. Prewitt法を簡単に利用できる関数は用意されていないため, openCVの「filter2D()」関数を使用し, カスタムフィルタを適用する形で実装する.

以下の部分でカスタムフィルタを作成した.

```python
kernel_x = np.array([[1, 0, -1],
                   [1, 0, -1],
                   [1, 0, -1]])
kernel_y = np.array([[1, 1, 1],
                   [0, 0, 0],
                   [-1, -1, -1]])
```

ここでは, Prewitt法のオペレータ値を入れた配列を作成した. そして以下で画像にフィルタを適用し, x方向とy方向にそれぞれ適用した画像を足し合わせたものを表示するようにした.

```python
img_x = cv2.filter2D(post_img, -1, kernel_x)
img_y = cv2.filter2D(post_img, -1, kernel_y)
image_show(img_x+img_y)
```

以上のPrewitt法のフィルタを施した結果を図3に示す.

![原画像](https://raw.githubusercontent.com/gekkyo/lecture_image_processing/master/kadai_10/resource/prewitt.jpg)

図3 Prewitt法

### Sobel法

Sobel法は, openCVの「Sobel()」関数を使用することで簡単に処理ができる.

```python
img_x = cv2.Sobel(post_img,cv2.CV_8U,1,0,ksize=3)
img_y = cv2.Sobel(post_img,cv2.CV_8U,0,1,ksize=3)
```

Sobel法のフィルタを施した結果を図4に示す.

![原画像](https://raw.githubusercontent.com/gekkyo/lecture_image_processing/master/kadai_10/resource/sobel.jpg)

図4 Sobel法

### Canny法

Canny法は, openCVの「Canny()」関数を使用すれば良い.

```python
post_img = cv2.Canny(post_img, 100, 200)
```

Canny法のフィルタを施した結果を図5に示す.

![原画像](https://raw.githubusercontent.com/gekkyo/lecture_image_processing/master/kadai_10/resource/canny.jpg)

図5 Canny法

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

どのアルゴリズムを用いても, エッジがよく検出されていることが確認できた.

Prewitt法とSobel法を比べた場合, 背景の雲などに注目するとSobel法の方がより細かなエッジにも反応していることが確認できる.

またCanny法とそれ以外を比べた場合, Canny法では前景のプロペラのオブジェクトをより正確かつ鮮明に検出できていることが確認できた.

Canny法については, 「Canny()」関数を呼ぶときに2つの数値を渡しているが, これはアルゴリズム内で強いエッジを見つけるために使われるしきい値の値を決める数値である. また, Canny法では複数のステップによってエッジを検出しているが, その中で画素の勾配を計算するためにはSobel法が用いられている. つまりSobel法を応用し, より正確なエッジ検出をできるようにしたアルゴリズムと言える.

今後の課題として, Canny法の詳しいアルゴリズムの処理や, その他のエッジ検出の方法についても学んでみたいと思う.
