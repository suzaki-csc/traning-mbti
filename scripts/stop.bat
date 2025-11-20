@echo off
REM クイズアプリ停止スクリプト（Windows用、Docker Compose使用）

REM スクリプトのディレクトリからプロジェクトルートに移動
cd /d "%~dp0\.."

REM Docker Composeコマンドの確認
docker compose version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    set DOCKER_COMPOSE_CMD=docker compose
) else (
    set DOCKER_COMPOSE_CMD=docker-compose
)

echo クイズアプリを停止します...

REM コンテナを停止
%DOCKER_COMPOSE_CMD% -f docker/docker-compose.yml down

echo クイズアプリが停止しました。

