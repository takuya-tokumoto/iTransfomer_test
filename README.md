# 複数時系列データ × Transformerの実装と評価

- [参照記事](https://zenn.dev/shungo_a/articles/1ae7e8c68b1cbb)

## セットアップ
### xx


## iTransformerの特徴
### 既存手法では各時刻の値でトークン化していたが時系列データ全体をトークン化するように変更
- 時系列データ全体で考えた時に本来あるはずだった相関を上手く捉えることができない状態で学習がなされていたが、iTransformerではこの課題を解決するために、時系列データ全体をトークン化することで、精度を向上させています。[参考画像1](https://storage.googleapis.com/zenn-user-upload/35625fcb1926-20231106.png)  
- また、クエリとキーで類似性を算出する際に、既存手法では時系列データに対する相関を組み込めていなかったが、時系列データ全体をトークン化することで変数間の相関を出力できるようになった。[参考画像2](https://storage.googleapis.com/zenn-user-upload/d8b9a1d88dcd-20231107.png)
