# gmusic-uploader

指定のディレクトリを監視して、ファイルが作成されたら[Google Play Music](https://music.google.com/)にアップロードします

ファイルをアップロードしたらSlackに通知します。

## 対象バージョン

Python 2.7.x

## 使い方

```
$ pip install -r requirements.txt

#認証用ファイルを作成する
$ python make_creadentials.py

#表示されたURLにアクセスして認証後に表示される文字を貼り付ける

#設定ファイルを編集
$ cp config.py.org config.py
$ vi config.py 

#実行
$ python watcher.py
```