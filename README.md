# Flask API Sample
## 概要
- FlaskのWEB APIサンプルアプリケーション
- DatabaseはSqlite (in-memory) を利用

## usage
### 実行
```bash
$ pipenv install
$ pipenv run python main.py
```

### データベース初期化
- テーブル削除
- テーブル作成
- 初期データ登録

```bash
$ curl -X GET http://0.0.0.0:5000/app/init
```

### CURD
```bash
# データ登録
$ curl -X POST http://0.0.0.0:5000/app/records/new -H "Content-Type: application/json" -d '[{"user_id":"test", "dept_no":"01", "user_name":"test"},{"user_id":"test", "dept_no":"01", "user_name":"test"}]'

# データ全件取得
$ curl -X GET http://0.0.0.0:5000/app/records

# 特定データ取得
$ curl -X GET http://0.0.0.0:5000/app/records/<user_id>

# データ削除
$ curl -X DELETE http://0.0.0.0:5000/app/records/<user_id>
```
