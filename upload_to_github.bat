@echo off
chcp 65001 > nul
echo ========================================
echo   Загрузка StroiNadzor на GitHub
echo ========================================
echo.
echo GitHub Username: AntonKuznetsov1911
echo Repository: StroiNadzor
echo.
echo ========================================
echo   Шаг 1: Создание репозитория
echo ========================================
echo.
echo Откройте в браузере:
echo https://github.com/new
echo.
echo Заполните:
echo   - Repository name: StroiNadzor
echo   - Description: AI консультант по строительным нормативам
echo   - Public/Private: на ваш выбор
echo   - НЕ создавайте README, .gitignore, license
echo.
echo Нажмите Enter после создания репозитория...
pause > nul
echo.
echo ========================================
echo   Шаг 2: Загрузка кода
echo ========================================
echo.
cd /d "%~dp0"
git remote add origin https://github.com/AntonKuznetsov1911/StroiNadzor.git
git branch -M main
git push -u origin main
echo.
echo ========================================
echo   Готово!
echo ========================================
echo.
echo Ваш репозиторий:
echo https://github.com/AntonKuznetsov1911/StroiNadzor
echo.
pause
