# -*- coding: utf-8 -*-

# 説明 {{{
'''
  api_service.pyからリクエストを受け取ってメイン処理を行います。
'''
# }}}

# 標準モジュールのインポート {{{
import sys
import os
import json
import ConfigParser
import uuid
from contextlib import contextmanager
# }}}

# サードパーティーモジュールのインポート {{{
from flask import Flask, jsonify, request, url_for, abort, Response
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, relation, sessionmaker
# }}}

# 独自モジュールのインポート {{{
from api_persistence import User, UserMapper
import api_util
# テストデータ
import test_data
# }}}

# 前処理 {{{
# }}}


class UserCreate():
    '''
      ユーザー情報を作成するクラス。
    '''
    def __init__(self):
        try:
            # 設定ファイルのロード
            self.config = ConfigParser.SafeConfigParser()
            self.config.read(os.path.dirname(os.path.abspath(__file__)) + '/../api.conf')
        except Exception as e:
            print(e.__class__)
            print(e)

    def create(self, request):
        '''
          KVSにユーザー情報を登録します。
        '''
        try:
            print(u'UserCreate.create()開始') # debug
            # Content-Body を JSON 形式として辞書に変換する
            request_json = json.loads(request.data)
            acccess_token = request_json['acccess_token']
            user_id = request_json['request_data']['user_id']
            password = request_json['request_data']['password']

            if acccess_token != 'calendar-app':
                print(u'acccess_tokenが不正です。')
                # レスポンスオブジェクトを作る
                auth_info = self._get_auth_info_for_acccess_token_error()
                response = jsonify(auth_info)
                print(response)
                response.status_code = 200
                return response
            # テストモード判定
            elif api_util.get_test_mode(self) == 'true':
                print(u"test mode : yes") # debug
                # レスポンスオブジェクトを作る
                auth_info = self._get_auth_info_from_test_data(user_id, password)
                response = jsonify(auth_info)
                print(response)
                response.status_code = 200
                return response
            else:
                print(u"test mode : no") # debug
                user_from_db = self._select_user_fron_db(user_id, password)

                if len(user_from_db) == 1:
                    user_auth_key = self._create_user_auth_key(user_from_db[0]['user_id'])
                    user_to_kvs = self._create_user_to_kvs(user_from_db[0], user_auth_key)

                    if self._insert_user_to_kvs(user_to_kvs):
                        auth_info = self._create_auth_info(user)
                    else:
                        auth_info = self._get_auth_info_for_kvs_insert_error()
                else:
                    auth_info = self._get_auth_info_for_auth_error()

                response = jsonify(auth_info)
                print(response)
                response.status_code = 200
                return response
        except Exception as e:
            print(e.__class__)
            print(e)

    def _get_auth_info_for_acccess_token_error(self):
        '''
          アクセストークンエラー用のレスポンスオブジェクトを生成して返します。
        '''
        return {
            'result_code'    : 200,
            'result_message' : '正常終了',
            'response_data'  : {
                'user_auth_key' : '',
                'unit_error' : {
                    '400' : 'アクセストークン不正'
                }
            }
        }

    def _get_auth_info_for_auth_error(self):
        '''
          認証エラー用のレスポンスオブジェクトを生成して返します。
        '''
        return {
            'result_code'    : 200,
            'result_message' : '正常終了',
            'response_data'  : {
                'user_auth_key' : '',
                'unit_error' : {
                    '401' : '認証エラー'
                }
            }
        }

    def _get_auth_info_for_kvs_insert_error(self):
        '''
          KVS INSERT エラー用のレスポンスオブジェクトを生成して返します。
        '''
        return {
            'result_code'    : 200,
            'result_message' : '正常終了',
            'response_data'  : {
                'user_auth_key' : '',
                'unit_error' : {
                    '402' : 'KVS INSERT エラー'
                }
            }
        }

    def _get_auth_info_from_test_data(self, user_id, password):
        '''
          テストデータからユーザー情報を取得して返します。
        '''
        try:
            # 入力チェック
            if user_id == 'aaaa':
                if password != '1111': # 修正するときはtest_data.pyのコメントも一緒に行うこと。
                    print(u'パスワード不正 : user_id : ' + user_id)
                    abort(400)
                    exit()
            elif user_id == 'bbbb':
                if password != '2222': # 修正するときはtest_data.pyのコメントも一緒に行うこと。
                    print(u'パスワード不正 : user_id : ' + user_id)
                    abort(400)
                    exit()
            else:
                print(u'ユーザーID不正 : user_id : ' + user_id)
                abort(400)
                exit()

            return test_data.account[user_id]
        except Exception as e:
            print(e.__class__)
            print(e)

    def _create_user_auth_key(self, user_id):
        '''
          ユーザー認証キーを生成して返します。
        '''
        return uuid.uuid4()

    def _create_user_to_kvs(self, user_from_db, user_auth_key):
        '''
          KVS INSERT 用のオブジェクトを生成して返します。
        '''
        return {
            user_auth_key : {
                'user_id' : user_from_db['user_id'],
                'name' : user_from_db['name'],
                'affiliation_group' : user_from_db['affiliation_group'].split(","),
                'managerial_position' : user_from_db['managerial_position'].split(","),
                'mail_address' : user_from_db['mail_address'].split(",")
            }
        }

    def _create_auth_info(self, user_id):
        '''
          認証情報を生成して返します。
        '''
        try:
            return None
        except Exception as e:
            print(e.__class__)
            print(e)

    def _select_user_fron_db(self, user_id, password):
        session = None
        try:
            # データベースの接続情報を取得。
            engine = create_engine(self.config.get('data_source', 'dsn'), echo=True,
                                                   encoding='utf-8', convert_unicode=True)
            # セッションはスレッドローカルにする
            Session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
            session = Session()
            print('user_id : ' + user_id + ', password : ' + password)
            return UserMapper.select(session, user_id=user_id, password=password)
        except:
            raise
        finally:
            session.close()

    def _insert_user_to_kvs(self, user):
        '''
          KVSにユーザー情報を登録します。
        '''
        try:
            print(json.dumps(user))
        except Exception as e:
            print(e.__class__)
            print(e)
            return False


class UserRead():
    '''
      ユーザー情報を読み込むクラス。
    '''
    def __init__(self):
        try:
            # 設定ファイルのロード
            self.config = ConfigParser.SafeConfigParser()
            self.config.read(os.path.dirname(os.path.abspath(__file__)) + '/../api.conf')
        except Exception as e:
            print(e.__class__)
            print(e)

    def read(self, request):
        '''
          KVSからユーザー情報を取得して返します。
        '''
        try:
            print(u'UserRead.read()開始') # debug
            # Content-Body を JSON 形式として辞書に変換する
            request_json = json.loads(request.data)
            # リクエストされたパスと ID を持つユーザを探す
            acccess_token = request_json['acccess_token']
            user_auth_key = request_json['request_data']['user_auth_key']

            if acccess_token != 'calendar-app':
                print(u'acccess_tokenが不正です。')
                # レスポンスオブジェクトを作る
                user = self._get_user_for_acccess_token_error()
                response = jsonify(user)
                response.status_code = 200
                return response
            # テストモード判定
            elif api_util.get_test_mode(self) == 'true':
                print(u"test mode : yes")
                # レスポンスオブジェクトを作る
                user = self._get_user_from_test_data(user_auth_key)
                response = jsonify(user)
                print(response)
                response.status_code = 200
                return response
            else:
                # レスポンスオブジェクトを作る
                user = self._get_user_from_kvs(user_auth_key)
                response = jsonify(user)
                # ステータスコードは Created (201)
                response.status_code = 200
                return response
        except Exception as e:
            print(e.__class__)
            print(e)

    def _get_user_for_acccess_token_error(self):
        '''
            アクセストークンエラー用のレスポンスオブジェクトを生成して返します。
        '''
        return {
            'result_code'    : 200,
            'result_message' : '正常終了',
            'response_data'  : {
                'user_id' : '',
                'name' : '',
                'affiliation_group' : [],
                'managerial_position' : [],
                'mail_address' : [],
                'unit_error' : {
                    '400' : 'アクセストークン不正'
                }
            }
        }

    def _get_user_from_kvs(self, user_auth_key):
        '''
          KVSからユーザー情報を取得して返します。
        '''
        try:
            # ToDo :
            print(u'KVSからユーザー情報を取得して返します。')
        except Exception as e:
            print(e.__class__)
            print(e)

    def _get_user_from_test_data(self, user_auth_key):
        '''
          テストデータからユーザー情報を取得して返します。
        '''
        try:
            return test_data.user[user_auth_key]
        except Exception as e:
            print(e.__class__)
            print(e)


class UserUpdate():
    '''
      ユーザー情報を更新するクラス。
    '''
    def __init__(self):
        try:
            # 設定ファイルのロード
            self.config = ConfigParser.SafeConfigParser()
            self.config.read(os.path.dirname(os.path.abspath(__file__)) + '/../api.conf')
        except Exception as e:
            print(e.__class__)
            print(e)

    def update(self, request):
        '''
          KVS上のユーザー情報を更新します。
        '''
        try:
            # ToDo :
            print(u'KVS上のユーザー情報を更新します。')
        except Exception as e:
            print(e.__class__)
            print(e)


class UserDelete():
    '''
      ユーザー情報を削除するクラス。
    '''
    def __init__(self):
        try:
            # 設定ファイルのロード
            self.config = ConfigParser.SafeConfigParser()
            self.config.read(os.path.dirname(os.path.abspath(__file__)) + '/../api.conf')
        except Exception as e:
            print(e.__class__)
            print(e)

    def delete(self, request):
        '''
          KVS上のユーザー情報を削除します。
        '''
        try:
            # ToDo :
            print(u'KVS上のユーザー情報を削除します。')
        except Exception as e:
            print(e.__class__)
            print(e)


# 後処理 {{{
# }}}
