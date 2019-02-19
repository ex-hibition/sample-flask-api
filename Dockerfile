# 公式centos7イメージを利用
FROM centos:7

## python設定
# Python3をIUSリポジトリからインストールする
RUN yum -y update nss
RUN yum -y install ca-certificates
RUN curl -s https://setup.ius.io/ | bash

# python36インストール
RUN yum install -y python36u python36u-devel python36u-libs python36u-pip python36u-setuptools
RUN ln -s /usr/bin/python3.6 /usr/bin/python3
RUN ln -s /usr/bin/pip3.6 /usr/bin/pip3

RUN pip3 install --upgrade pip
RUN pip3 install pipenv

## oracle client設定
# oracleクライアント用ディレクトリを作成してコンテナにコピー
RUN mkdir -p /opt/oracle/
ADD oracle/instantclient-basic-linux.x64-18.3.0.0.0dbru.zip /opt/oracle/
ADD oracle/instantclient-sqlplus-linux.x64-18.3.0.0.0dbru.zip /opt/oracle/

# unzip,libaioインストール
# whichがないと"pipenv run pip ..."ができない
RUN yum install -y unzip libaio make gcc pcre-devel which

RUN unzip /opt/oracle/instantclient-basic-linux.x64-18.3.0.0.0dbru.zip -d /opt/oracle/
RUN unzip /opt/oracle/instantclient-sqlplus-linux.x64-18.3.0.0.0dbru.zip -d /opt/oracle/

# Oracle環境変数を設定
ENV LD_LIBRARY_PATH=/opt/oracle/instantclient_18_3 \
    ORACLE_HOME=/opt/oracle/instantclient_18_3 \
    NLS_LANG=Japanese_Japan.JA16SJIS \
    PATH=$PATH:$LD_LIBRARY_PATH:$ORACLE_HOME

# アプリケーションディレクトリ作成
RUN mkdir -p /usr/local/app
COPY . /usr/local/app
WORKDIR /usr/local/app

# 環境変数を設定
ENV LANG=ja_JP.utf8
RUN localedef -f UTF-8 -i ja_JP ja_JP.utf8

# 依存ライブラリインストール
RUN pipenv run pip install pip --upgrade pip
RUN pipenv install

# アプリケーション起動
ENTRYPOINT ["pipenv", "run"]
CMD ["start"]
