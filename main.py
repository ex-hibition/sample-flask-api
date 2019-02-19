from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import csv
import datetime
import os
# import cx_Oracle


# DB接続設定
def init_db():
    # DB(sqlite in-memory)
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
    # DB(oracle)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'oracle+cx_oracle://user:pw@' \
                                            'xxx.xxx.xxx.xxx:9999' \
                                            '/?service_name=DBNAME'
    # デバッグログ
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


app = Flask(__name__)
init_db()
db = SQLAlchemy(app)


# モデル定義
class TargetTable(db.Model):
    # テーブル名
    __tablename__ = "app_sample_table"

    id = db.Column(db.Integer, db.Sequence('app-sample-table_id_seq'), primary_key=True)
    user_id = db.Column(db.String(10))
    dept_no = db.Column(db.String(10))
    user_name = db.Column(db.String(10))
    created_on = db.Column(db.DateTime)
    modified_on = db.Column(db.DateTime)

    def to_dict(self):
        """
        全カラムをdictで返す
        :return:
        """
        return {
            'id': self.id,
            'user_id': self.user_id,
            'dept_no': self.dept_no,
            'user_name': self.user_name,
            'created_on': self.created_on,
            'modified_on': self.modified_on,
        }

    def __repr__(self):
        return "<TargetTable id:{}, user_id:{}>".format(self.id, self.user_id)


# index
@app.route("/")
def index():
    return "it's works.", 200


# テーブル作成
@app.route("/app/init")
def init():
    """created and initialized table."""

    # テーブル削除
    db.drop_all()
    # テーブル生成
    db.create_all()

    # データインポート
    with open(os.path.join(os.path.dirname(__file__), "data", "init_data.csv"), encoding="utf8") as csv_file:
        reader = csv.DictReader(csv_file)
        for rec in reader:
            app.logger.debug(rec)
            obj = TargetTable(
                user_id=rec["user_id"],
                dept_no=rec["dept_no"],
                user_name=rec["user_name"],
                created_on=datetime.datetime.now()
            )
            db.session.add(obj)
        db.session.commit()

    return 'table was deleted and created and initialized.'


# 全データ取得
@app.route("/app/records", methods=['GET', 'POST'])
def records():
    target_list = TargetTable.query.all()
    app.logger.debug(target_list)
    return jsonify({'body': [TargetTable.to_dict(rec) for rec in target_list]}), 200


# 特定データ取得
@app.route("/app/records/<user_id>", methods=['GET', 'POST'])
def get_records(user_id):
    target_list = TargetTable.query.filter_by(user_id=user_id).all()
    app.logger.debug(target_list)
    return jsonify({'body': [TargetTable.to_dict(rec) for rec in target_list]}), 200


# データ登録
@app.route("/app/records/new", methods=['GET', 'POST'])
def create_records():
    app.logger.debug(request.json)

    # データインポート
    reader = request.json
    app.logger.debug(f"reader={reader.__class__}")
    for rec in reader:
        app.logger.debug(rec)
        obj = TargetTable(
            user_id=rec["user_id"],
            dept_no=rec["dept_no"],
            user_name=rec["user_name"],
            created_on=datetime.datetime.now()
        )
        db.session.add(obj)
    db.session.commit()

    return 'json data was registered.'


# データ削除
@app.route("/app/records/<user_id>", methods=['DELETE'])
def delete_records(user_id):
    # データ取得
    target_list = TargetTable.query.filter_by(user_id=user_id).all()
    app.logger.debug(target_list)

    # データ削除
    for obj in target_list:
        db.session.delete(obj)
    db.session.commit()

    return f"user_id={user_id} was deleted."


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
