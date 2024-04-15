# 異常検知データセットでmetric learningを試す

- [qiitaでの紹介記事](https://qiita.com/takuya66520126/private/ddb271b57b098dcfe81b)

## セットアップ
### dockerをインストール
#### docker desktopをインストールする場合
- [ここ](https://docs.docker.com/desktop/)などを参考にdocker desktopをインストール

#### CLIでインストールする場合
- ec2でubuntuインスタンスを立ち上げた場合などを想定
```shell
sudo apt-get update
sudo apt-get install docker.io
sudo gpasswd -a {ユーザ名:ubuntu} docker
docker --version #表示されればセットアップ完了
exit #gpasswdでユーザを付与した後に再ログイン必要
```

### git clone
```shell
git clone https://github.com/takuya-tokumoto/deep-metric-fraud-detector.git
cd deep-metric-fraud-detector
```

### dorkerの起動して環境構築
```shell
./build.sh
./run.sh #windows環境の場合は run_for_win.sh を実行
```

### jupyterlabへアクセス
- ローカルPCで立ち上げた場合はブラウザから`locathost:8888`
- EC2の場合はブラウザから`{パブリック IPv4 DNS}:8888`

### データの準備
- `./tmp/`配下に[zipファイル](https://adfi.jp/download/)を格納
- `sh unzip_files.sh`

### 備考
- 実行環境
  - EC2(AMI:Deep Learning Base GPU AMI, instancetype:d4dn.2xlarge, EBS:150GB)
