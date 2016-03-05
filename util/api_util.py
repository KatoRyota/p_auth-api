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

def to_json(model):
    """ Returns a JSON representation of an SQLAlchemy-backed object.
    """
    tmp_dict = {}
    tmp_dict['fields'] = {}
    tmp_dict['pk'] = getattr(model, 'id')

    for col in model._sa_class_manager.mapper.mapped_table.columns:
        json['fields'][col.name] = getattr(model, col.name)

    return json.dumps([json])


# 後処理 {{{
# }}}
