# -*- coding: utf-8 -*-

# 説明 {{{
'''
  p_auth_api(認証API)へのリクエストを制御して、domain配下のソースコードに処理を委譲し、処理結果を
  リクエスト元に返します。
'''
# }}}

# 標準モジュールのインポート {{{
import sys
import os
import json
import ConfigParser
import logging
import logging.config
from optparse import OptionParser
from functools import wraps
# }}}

# サードパーティーモジュールのインポート {{{
from flask import Flask, jsonify, request, url_for, abort, Response
# }}}

# 独自モジュールのインポート {{{
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/domain')
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/persistence')
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/util')
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/test')

from api_domain import UserCreate, UserRead, UserUpdate, UserDelete
# }}}

# 前処理 {{{
try:
  logging.config.fileConfig('logging.conf')

  api = Flask(__name__)
except Exception as e:
  print(e.__class__)
  print(e)
  exit()
# }}}

def before(content_type):
  '''
    models配下のソースコードに処理を委譲する前に、API共通の処理を行います。
  '''
  def _before(function):
    @wraps(function)
    def __before(*argv, **keywords):
      if request.headers['Content-Type'] != content_type:
        abort(400)
      return function(*argv, **keywords)
    return __before
  return _before


@api.route('/p_auth-api/create_user', methods=['POST'])
@before('application/json')
def create_user():
  logger = logging.getLogger('logExample')
  logger.info(u'api_service.create_user()開始')
  return UserCreate().create(request)


@api.route('/p_auth-api/read_user', methods=['POST'])
@before('application/json')
def read_user():
  logger = logging.getLogger('logExample')
  logger.info(u'api_service.read_user()開始')
  return UserRead().read(request)


@api.route('/p_auth-api/update_user', methods=['PUT'])
@before('application/json')
def update_user():
  logger = logging.getLogger('logExample')
  logger.info(u'api_service.update_user()開始')
  return UserUpdate().update(request)


@api.route('/p_auth-api/delete_user', methods=['DELETE'])
@before('application/json')
def delete_user():
  logger = logging.getLogger('logExample')
  logger.info(u'api_service.delete_user()開始')
  return UserDelete().delete(request)


def __parse_initialize_parameter():
  # 起動パラメータのパーサー生成
  parser = OptionParser()
  parser.add_option("-t", "--host", dest="host", help=u"ホスト名を指定して下さい。 ",
                    metavar="HOST", type="string")
  parser.add_option("-p", "--port", dest="port", help=u"ポート番号を指定して下さい。",
                    metavar="PORT", type="int")
  parser.add_option("--debug", dest="debug", help=u"サーバーがデバッグモードで起動します。",
                    action="store_true", default=False)

  # 起動パラメータのパース
  (options, args) = parser.parse_args()

  print(options.host) # debug

  # 起動パラメータ入力チェック
  if options.host is None or not options.host:
    parser.error(u"ホスト名が不正です。")
    parser.print_help()
    exit()

  if options.port is None or not options.port:
    parser.error(u"ポート番号が不正です。")
    parser.print_help()
    exit()

  if options.debug is None or not options.debug:
    print(u"debug mode : no")
  else:
    print(u"debug mode : yes")

  if len(args) != 0:
    parser.error(u"引数は指定できません。")
    parser.print_help()
    exit()


# 後処理 {{{
if __name__ == '__main__':
  __parse_initialize_parameter()
  api.run(host=options.host, port=options.port, debug=options.debug)
# }}}
