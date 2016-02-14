# -*- coding: utf-8 -*-

# 説明 {{{
'''
  認証API共通の関数定義
'''
# }}}

# 標準モジュールのインポート {{{
import sys
import os
import json
import ConfigParser
# }}}

# サードパーティーモジュールのインポート {{{
# }}}

# 独自モジュールのインポート {{{
# }}}

# 前処理 {{{
# }}}

def get_test_mode(instance):
    for test in instance.config.items('test'):
        if test[0] == 'mode':
            return test[1]

# 後処理 {{{
# }}}
