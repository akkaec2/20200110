@echo off
 
for /f %%i in ('dir /b *.csv') do (
    echo %%i
    type %%i>>result.csv
)
