# 課題9 メディアンフィルタと先鋭化

メディアンフィルターを適用し，ノイズ除去を体験せよ.

## 使用画像

標準画像「original.png」を原画像とする.

この画像は縦600px, 横800pxのディジタルカラー画像である.

以下図1に原画像を示す.

![原画像](https://raw.githubusercontent.com/gekkyo/lecture_image_processing/master/kadai_09/resource/original.png)

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

![原画像](https://raw.githubusercontent.com/gekkyo/lecture_image_processing/master/kadai_09/resource/gray.jpg)

図2 グレースケール画像

### ノイズ追加

まずノイズを加える処理をするため, 「add_noise()」関数を作成し, 以下の処理をした.

```python
noise_img = add_noise(post_img)
```

実際の「add_noise()」関数は以下となる.

```python
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
```

この関数は, グレースケールのopenCV画像を引数に取り, ノイズを加えた画像を返す関数となる.

関数内を順に説明する. まず以下の部分では, 引数で渡された画像の高さと幅を記憶し, 同じ情報量を持った, 0〜255までのランダムな値を持った配列を作成している.

```python
# 行数とチャンネル数記憶
row, ch = src.shape
# 0〜255までのランダムな値を持った配列作成
gauss = np.random.randint(256, size=(row,ch))
```

以下の部分では, 配列の値を0もしくは255に2値化し, 配列の構造をopenCVの画像配列と同じ形式に変形した. ここではしきい値として「235」を使用しているが, これは適度なノイズを実現するため, 何度か試してみた結果採用した値である.

```python
# 作成した配列の値を2値化
gauss = (gauss > 235) * 255
# 配列の構造をsrcの構造に揃える
gauss = gauss.reshape(row,ch)
```

以上でノイズのみの画像が生成できたので, あとは元の画像に足し合わせ, 値を微調整している.

```python
# 元画像と生成したノイズを足し合わせる
noisy = gauss + src
# 値を 0〜255 に収める
noisy = np.clip(noisy, 0, 255)
```

以上のノイズ追加処理を施した結果を図3に示す.

![原画像](https://raw.githubusercontent.com/gekkyo/lecture_image_processing/master/kadai_09/resource/noise.jpg)

図3 ノイズ追加

### 平滑化フィルタ

平滑化するためには, openCVの「blur()」関数を使用すれば良い.

```python
post_img = cv2.blur(post_img,(3,3))
```

平滑化した結果を図4に示す.

![原画像](https://raw.githubusercontent.com/gekkyo/lecture_image_processing/master/kadai_09/resource/blur.jpg)

図4 平滑化

### メディアンフィルタ

メディアンフィルタを使用するためには, openCVの「medianBlur()」関数を使用すれば良い.

```python
post_img = cv2.medianBlur(np.float32(post_img), 3)
```

メディアンフィルタを適用した結果を図5に示す.

![原画像](https://raw.githubusercontent.com/gekkyo/lecture_image_processing/master/kadai_09/resource/median.jpg)

図5 メディアンフィルタ

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

平滑化フィルタでは, 画像がすこしぼやけてしまい, ノイズ自体もあまり取れていない事がわかるが, メディアンフィルタではきれいにノイズのみが取れていることが確認できた. またメディアンフィルタではエッジがぼやけてしまうこともないので, シャープネスを保ったままノイズが除去できるのはとても有用だと感じた.

いままでは, 画像をぼかした後にシャープネスをかける等の処理をしてノイズを取っていたが, 今後はメディアンフィルタを活用していきたいと思う.
