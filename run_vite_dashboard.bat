@echo off
echo ========================================
echo Device Analytics Dashboard
echo Vite Dev Server
echo ========================================
echo.
echo Installing dependencies (first time only)...
call npm install
echo.
echo Starting Vite dev server...
echo The dashboard will open automatically in your browser
echo.
echo Features:
echo  - Hot Module Replacement (HMR)
echo  - Fast refresh on code changes
echo  - Better error messages
echo.
echo Press Ctrl+C to stop the server
echo.
call npm run dev
pause

