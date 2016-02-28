# -*- coding: utf-8 -*-

# 説明 {{{
'''
  アプリケーションのルートディレクトリで以下のコマンドを実行するとテーブルが作成されます。

    python persistence/api_persistence.py
'''
# }}}

# 標準モジュールのインポート {{{
import os
import json
import ConfigParser
# }}}

# サードパーティーモジュールのインポート {{{
from sqlalchemy import create_engine, Column, ForeignKey, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, relation, sessionmaker
# }}}

# 独自モジュールのインポート {{{
# }}}

# 前処理 {{{
Base = declarative_base()
# }}}


class BaseEntity(object):
    '''
      エンティティクラス共通の親クラス
    '''
    id = Column(Integer, primary_key=True)

    def __repr__(self):
        items = ['{key}={value}'.format(key=key, value=value)
                     for key, value in self.__dict__.items() if not key.startswith('_')]
        return '<{cls_name}: {attrs}>'.format(cls_name=self.__class__.__name__,
                                              attrs=', '.join(items),)


class UserEntity(Base, BaseEntity):
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


class UserMapper(object):
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
    def select(cls, session, **kwargs):
        print('UserMapper.select()開始')
        print('**kwargs : ' + json.dumps(kwargs)) # debug
        user_list_from_db = session.query(UserEntity).filter_by(**kwargs).all()
        user_list = []
        for user_from_db in user_list_from_db:
            user = User(
                id_=user_from_db.id,
                user_id=user_from_db.user_id,
                password=user_from_db.password,
                name=user_from_db.name,
                affiliation_group=user_from_db.affiliation_group,
                managerial_position=user_from_db.managerial_position,
                mail_address=user_from_db.mail_address
            )
            print('user_id : ' + user_from_db.user_id) # debug
            print('id : ' + str(user_from_db.id)) # debug
            user_list.append(user)
        return user_list

    @classmethod
    def delete(cls, user):
        session = cls.get_session()
        user_from_db = session.query(UserRecord).filter_by(id=user.id).first()
        session.delete(user_from_db)


class User(object):
    '''
      ユーザー (社員) ドメインクラス
    '''
    def __init__(self, user_id, password, name, affiliation_group, managerial_position,
                 mail_address, id_=None):
        self.id = id_
        self.user_id = user_id
        self.password = password
        self.name = name
        self.affiliation_group = affiliation_group
        self.managerial_position = managerial_position
        self.mail_address = mail_address

# 後処理 {{{
if __name__ == '__main__':
    # データベース、テーブル作成処理。モジュールとしてimportされる時は実行されない。
    try:
        # 設定ファイルのロード
        config = ConfigParser.SafeConfigParser()
        config.read(os.path.dirname(os.path.abspath(__file__)) + '/../api.conf')
        # データベースのコネクションを取得
        engine = create_engine(config.get('data_source', 'dsn'), echo=True,
                                          encoding='utf-8', convert_unicode=True)
        # データベース, テーブル作成
        Base.metadata.create_all(bind=engine, checkfirst=False)
    except Exception as e:
        print(e.__class__)
        print(e)
    finally:
        print(os.getpid())
        exit()
# }}}

