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
import logging
from contextlib import contextmanager
# }}}

# サードパーティーモジュールのインポート {{{
from flask import Flask, jsonify, request, url_for, abort, Response
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, relation, sessionmaker
import redis
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

    # ロガー
    logger = logging.getLogger('logExample')

    def __init__(self):
        try:
            # 設定ファイルのロード
            self.config = ConfigParser.SafeConfigParser()
            self.config.read(os.path.dirname(os.path.abspath(__file__)) + '/../api.conf')
        except Exception as e:
            self.logger.error(e.__class__)
            self.logger.error(e)

    def create(self, request):
        '''
          KVSにユーザー情報を登録します。
        '''
        try:
            self.logger.info(u'UserCreate.create()開始') # debug
            # json→dict
            request_json = json.loads(request.data)
            acccess_token = request_json['acccess_token']        # アクセストークン
            user_id = request_json['request_data']['user_id']    # ユーザーID
            password = request_json['request_data']['password']  # パスワード
            # アクセストークンチェック
            if acccess_token != 'calendar-app':
                self.logger.warn(u'acccess_tokenが不正です。')
                # 認証情報オブジェクトを生成 (認証キーは空文字)
                auth_info = self._get_auth_info_for_acccess_token_error()
            # テストモードチェック
            elif api_util.get_test_mode(self) == 'true':
                self.logger.info(u"test mode : yes") # debug
                # 認証情報オブジェクトを生成 (認証キーはテスト用の固定値)
                auth_info = self._get_auth_info_from_test_data(user_id, password)
            # 通常モード
            else:
                self.logger.info(u"test mode : no") # debug
                # DBからユーザー情報取得
                user_list_from_db = self._select_user_from_db(user_id, password)
                # レコード数チェック
                if len(user_list_from_db) == 1:
                    # レコードが1件の場合は認証成功
                    # 認証情報オブジェクトを生成
                    auth_info = self._get_auth_info_for_auth_success(user_list_from_db)
                else:
                    # レコードが複数件の場合は認証失敗
                    # 認証情報オブジェクトを生成 (認証キーは空文字)
                    auth_info = self._get_auth_info_for_auth_error()
            # ユーザー認証情報を返す (認証キーは前処理で取得したもの)
            return Response(
                json.dumps(auth_info, ensure_ascii=False, indent=4),
                mimetype='application/json',
                status=200,
            )
        except Exception as e:
            self.logger.error(e.__class__)
            self.logger.error(e)

    def _get_auth_info_for_auth_success(self, user_list_from_db):
        # ユーザー認証キー生成
        user_auth_key = self._create_user_auth_key(user_list_from_db[0].user_id)
        # Redis登録用オブジェクト生成
        user_to_kvs = self._create_user_to_kvs(user_list_from_db[0])
        # Redis登録処理
        if self._insert_user_to_kvs(user_auth_key, user_to_kvs):
            # Redis登録処理の成功
            # 認証情報オブジェクトを生成 (認証キーは前処理で動的に生成したもの)
            auth_info = self._create_auth_info(user_auth_key)
        else:
            # Redis登録処理の失敗
            # 認証情報オブジェクトを生成 (認証キーは空文字)
            auth_info = self._get_auth_info_for_kvs_insert_error()
        # 認証情報オブジェクトを返す
        return auth_info

    def _get_auth_info_for_acccess_token_error(self):
        '''
          アクセストークンエラー用のレスポンスオブジェクトを生成して返します。
        '''
        return {
            'result_code'    : 200,
            'result_message' : u'正常終了',
            'response_data'  : {
                'user_auth_key' : '',
                'unit_error' : {
                    '400' : u'アクセストークン不正'
                }
            }
        }

    def _get_auth_info_for_auth_error(self):
        '''
          認証エラー用のレスポンスオブジェクトを生成して返します。
        '''
        return {
            'result_code'    : 200,
            'result_message' : u'正常終了',
            'response_data'  : {
                'user_auth_key' : '',
                'unit_error' : {
                    '401' : u'認証エラー'
                }
            }
        }

    def _get_auth_info_for_kvs_insert_error(self):
        '''
          KVS INSERT エラー用のレスポンスオブジェクトを生成して返します。
        '''
        return {
            'result_code'    : 200,
            'result_message' : u'正常終了',
            'response_data'  : {
                'user_auth_key' : '',
                'unit_error' : {
                    '402' : u'KVS INSERT エラー'
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
                    self.logger.warn(u'パスワード不正 : user_id : ' + user_id)
                    abort(400)
                    exit()
            elif user_id == 'bbbb':
                if password != '2222': # 修正するときはtest_data.pyのコメントも一緒に行うこと。
                    self.logger.warn(u'パスワード不正 : user_id : ' + user_id)
                    abort(400)
                    exit()
            else:
                self.logger.warn(u'ユーザーID不正 : user_id : ' + user_id)
                abort(400)
                exit()

            return test_data.account[user_id]
        except Exception as e:
            self.logger.error(e.__class__)
            self.logger.error(e)

    def _create_user_auth_key(self, user_id):
        '''
          ユーザー認証キーを生成して返します。
        '''
        return str(uuid.uuid4())

    def _create_auth_info(self, user_auth_key):
        '''
          認証情報を生成して返します。
        '''
        return {
            'result_code'    : 200,
            'result_message' : u'正常終了',
            'response_data'  : {
                'user_auth_key' : user_auth_key,
                'unit_error' : {
                    '200' : u'正常終了'
                }
            }
        }

    def _select_user_from_db(self, user_id, password):
        session = None
        try:
            # データベースの接続情報を取得。
            engine = create_engine(self.config.get('data_source', 'dsn'), echo=True,
                                                   encoding='utf-8', convert_unicode=True)
            # セッションはスレッドローカルにする
            Session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
            session = Session()
            self.logger.debug('user_id : %s, password : %s' % (user_id, password))
            user_list_from_db = UserMapper.select(session, user_id=user_id, password=password)
            session.commit()
            return user_list_from_db
        except Exception as e:
            self.logger.error(e.__class__)
            self.logger.error(e)
            session.rollback()
            raise
        finally:
            session.close()

    def _create_user_to_kvs(self, user_from_db):
        '''
          KVS INSERT 用のオブジェクトを生成して返します。
        '''
        return {
            'user_id' : user_from_db.user_id,
            'name' : user_from_db.name,
            'affiliation_group' : user_from_db.affiliation_group,
            'managerial_position' : user_from_db.managerial_position,
            'mail_address' : user_from_db.mail_address,
        }

    def _insert_user_to_kvs(self, user_auth_key, user_to_kvs):
        '''
          KVSにユーザー情報を登録します。
        '''
        try:
            self.logger.info(u'KVSにユーザー情報を登録します。')
            # Redisとのコネクション取得
            conn = redis.StrictRedis(self.config.get('data_source_for_kvs', 'host'),
                                     self.config.get('data_source_for_kvs', 'port'))
            # Redisにユーザー認証キーをKey, ユーザー情報をValueとして登録
            conn.hmset(user_auth_key, user_to_kvs)
            self.logger.debug(u'Redisに登録したデータ : %s' % api_util.pp(conn.hgetall(user_auth_key)))
            return True
        except Exception as e:
            self.logger.error(e.__class__)
            self.logger.error(e)
            return False


class UserRead():
    '''
      ユーザー情報を読み込むクラス。
    '''
    # ロガー
    logger = logging.getLogger('logExample')

    def __init__(self):
        try:
            # 設定ファイルのロード
            self.config = ConfigParser.SafeConfigParser()
            self.config.read(os.path.dirname(os.path.abspath(__file__)) + '/../api.conf')
        except Exception as e:
            self.logger.error(e.__class__)
            self.logger.error(e)

    def read(self, request):
        '''
          KVSからユーザー情報を取得して返します。
        '''
        try:
            self.logger.info(u'UserRead.read()開始')
            # json→dict
            request_json = json.loads(request.data)
            acccess_token = request_json['acccess_token']                  # アクセストークン
            user_auth_key = request_json['request_data']['user_auth_key']  # ユーザー認証キー
            # アクセストークンチェック
            if acccess_token != 'calendar-app':
                self.logger.warn(u'acccess_tokenが不正です。')
                # ユーザー情報取得 (アクセストークンエラー用の固定値)
                user = self._get_user_for_acccess_token_error()
            # テストモードチェック
            elif api_util.get_test_mode(self) == 'true':
                self.logger.info(u"test mode : yes")
                # ユーザー情報取得 (テストモード用の固定値)
                user = self._get_user_from_test_data(user_auth_key)
            # 通常モード
            else:
                # ユーザー情報取得 (検索条件にユーザー認証キーをセットしてRedisから取得)
                user = self._convert_user_from_kvs(self._get_user_from_kvs(user_auth_key))
            # ユーザー情報を返す
            return Response(
                json.dumps(user, ensure_ascii=False, indent=4),
                mimetype='application/json',
                status=200,
            )
        except Exception as e:
            self.logger.error(e.__class__)
            self.logger.error(e)

    def _get_user_for_acccess_token_error(self):
        '''
            アクセストークンエラー用のレスポンスオブジェクトを生成して返します。
        '''
        return {
            'result_code'    : 200,
            'result_message' : u'正常終了',
            'response_data'  : {
                'user_id' : '',
                'name' : '',
                'affiliation_group' : [],
                'managerial_position' : [],
                'mail_address' : [],
                'unit_error' : {
                    '400' : u'アクセストークン不正'
                }
            }
        }

    def _get_user_from_kvs(self, user_auth_key):
        '''
          KVSからユーザー情報を取得して返します。
        '''
        try:
            self.logger.info(u'KVSからユーザー情報を取得して返します。')
            # Redisとのコネクション取得
            conn = redis.StrictRedis(self.config.get('data_source_for_kvs', 'host'),
                                     self.config.get('data_source_for_kvs', 'port'))
            self.logger.debug(u'Redisから取得したデータ : %s' % api_util.pp(conn.hgetall(user_auth_key)))
            # ユーザー認証キーを引数に与えてユーザー情報を取得して返す
            return conn.hgetall(user_auth_key)
        except Exception as e:
            self.logger.error(e.__class__)
            self.logger.error(e)
            raise

    def _convert_user_from_kvs(self, user_from_kvs):
        '''
          KVSから取得したユーザー情報をレスポンスオブジェクトに変換して返します。
        '''
        self.logger.info(u'KVSから取得したユーザー情報をレスポンスオブジェクトに変換して返します。')
        return {
            'result_code'    : 200,
            'result_message' : u'正常終了',
            'response_data'  : {
                'user_id' : user_from_kvs['user_id'].decode('utf-8'),
                'name' : user_from_kvs['name'].decode('utf-8'),
                'affiliation_group' : [
                    x.decode('utf-8') for x in user_from_kvs['affiliation_group'].split(',')
                ],
                'managerial_position' : [
                    x.decode('utf-8') for x in user_from_kvs['managerial_position'].split(',')
                ],
                'mail_address' : [
                    x.decode('utf-8') for x in user_from_kvs['mail_address'].split(',')
                ],
                'unit_error' : {
                    '200' : u'正常終了'
                }
            }
        }

    def _get_user_from_test_data(self, user_auth_key):
        '''
          テストデータからユーザー情報を取得して返します。
        '''
        try:
            return test_data.user[user_auth_key]
        except Exception as e:
            self.logger.error(e.__class__)
            self.logger.error(e)


class UserUpdate():
    '''
      ユーザー情報を更新するクラス。
    '''
    # ロガー
    logger = logging.getLogger('logExample')

    def __init__(self):
        try:
            # 設定ファイルのロード
            self.config = ConfigParser.SafeConfigParser()
            self.config.read(os.path.dirname(os.path.abspath(__file__)) + '/../api.conf')
        except Exception as e:
            self.logger.error(e.__class__)
            self.logger.error(e)

    def update(self, request):
        '''
          KVS上のユーザー情報を更新します。
        '''
        try:
            # TODO :
            self.logger.info(u'KVS上のユーザー情報を更新します。')
        except Exception as e:
            self.logger.error(e.__class__)
            self.logger.error(e)


class UserDelete():
    '''
      ユーザー情報を削除するクラス。
    '''
    # ロガー
    logger = logging.getLogger('logExample')

    def __init__(self):
        try:
            # 設定ファイルのロード
            self.config = ConfigParser.SafeConfigParser()
            self.config.read(os.path.dirname(os.path.abspath(__file__)) + '/../api.conf')
        except Exception as e:
            self.logger.error(e.__class__)
            self.logger.error(e)

    def delete(self, request):
        '''
          KVS上のユーザー情報を削除します。
        '''
        try:
            # TODO :
            self.logger.info(u'KVS上のユーザー情報を削除します。')
        except Exception as e:
            self.logger.error(e.__class__)
            self.logger.error(e)


# 後処理 {{{
# }}}
