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
import abc
from contextlib import contextmanager,
# }}}

# サードパーティーモジュールのインポート {{{
from sqlalchemy import create_engine, Column, ForeignKey, String, Integer,
from sqlalchemy.ext.declarative import declarative_base,
from sqlalchemy.orm import scoped_session, relation, sessionmaker,
# }}}

# 独自モジュールのインポート {{{
# }}}

# 前処理 {{{
try:
    # 設定ファイルのロード
    # 設定ファイルを読み込む処理がダメ。これだと何度か読み込み処理を行っていることになる。
    config = ConfigParser.ConfigParser()
    config.readfp(open(os.path.dirname(os.path.abspath(__file__)) + '/../api.conf'))
except Exception as e:
    print(e.__class__)
    print(e)
    exit()

# データベースの接続情報を取得。
engine = create_engine(config['data_source']['dsn'], echo=True)
# セッションはスレッドローカルにする
Session = scoped_session(sessionmaker(bind=engine))
# ドメインが継承するスーパークラス
Base = declarative_base()
# }}}


@contextmanager
def transaction():
    '''
      DBトランザクション用のコンテキストマネージャ
    '''
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


class EntityBase(object):
    '''
      エンティティクラス共通の親クラス
    '''
    id = Column(Integer, primary_key=True)

    def __repr__(self):
        items = ['{key}={value}'.format(key=key, value=value)
                     for key, value in self.__dict__.items() if not key.startswith('_')]
        return '<{cls_name}: {attrs}>'.format(cls_name=self.__class__.__name__,
                                              attrs=', '.join(items),)


class UserEntity(Base, EntityBase):
    '''
      ユーザー (社員) エンティティクラス
    '''
    # テーブル名
    __tablename__ = 'users'
    # 社員ID
    user_id = Column(String(255), nullable=False)
    # ログインパスワード
    password = Column(String(255), nullable=False)
    # 氏名
    name = Column(String(255), nullable=False)
    # 所属グループ
    affiliation_group = Column(String(255))
    # 役職
    managerial_position = Column(String(255))
    # メールアドレス
    mail_address = Column(String(255))


class MapperBase(object):
    '''
      マッパークラスの共通親クラス
    '''
    __metaclass__ = abc.ABCMeta

    @classmethod
    def get_session(cls):
        return Session()


class UserMapper(MapperBase):
    '''
      UserオブジェクトとUserEntityオブジェクトをマッピングするマッパークラス
    '''
    @classmethod
    def insert(cls, user):
        session = cls.get_session()
        addresses = [
            AddressRecord(address=address)
            for address in user.addresses
        ]
        user_from_db = UserRecord(
            name=user.name,
            age=user.age,
            addresses=addresses,
        )
        session.add(user_from_db)
        return user_from_db.id

    @classmethod
    def select(session, **kwargs):
        user_from_db = session.query(UserEntity).filter_by(**kwargs)
        users = User(
            id_=user_from_db.id,
            user_id=user_from_db.user_id,
            password=user_from_db.password,
            name=user_from_db.name,
            affiliation_group=user_from_db.affiliation_group,
            managerial_position=user_from_db.managerial_position,
            mail_address=user_from_db.mail_address,
        )
        return users

    @classmethod
    def delete(cls, user):
        session = cls.get_session()
        user_from_db = session.query(UserRecord).filter_by(id=user.id).first()
        session.delete(user_from_db)


class User(object):
    '''
      ユーザー (社員) ドメインクラス
    '''
    def __init__(self, id_=None, user_id, password, name, affiliation_group,
                 managerial_position, mail_address):
        self.id = id_
        self.user_id = user_id
        self.password = password
        self.name = name
        self.affiliation_group = affiliation_group
        self.managerial_position = managerial_position
        self.mail_address = mail_address

# 後処理 {{{
if __name__ == '__main__':
    # データベース、テーブル作成処理。モジュールとしてimportする時は実行されない。
    try:
        # データベースかテーブルが存在する場合は新規作成しない。
        Base.metadata.create_all(bind=engine, checkfirst=False)
    except Exception as e:
        print(e.__class__)
        print(e)
    finally:
        print(os.getpid())
# }}}

