@echo off
REM クイズアプリ起動スクリプト（Windows用、Docker Compose使用）

REM スクリプトのディレクトリからプロジェクトルートに移動
cd /d "%~dp0\.."

REM Dockerがインストールされているか確認
where docker >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo エラー: Dockerがインストールされていません。
    echo Dockerのインストール方法: https://docs.docker.com/get-docker/
    exit /b 1
)

REM Docker Composeコマンドの確認
docker compose version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    set DOCKER_COMPOSE_CMD=docker compose
) else (
    docker-compose version >nul 2>&1
    if %ERRORLEVEL% EQU 0 (
        set DOCKER_COMPOSE_CMD=docker-compose
    ) else (
        echo エラー: Docker Composeがインストールされていません。
        echo Docker Composeのインストール方法: https://docs.docker.com/compose/install/
        exit /b 1
    )
)

REM データベースが存在しない場合は初期化（初回起動時）
REM 注意: app.pyで自動的に初期化されるため、ここではスキップ
REM 手動で初期化する場合は以下を実行:
REM %DOCKER_COMPOSE_CMD% exec web poetry run python -m app.data.init_questions

REM アプリケーションを起動
echo クイズアプリを起動します...
echo ブラウザで http://localhost:5000 にアクセスしてください。
echo 停止するには Ctrl+C を押すか、別のコマンドプロンプトで stop.bat を実行してください。
echo.

%DOCKER_COMPOSE_CMD% -f docker/docker-compose.yml up

