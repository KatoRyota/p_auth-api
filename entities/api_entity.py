# -*- coding: utf-8 -*-

# 説明 {{{
'''
  アプリケーションのルートディレクトリで以下のコマンドを実行するとテーブルが作成されます。

    python entities/api_entity.py
'''
# }}}

# 標準モジュールのインポート {{{
import os
import ConfigParser
# }}}

# サードパーティーモジュールのインポート {{{
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Float, ForeignKey, Table, create_engine
from sqlalchemy.orm import relation
Base = declarative_base()
# }}}

# 独自モジュールのインポート {{{
# }}}

# 前処理 {{{
try:
    # 設定ファイルのロード
    config = ConfigParser.ConfigParser()
    config.readfp(open(os.path.dirname(os.path.abspath(__file__)) + '/../api.conf'))
except Exception as e:
    print(e.__class__)
    print(e)
    exit()
# }}}


class User(Base):
    '''
      ユーザー情報を格納するクラス。
    '''
    # テーブル名
    __tablename__ = 'user'
    # 社員ID
    employee_id = Column(String(255), primary_key=True)
    # 氏名
    name = Column(String(255), nullable=False)
    # 所属グループ
    affiliation_group = Column(String(255))
    # 役職
    managerial_position = Column(String(255))
    # メールアドレス
    mail_address = Column(String(255))

    def __repr__(self):
        return \
            "<User(" +\
                "employee_id={employee_id}, " +\
                "name={name}, " +\
                "affiliation_group={affiliation_group}, " +\
                "managerial_position={managerial_position}" +\
                "mail_address={mail_address}" +\
            ")>"\
            .format(employee_id=self.employee_id, name=self.name,
                    affiliation_group=self.affiliation_group,
                    managerial_position=self.managerial_position, mail_address=self.mail_address)


# 後処理 {{{{
if __name__ == '__main__':
    # データベース、テーブル作成処理。モジュールとしてimportする時は実行されない。
    try:
        # データベースの接続情報を取得。
        engine = create_engine(config['data_source']['dsn'], echo=True)
        # データベースかテーブルが存在する場合は新規作成しない。
        Base.metadata.create_all(bind=engine, checkfirst=False)
    except Exception as e:
        print(e.__class__)
        print(e)
    finally:
        print(os.getpid())
# }}}

