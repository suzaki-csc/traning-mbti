@echo off
REM ##############################################################################
REM パスワード強度チェッカー - 起動スクリプト（Docker Compose版 - Windows用）
REM
REM このスクリプトは、Docker Composeを使用してパスワード強度チェッカーを起動します。
REM Docker環境のチェック、イメージのビルド、コンテナの起動を自動で行います。
REM ##############################################################################

chcp 65001 > nul
setlocal enabledelayedexpansion

REM スクリプトのディレクトリに移動
cd /d %~dp0

REM 引数を取得（デフォルトはstart）
set ACTION=%1
if "%ACTION%"=="" set ACTION=start

REM アクションに応じて処理を分岐
if /i "%ACTION%"=="start" goto START_APP
if /i "%ACTION%"=="stop" goto STOP_APP
if /i "%ACTION%"=="restart" goto RESTART_APP
if /i "%ACTION%"=="logs" goto SHOW_LOGS
if /i "%ACTION%"=="status" goto SHOW_STATUS
if /i "%ACTION%"=="build" goto REBUILD_APP
if /i "%ACTION%"=="clean" goto CLEAN_APP
if /i "%ACTION%"=="help" goto SHOW_HELP
if /i "%ACTION%"=="-h" goto SHOW_HELP
if /i "%ACTION%"=="--help" goto SHOW_HELP

echo [エラー] 不明なオプション '%ACTION%'
echo.
goto SHOW_HELP

:SHOW_HELP
echo ================================================================
echo   パスワード強度チェッカー - Docker Compose版
echo ================================================================
echo.
echo 使用方法: %~nx0 [オプション]
echo.
echo オプション:
echo   start       アプリケーションを起動（デフォルト）
echo   stop        アプリケーションを停止
echo   restart     アプリケーションを再起動
echo   logs        ログを表示
echo   status      コンテナの状態を確認
echo   build       イメージを再ビルド
echo   clean       コンテナとイメージを削除
echo   help        このヘルプを表示
echo.
pause
exit /b 0

:START_APP
echo ================================================================
echo   パスワード強度チェッカー - Docker Compose版
echo ================================================================
echo.

REM Dockerがインストールされているかチェック
echo [1/3] Docker環境をチェック中...

where docker >nul 2>&1
if %errorlevel% neq 0 (
    echo [エラー] Dockerがインストールされていません
    echo 以下のURLからDockerをインストールしてください:
    echo https://docs.docker.com/get-docker/
    pause
    exit /b 1
)

REM Dockerデーモンが起動しているかチェック
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo [エラー] Dockerデーモンが起動していません
    echo Docker Desktopを起動してください
    pause
    exit /b 1
)

docker --version

REM Docker Composeがインストールされているかチェック
docker compose version >nul 2>&1
if %errorlevel% equ 0 (
    set DOCKER_COMPOSE=docker compose
    docker compose version
) else (
    where docker-compose >nul 2>&1
    if %errorlevel% neq 0 (
        echo [エラー] Docker Composeがインストールされていません
        pause
        exit /b 1
    )
    set DOCKER_COMPOSE=docker-compose
    docker-compose --version
)
echo.

REM 必要なファイルが存在するかチェック
echo [2/3] 必要なファイルをチェック中...
set FILES_OK=1

if exist "Dockerfile" (
    echo   [OK] Dockerfile
) else (
    echo   [NG] Dockerfile が見つかりません
    set FILES_OK=0
)

if exist "docker-compose.yml" (
    echo   [OK] docker-compose.yml
) else (
    echo   [NG] docker-compose.yml が見つかりません
    set FILES_OK=0
)

if exist "password_checker_app.py" (
    echo   [OK] password_checker_app.py
) else (
    echo   [NG] password_checker_app.py が見つかりません
    set FILES_OK=0
)

if exist "templates\password_checker.html" (
    echo   [OK] templates\password_checker.html
) else (
    echo   [NG] templates\password_checker.html が見つかりません
    set FILES_OK=0
)

if exist "static\css\password_style.css" (
    echo   [OK] static\css\password_style.css
) else (
    echo   [NG] static\css\password_style.css が見つかりません
    set FILES_OK=0
)

if exist "static\js\password_checker.js" (
    echo   [OK] static\js\password_checker.js
) else (
    echo   [NG] static\js\password_checker.js が見つかりません
    set FILES_OK=0
)
echo.

if %FILES_OK%==0 (
    echo [エラー] 必要なファイルが不足しています
    pause
    exit /b 1
)

REM アプリケーションを起動
echo [3/3] アプリケーションを起動中...
echo.

REM 既存のコンテナをチェック
docker ps --format "{{.Names}}" | findstr /C:"password_checker_app" >nul 2>&1
if %errorlevel% equ 0 (
    echo 既存のコンテナを停止します...
    %DOCKER_COMPOSE% down
    timeout /t 2 /nobreak >nul
)

REM Dockerイメージをビルド
echo Dockerイメージをビルド中...
%DOCKER_COMPOSE% build
if %errorlevel% neq 0 (
    echo [エラー] イメージのビルドに失敗しました
    pause
    exit /b 1
)

echo.
echo コンテナを起動中...
%DOCKER_COMPOSE% up -d
if %errorlevel% neq 0 (
    echo [エラー] コンテナの起動に失敗しました
    pause
    exit /b 1
)

REM 起動待機
echo.
echo アプリケーションの起動を待機中...
timeout /t 3 /nobreak >nul

REM ヘルスチェック
set STARTED=0
for /L %%i in (1,1,10) do (
    curl -s http://localhost:5000/health >nul 2>&1
    if !errorlevel! equ 0 (
        echo [OK] アプリケーションが正常に起動しました
        set STARTED=1
        goto START_SUCCESS
    )
    timeout /t 1 /nobreak >nul
)

if %STARTED%==0 (
    echo [警告] アプリケーションの起動確認がタイムアウトしました
    echo ログを確認してください: %~nx0 logs
)

:START_SUCCESS
echo.
echo ================================================================
echo パスワード強度チェッカーが起動しました
echo ================================================================
echo.
echo アクセスURL: http://localhost:5000
echo.
echo コマンド:
echo   %~nx0 stop     - アプリケーションを停止
echo   %~nx0 logs     - ログを表示
echo   %~nx0 status   - 状態を確認
echo.
echo ================================================================
pause
exit /b 0

:STOP_APP
echo ================================================================
echo   パスワード強度チェッカー - 停止
echo ================================================================
echo.
echo アプリケーションを停止中...

REM Docker Compose コマンドを判定
docker compose version >nul 2>&1
if %errorlevel% equ 0 (
    set DOCKER_COMPOSE=docker compose
) else (
    set DOCKER_COMPOSE=docker-compose
)

%DOCKER_COMPOSE% down

echo.
echo [OK] アプリケーションを停止しました
echo.
pause
exit /b 0

:RESTART_APP
echo ================================================================
echo   パスワード強度チェッカー - 再起動
echo ================================================================
echo.
call :STOP_APP
timeout /t 2 /nobreak >nul
goto START_APP

:SHOW_LOGS
echo ================================================================
echo   パスワード強度チェッカー - ログ表示
echo ================================================================
echo.
echo ログを表示します (Ctrl+C で終了)
echo.

docker compose version >nul 2>&1
if %errorlevel% equ 0 (
    set DOCKER_COMPOSE=docker compose
) else (
    set DOCKER_COMPOSE=docker-compose
)

%DOCKER_COMPOSE% logs -f
exit /b 0

:SHOW_STATUS
echo ================================================================
echo   パスワード強度チェッカー - 状態確認
echo ================================================================
echo.
echo コンテナの状態:
echo.

docker compose version >nul 2>&1
if %errorlevel% equ 0 (
    set DOCKER_COMPOSE=docker compose
) else (
    set DOCKER_COMPOSE=docker-compose
)

%DOCKER_COMPOSE% ps
echo.

REM ヘルスチェック
curl -s http://localhost:5000/health >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] アプリケーションは正常に動作しています
    echo   URL: http://localhost:5000
) else (
    echo [NG] アプリケーションにアクセスできません
)
echo.
pause
exit /b 0

:REBUILD_APP
echo ================================================================
echo   パスワード強度チェッカー - 再ビルド
echo ================================================================
echo.
echo イメージを再ビルド中...

docker compose version >nul 2>&1
if %errorlevel% equ 0 (
    set DOCKER_COMPOSE=docker compose
) else (
    set DOCKER_COMPOSE=docker-compose
)

%DOCKER_COMPOSE% build --no-cache

echo.
echo [OK] イメージを再ビルドしました
echo 変更を反映するには restart を実行してください
echo.
pause
exit /b 0

:CLEAN_APP
echo ================================================================
echo   パスワード強度チェッカー - クリーンアップ
echo ================================================================
echo.
echo [警告] コンテナとイメージを削除します
echo この操作は元に戻せません。続行しますか？ (Y/N)
set /p CONFIRM="> "

if /i not "%CONFIRM%"=="Y" (
    echo キャンセルしました
    pause
    exit /b 0
)

docker compose version >nul 2>&1
if %errorlevel% equ 0 (
    set DOCKER_COMPOSE=docker compose
) else (
    set DOCKER_COMPOSE=docker-compose
)

echo.
echo コンテナを停止中...
%DOCKER_COMPOSE% down

echo イメージを削除中...
docker rmi traning-mbti-password-checker 2>nul

echo.
echo [OK] クリーンアップが完了しました
echo.
pause
exit /b 0
