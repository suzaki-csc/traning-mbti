"""
クイズアプリケーションパッケージ
"""
# app.pyとmodels.pyは同じディレクトリにあるため、直接インポート
# FLASK_APP=app.app:app で起動するため、ここではエクスポートのみ
from . import app
from . import models

__all__ = ['app', 'models']

