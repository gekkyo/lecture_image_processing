# 課題１レポート

## 標本化間隔と空間解像度

画像をダウンサンプリングして（標本化間隔を大きくして）表示せよ.

## 使用画像

標準画像「original.png」を原画像とする.  
この画像は縦600px, 横800pxのディジタルカラー画像である.  
以下図1に原画像を示す.

![原画像](https://raw.githubusercontent.com/gekkyo/lecture_image_processing/master/kadai_01/resource/original.png)  
図1 原画像

## プログラム説明

### インポート部

以下の部分にて, 画像処理に必要な「openCV」のライブラリを読み込んでいる.

```
import cv2
```

また, 以下の部分にて「matplotlib」を読み込んでいる.  
このライブラリは, 処理した画像を画面にプロットするために使用している.

```
from matplotlib import pyplot as plt
```

### メイン処理

まず, 以下の部分で原画像を読み込んでいる.

```
img = cv2.imread('resource/original.png')
```

きちんと読み込めたかどうか確認するため, 以下の部分で読み込んだ原画像を画面にプロットした. プロットの処理に関しては, 関数「image_show()」に処理をまとめている. 詳しくは「画面表示処理」の部分を参照のこと.

```
image_show(img)
input("Displaying original image. Hit Enter.\n")
```

表示した結果を図2に示す.

![原画像](https://raw.githubusercontent.com/gekkyo/lecture_image_processing/master/kadai_01/resource/orig.jpg)  
図2 原画像

原画像を1/2サンプリングするには, 画像を1/2倍に縮小した後, 2倍に拡大すればよい.  
リサイズする際には，単純補間するために「INTER_NEAREST」オプションを使用した.

```
img = cv2.resize(img, (0,0), fx=0.5, fy=0.5, interpolation=cv2.INTER_NEAREST)
img2 = cv2.resize(img, (0,0), fx=2, fy=2, interpolation=cv2.INTER_NEAREST)
```

1/2サンプリングの結果を図3に示す.

![原画像](https://raw.githubusercontent.com/gekkyo/lecture_image_processing/master/kadai_01/resource/img2.jpg)  
図3 1/2サンプリング

同様に原画像を1/4サンプリングするには, 画像を更に1/2倍に縮小した後，4倍に拡大すればよい．すなわち以下のようにする.

```
img = cv2.resize(img, (0,0), fx=0.5, fy=0.5, interpolation=cv2.INTER_NEAREST)
img2 = cv2.resize(img, (0,0), fx=4, fy=4, interpolation=cv2.INTER_NEAREST)
```

1/4サンプリングの結果を図4に示す.

![原画像](https://raw.githubusercontent.com/gekkyo/lecture_image_processing/master/kadai_01/resource/img4.jpg)  
図4 1/4サンプリング

1/8から1/32サンプリングについても, 同様の処理を繰り返せばよい.  
サンプリングの結果を図5～7に示す．

![原画像](https://raw.githubusercontent.com/gekkyo/lecture_image_processing/master/kadai_01/resource/img8.jpg)  
図5 1/8サンプリング

![原画像](https://raw.githubusercontent.com/gekkyo/lecture_image_processing/master/kadai_01/resource/img16.jpg)  
図6 1/16サンプリング

![原画像](https://raw.githubusercontent.com/gekkyo/lecture_image_processing/master/kadai_01/resource/img32.jpg)  
図7 1/32サンプリング

### 画面表示処理

画像を画面にプロットするために, 以下の関数を作成した.

```
def image_show(orig_img):
    # 解像度
    resolution = 72
    # OpenCVではBGR形式で管理されているのでRGBに変換
    tmp_img = cv2.cvtColor(orig_img, cv2.COLOR_BGR2RGB)
    # 画像を表示
    plt.figure(figsize=(tmp_img.shape[1] / resolution, tmp_img.shape[0] / resolution), dpi=resolution)
    plt.imshow(tmp_img)
    plt.show()
```

この関数では, openCVの画像を引数として渡すことにより, その画像をmatplotlibを使用して表示する処理をしている.  

openCVでは, BGRの形式で画像を保持しているので, まず以下の部分でRGB形式に変換する.

```
tmp_img = cv2.cvtColor(orig_img, cv2.COLOR_BGR2RGB)
```

以降の部分は, matplotlibを利用し, 画像を画面に表示する処理である.  
表示サイズをピクセル等倍にするため, まず以下の部分でfigureの設定をする.

```
plt.figure(figsize=(tmp_img.shape[1] / resolution, tmp_img.shape[0] / resolution), dpi=resolution)
```

matplotlibでは, 表示サイズはインチで指定する必要があるため, 取得した原画像のピクセルサイズを解像度で割ることで表示サイズをピクセル等倍とした.  

以下の部分で, 最終的に画面に表示させている.

```
plt.imshow(tmp_img)
plt.show()
```

## 考察

このようにサンプリング幅が大きくなると，モザイク状のサンプリング歪みが発生する．
