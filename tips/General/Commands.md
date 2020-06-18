# Tips for Commands

## 解凍
| 形式 | 詳細情報 | コマンド |
| ---- | -------- | -------- |
| zip | [link](https://www.atmarkit.co.jp/ait/articles/1607/26/news014.html) | `unzip .zip` |
| tar.gz | - | `tar -zxvf .tar.gz` |

## chmod
- `-R`オプションでディレクトリ以下の全てのファイルやディレクトリの権限を変更できる(参考：[ファイルやディレクトリのパーミッションを一括で置換したい - Qiita](https://qiita.com/takeshi81/items/48ea62eae2fc7f1cb2f0))
```bash
chmod -R 755 /path/to/dir
```
- ディレクトリと実行ファイルを755に、それ以外を644とする(参考：[ファイルやディレクトリのパーミッションを一括で置換したい - Qiita](https://qiita.com/takeshi81/items/48ea62eae2fc7f1cb2f0))
```bash
chmod -R a=rX,u+w path/to/dir
```