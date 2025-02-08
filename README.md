![OVSTUDY](https://github.com/Iris-Fla/OVS-OpenVinoStudy/assets/103801589/20703373-245e-452b-a6fc-d34287f8a3d9)

# OpenVinoを用いた子供向け英単語学習アプリ
<p>
  <img src="https://img.shields.io/badge/-Python3.10-FAEB7E.svg?logo=python&style=for-the-badge">
  <img src="https://img.shields.io/badge/-OpenVino-6F51A1.svg?logo=intel&style=for-the-badge">
</p>

### インテル プレゼンツ OpenVINO ツールキット学生向け AI コンテスト 最優秀賞🎉
窓の杜にてコンテストの概要やアプリケーションについて取り上げられました✨
[Link](https://forest.watch.impress.co.jp/docs/special/1598339.html)

### Intel® AI Global Impact Festival 2024 Country/Region部門 受賞作品🎉
インテルの世界コンテストに提出し、表彰されました。
[Link](https://www.intel.com/content/www/us/en/corporate/artificial-intelligence/winners2024.html#tab-blade-1-1)

## 実行環境

- Python 3.10.11
- Windows 10
- **IntelCore Ultra**

## Venvの入り方
```
py -3.10 -m venv venv
venv\Scripts\Activate.ps1 
pip install -r .\requirements.txt
```

## 起動
clone
```
git clone https://github.com/wenyi5608/GroundingDINO/
git clone https://github.com/yformer/EfficientSAM
git clone https://github.com/IDEA-Research/Grounded-Segment-Anything
```
```
python app.py
```


## IntelOpenVinoに対応しているか確認する方法
check.pyを動かしてInfo:GPUにAvailable_Devicesが1以上あることを確認してください。
