@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ========================================
echo 開始部署到 Vercel
echo ========================================
echo.

echo [1/3] 添加修改的文件...
if exist ".git\index.lock" (
    echo 偵測到 Git 鎖定文件，正在清除...
    del /f /q ".git\index.lock"
    echo ✓ 已清除鎖定文件
)
git add .
if %errorlevel% neq 0 (
    echo 錯誤：無法添加文件
    echo 提示：請確認沒有其他 Git 操作正在進行
    pause
    exit /b 1
)
echo ✓ 文件已添加
echo.

echo [2/3] 提交變更...
git commit -m "更新牌位系統"
if %errorlevel% neq 0 (
    echo 注意：可能沒有新的變更需要提交
)
echo ✓ 變更已提交
echo.

echo [3/3] 推送到 Git 並觸發 Vercel 自動部署...
git push origin main
if %errorlevel% neq 0 (
    echo 嘗試推送到 master 分支...
    git push origin master
    if %errorlevel% neq 0 (
        echo 錯誤：推送失敗，請檢查：
        echo   1. 是否已設定 Git 遠端倉庫
        echo   2. 是否有網路連線
        echo   3. 是否有推送權限
        pause
        exit /b 1
    )
)
echo ✓ 已推送到 Git
echo.

echo ========================================
echo 部署完成！
echo Vercel 會自動偵測到變更並開始部署
echo.
echo 提示：
echo   - 到 https://vercel.com 查看部署狀態
echo   - 部署通常需要 1-2 分鐘完成
echo ========================================
echo.
pause

