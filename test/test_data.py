# -*- coding: utf-8 -*-

# 説明 {{{
'''
  テスト用のJSON形式データ。
'''
# }}}

# 標準モジュールのインポート {{{
# }}}

# サードパーティーモジュールのインポート {{{
# }}}

# 独自モジュールのインポート {{{
# }}}

# 前処理 {{{
# }}}
account = {
    # ユーザーID : aaaa, パスワード : '1111'
    'aaaa' : {
        'result_code'    : 200,
        'result_message' : '正常終了',
        'response_data'  : {
            'user_auth_key' : 'aaaa', # ユーザー認証キー
            'unit_error' : {
                '200' : '正常終了'
            }
        }
    },
    # ユーザーID : bbbb, パスワード : '2222'
    'bbbb' : {
        'result_code'    : 200,
        'result_message' : '正常終了',
        'response_data'  : {
            'user_auth_key' : 'bbbb', # ユーザー認証キー
            'unit_error' : {
                '200' : '正常終了'
            }
        }
    }
}
user = {
    'aaaa' : { # ユーザー認証キー
        'result_code'    : 200,
        'result_message' : '正常終了',
        'response_data'  : {
            'user_id' : 'P111111',
            'name' : 'aaaa',
            'affiliation_group' : ['技術部', 'システム開発課'],
            'managerial_position' : ['一般社員', 'グルーワークリーダー'],
            'mail_address' : ['bbbb@example.com', 'bbbb@example.co.jp'],
            'unit_error' : {
                '200' : '正常終了'
            }
        }
    },
    'bbbb' : { # ユーザー認証キー
        'result_code'    : 200,
        'result_message' : '正常終了',
        'response_data'  : {
            'user_id' : 'P111111',
            'name' : 'bbbb',
            'affiliation_group' : ['技術部', 'システム開発課'],
            'managerial_position' : ['一般社員', 'グルーワークメンバー'],
            'mail_address' : ['bbbb@example.com', 'bbbb@example.co.jp'],
            'unit_error' : {
                '200' : '正常終了'
            }
        }
    }
}

# 後処理 {{{{
# }}}
