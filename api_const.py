# -*- coding: utf-8 -*-

# 説明 {{{
'''
  p_auth_api(認証API)用の定数モジュール
'''
# }}}

# 標準モジュールのインポート {{{
import sys
import os
import json
# }}}

# サードパーティーモジュールのインポート {{{
# }}}

# 独自モジュールのインポート {{{
# }}}

# 前処理 {{{
# }}}

class Result(object) :
    SUCCESS_001 = {'code' : 'SUCCESS_001', 'message' : u'正常終了'}

# エラー
class Error(object):
    SUCCESS_001 = {'code' : 'SUCCESS_001', 'message' : u'正常終了'}
    ERROR_001   = {'code' : 'ERROR_001',   'message' : u'アクセストークン不正'}
    ERROR_002   = {'code' : 'ERROR_002',   'message' : u'認証エラー'}
    ERROR_003   = {'code' : 'ERROR_003',   'message' : u'KVSへのデータ登録時に異常発生'}
    WARN_001    = {'code' : 'WARN_001',    'message' : u'警告'}

# 後処理 {{{
# }}}

