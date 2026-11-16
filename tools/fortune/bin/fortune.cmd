@echo off
rem Hidden SWE-agent Easter egg. Not enabled in default configs.
rem Windows wrapper so `fortune` can run when bash is missing.
setlocal
where python >nul 2>&1
if %ERRORLEVEL%==0 (
  python "%~dp0fortune.py" %*
  exit /b %ERRORLEVEL%
)
where python3 >nul 2>&1
if %ERRORLEVEL%==0 (
  python3 "%~dp0fortune.py" %*
  exit /b %ERRORLEVEL%
)
echo fortune: Python is required to run this Easter egg. 1>&2
exit /b 1
