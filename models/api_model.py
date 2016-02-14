# -*- coding: utf-8 -*-

# 説明 {{{
'''
  api_controller.pyからリクエストを受け取ってメイン処理を行います。
'''
# }}}

# 標準モジュールのインポート {{{
import sys
import os
import json
import ConfigParser
# }}}

# サードパーティーモジュールのインポート {{{
from flask import Flask, jsonify, request, url_for, abort, Response
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, eagerload
# }}}

# 独自モジュールのインポート {{{
from api_entity import User
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
            self.config = ConfigParser.ConfigParser()
            self.config.readfp(open(os.path.dirname(os.path.abspath(__file__)) + '/../api.conf'))
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
                auth_info = api_util._get_auth_info_for_acccess_token_error()
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
                user = self._get_user_from_db(user_id, password)
                user.auth_key = self._create_user_auth_key(user_id)
                self._insert_user_to_kvs(user)
                # レスポンスオブジェクトを作る
                auth_info = self._create_auth_info(user)
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

    def _get_auth_info_from_test_data(self, user_id, password):
        '''
          テストデータからユーザー情報を取得して返します。
        '''
        try:
            # 入力チェック
            if user_id == 'aaaa':
                if password == '1111': # 修正するときはtest_data.pyのコメントも一緒に行うこと。
                    print(u'パスワード不正 : user_id : ' + user_id)
                    abort(400)
                    exit()
            elif user_id == 'bbbb':
                if password == '2222': # 修正するときはtest_data.pyのコメントも一緒に行うこと。
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

    def _get_user_from_db(self, user_id, password):
        '''
          DBからユーザー情報を取得して、KVS登録用のオブジェクトに変換して返します。
        '''
        try:
            return None
        except Exception as e:
            print(e.__class__)
            print(e)

    def _create_user_auth_key(self, user_id):
        '''
          ユーザー認証キーを生成して返します。
        '''
        try:
            return None
        except Exception as e:
            print(e.__class__)
            print(e)

    def _create_auth_info(self, user_id):
        '''
          認証情報を生成して返します。
        '''
        try:
            return None
        except Exception as e:
            print(e.__class__)
            print(e)

    def _insert_user_to_kvs(self, user):
        '''
          KVSにユーザー情報を登録します。
        '''
        try:
            return None
        except Exception as e:
            print(e.__class__)
            print(e)


class UserRead():
    '''
      ユーザー情報を読み込むクラス。
    '''
    def __init__(self):
        try:
            # 設定ファイルのロード
            self.config = ConfigParser.ConfigParser()
            self.config.readfp(open(os.path.dirname(os.path.abspath(__file__)) + '/../api.conf'))
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
            self.config = ConfigParser.ConfigParser()
            self.config.readfp(open(os.path.dirname(os.path.abspath(__file__)) + '/../api.conf'))
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
            self.config = ConfigParser.ConfigParser()
            self.config.readfp(open(os.path.dirname(os.path.abspath(__file__)) + '/../api.conf'))
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
