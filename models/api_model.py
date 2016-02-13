# -*- coding: utf-8 -*-

# 説明 {{{
'''
  api_controller.pyからリクエストを受け取ってメイン処理を行います。
'''
# }}}

# 標準モジュールのインポート {{{
import sys
import os
import re
import json
import ConfigParser
# }}}

# サードパーティーモジュールのインポート {
from flask import Flask, jsonify, request, url_for, abort, Response
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, eagerload
# }

# 独自モジュールのインポート {
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../entities')
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../test')
from api_entity import User
# テストデータ
import user_json
# }

# 前処理 {{{
# }}}


class UserCreate():
    '''
      ユーザー情報を作成するクラス。
    '''
    def __init__(self):
        # 設定ファイルのロード
        config = ConfigParser.ConfigParser()
        config.readfp(open(os.path.dirname(os.path.abspath(__file__)) + '/../api.conf'))

    def create(self, request):
        '''
          KVSにユーザー情報を登録します。
        '''
        try:
            # ToDo :
            print(u'KVSにユーザー情報を登録します。')
        except Exception as e:
            print(e.__class__)
            print(e)


class UserRead():
    '''
      ユーザー情報を読み込むクラス。
    '''
    def __init__(self):
        # 設定ファイルのロード
        self.config = ConfigParser.ConfigParser()
        self.config.readfp(open(os.path.dirname(os.path.abspath(__file__)) + '/../api.conf'))

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
                return response

            # テストモード判定
            if self._get_test_mode() == 'true':
                # レスポンスオブジェクトを作る
                user = self._get_user_from_user_json(user_auth_key)
                response = jsonify(user)
                print(response)
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

    def _get_test_mode(self):
        print(self.config.items('test')) # debug

        for i, test in enumerate(self.config.items('test')):
            print(test[0]) # debug
            if test[0] == 'mode':
                return test[1]

    def _get_user_for_acccess_token_error(self):
        '''
          アクセストークンエラー用のレスポンスオブジェクトを生成して返します。
        '''
        try:
            return user['cccc']
        except Exception as e:
            print(e.__class__)
            print(e)

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

    def _get_user_from_user_json(self, user_auth_key):
        '''
          テストデータからユーザー情報を取得して返します。
        '''
        try:
            return user_json.user[user_auth_key]
        except Exception as e:
            print(e.__class__)
            print(e)


class UserUpdate():
    '''
      ユーザー情報を更新するクラス。
    '''
    def __init__(self):
        # 設定ファイルのロード
        config = ConfigParser.ConfigParser()
        config.readfp(open(os.path.dirname(os.path.abspath(__file__)) + '/../api.conf'))

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
        # 設定ファイルのロード
        config = ConfigParser.ConfigParser()
        config.readfp(open(os.path.dirname(os.path.abspath(__file__)) + '/../api.conf'))

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


# 後処理 {{{{
# }}}
