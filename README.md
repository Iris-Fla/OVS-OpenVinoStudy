# OpenVinoを使ってローカルでAIを動かしてみよう！
<img src="https://img.shields.io/badge/-Python3.10-FAEB7E.svg?logo=python&style=for-the-badge">
<img src="https://img.shields.io/badge/-OpenVino-6F51A1.svg?logo=intel&style=for-the-badge">

## 記事に掲載されました
窓の杜にてコンテストの概要やアプリケーションについて取り上げられました✨
[Link](https://forest.watch.impress.co.jp/docs/special/1598339.html)

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

## IntelOpenVinoに対応しているか確認する方法
check.pyを動かしてInfo:GPUにAvailable_Devicesが1以上あることを確認してください。
