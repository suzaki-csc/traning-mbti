#!/usr/bin/env python
"""
Flaskアプリケーションのエントリーポイント

このファイルは、Flaskアプリケーションを起動するためのメインファイルです。
開発環境と本番環境の両方で使用できます。
"""

from app import create_app

# Flaskアプリケーションのインスタンスを作成
app = create_app()

if __name__ == '__main__':
    # 開発環境での起動
    # 本番環境ではGunicornなどのWSGIサーバーを使用
    app.run(host='0.0.0.0', port=5000, debug=True)

