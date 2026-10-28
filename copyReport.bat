set "REPORTS_DIR=reports"
set "DEST=allure-results"
:: Find the latest date folder under reports (sorted by name descending)
for /f "delims=" %%d in ('dir "%REPORTS_DIR%" /ad /b /o-n 2^>nul') do (
    set "DATE_DIR=%%d"
    goto :find_time
)
:find_time
if "%DATE_DIR%"=="" (
    echo [ERROR] No date folder found under %REPORTS_DIR%
)
:: Find the latest time folder under the date folder
for /f "delims=" %%t in ('dir "%REPORTS_DIR%\%DATE_DIR%" /ad /b /o-n 2^>nul') do (
    set "TIME_DIR=%%t"
    goto :copy_files
)
:copy_files
if "%TIME_DIR%"=="" (
    echo [ERROR] No time folder found under %REPORTS_DIR%\%DATE_DIR%
)
set "SOURCE=%REPORTS_DIR%\%DATE_DIR%\%TIME_DIR%\allure\raw"
echo ========================================
echo   Allure Report Copier
echo ========================================
echo.
echo Project Dir: %CD%
echo Source:      %SOURCE%
echo Dest:        %DEST%
echo.
:: Check if source exists
if not exist "%SOURCE%" (
    echo [ERROR] Source path does not exist: %SOURCE%
)
:: Create destination directory if not exists
if not exist "%DEST%" mkdir "%DEST%"
:: Copy all files
echo Copying files...
xcopy "%SOURCE%\*" "%DEST%" /Y
echo.
echo [DONE] Files copied successfully!
echo.
echo Source: %SOURCE%
echo Dest:   %DEST%
