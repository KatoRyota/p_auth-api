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
import re
import pprint
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

def to_json_for_sqlalchemy(obj_list):
    """ Returns a JSON representation of an SQLAlchemy-backed object.
    """
    result = []
    if (isinstance(obj_list, list)):
        # 複数オブジェクトの場合
        # オブジェクトリスト分ループして、オブジェクト毎に処理
        for i, obj in enumerate(obj_list):
            column_obj = {}
            for column in obj._sa_class_manager.mapper.mapped_table.columns:
                column_obj[column.name] = getattr(obj, column.name)
            result.append(column_obj)
    else:
        # 単一オブジェクトの場合
        obj = obj_list
        column_obj = {}
        for column in obj._sa_class_manager.mapper.mapped_table.columns:
            column_obj[column.name] = getattr(obj, column.name)
        result.append(column_obj)

    return json.dumps(result, ensure_ascii=False, indent=4)

def pp(obj):
    pp = pprint.PrettyPrinter(indent=4, width=160)
    str = pp.pformat(obj)
    return re.sub(r"\\u([0-9a-f]{4})", lambda x: unichr(int("0x"+x.group(1), 16)), str)


# 後処理 {{{
# }}}
