# 課題2 階調数と疑似輪郭

２階調，４階調，８階調の画像を生成せよ.

## 使用画像

標準画像「original.png」を原画像とする.

この画像は縦600px, 横800pxのディジタルカラー画像である.

以下図1に原画像を示す.

![原画像](https://raw.githubusercontent.com/gekkyo/lecture_image_processing/master/kadai_02/resource/original.png)

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

![原画像](https://raw.githubusercontent.com/gekkyo/lecture_image_processing/master/kadai_02/resource/gray.jpg)

図2 グレースケール画像

### 2階調化処理

2階調化するには, 画像のそれぞれのピクセルの輝度値を, 一定のしきい値を境に, 「0」か「255」の値にすればよい.

以下の部分でグレースケールの画像のコピーを作成し, しきい値として「128」を用い, 輝度値を調整した.

```python
post_img = gray_img.copy()
post_img = (post_img > 128) * 255
```

2階調化した結果を図3に示す.

![原画像](https://raw.githubusercontent.com/gekkyo/lecture_image_processing/master/kadai_02/resource/img2.jpg)

図3 2階調化

### 多階調化処理

4階調化するには, 複数のしきい値を定め, それぞれの範囲で決まった輝度値に変換すればよい.

以下の部分では, しきい値を複数定めるために配列を用意し, それぞれに対応する輝度値を定め, 画像のピクセルに反映している.

```python
look_up_table = np.ones((256, 1), dtype='uint8') * 0

for i in range(256):
    if i < 64:
        look_up_table[i][0] = 0
    elif i < 128:
        look_up_table[i][0] = 85
    elif i < 192:
        look_up_table[i][0] = 170
    else:
        look_up_table[i][0] = 255

post_img = cv2.LUT(post_img, look_up_table)
```

4階調化した結果を図4に示す.

![原画像](https://raw.githubusercontent.com/gekkyo/lecture_image_processing/master/kadai_02/resource/img4.jpg)

図4 4階調化

同様に8階調化した結果を図5に示す．

![原画像](https://raw.githubusercontent.com/gekkyo/lecture_image_processing/master/kadai_02/resource/img8.jpg)

図5 8階調化

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

2階調化は単純な処理で書くことができたが, それ以上の階調化をするためには一工夫必要であった. openCVでは階調化(ポスタリゼーション)を簡単に実現できる関数が用意されていないため, ルックアップテーブルを作り, 範囲ごとに輝度値を割り当てる方法で実現することができた.

生成した画像では, 色数を制限することにより, 疑似輪郭が表れるのが確認できた. よりグラデーション部分を表現したい場合はディザリングなどの処理をするのが良いと感じるが, 疑似輪郭が現れている画像では, イラスト風の見た目になるため, 用途によっては, あえてポスタリゼーションをかけた画像を使用する場合も考えられる.
