# 複数時系列データ × Transformerの実装と評価

- [参照記事](https://zenn.dev/shungo_a/articles/1ae7e8c68b1cbb)

## 仮想環境作成
Anacondaのパスを通し、condaコマンドが利用可能か確認する。  
以下のコマンドで仮想環境を作成する。  
```shell
conda create -n {環境名} python=3.10
```
仮想環境を起動する  
```shell
conda activate {環境名}
```
ライブラリをインストール  
- `scripts/iTransformer.ipynb` を実行する場合
```shell
pip install -r require_itrans.txt --user
```
- `scripts/Prophet.ipynb` を実行する場合
```shell
pip install -r require_prophet.txt --user
```

## iTransformerの特徴
- <b>既存手法では各時刻の値でトークン化</b>していたが<b>時系列データ全体をトークン化するように変更</b>
- 従来のTransformerモデルでは、時系列データ全体で考えた時に相関関係を上手く捉えることができない状態で学習がなされていたが、iTransformerでは、<b>時系列データ全体をトークン化することで、相関が考慮可能。</b>[参考画像1](https://storage.googleapis.com/zenn-user-upload/35625fcb1926-20231106.png)  
- また、クエリとキーで類似性を算出する際に、既存手法では時系列データに対する相関を組み込めていなかったが、<b>時系列データ全体をトークン化することで変数間の相関を出力できるようになった。</b>[参考画像2](https://storage.googleapis.com/zenn-user-upload/d8b9a1d88dcd-20231107.png)
