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
user = {
    'aaaa' : {
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
    'bbbb' : {
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
    },
    'cccc' : {
        'result_code'    : 200,
        'result_message' : '正常終了',
        'response_data'  : {
            'user_id' : '',
            'name' : 'cccc',
            'affiliation_group' : [],
            'managerial_position' : [],
            'mail_address' : [],
            'unit_error' : {
                '400' : 'アクセストークン不正'
            }
        }
    }
}

# 後処理 {{{{
# }}}
