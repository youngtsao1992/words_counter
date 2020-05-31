@echo off

cd %~dp0

echo Select run type: 0-SHELL 1-GUI
set /p run= 

if %run% EQU 1 goto :UI

echo Hello Miss Tang,
echo       Welcome to TANGTANG WORD COUNTER
echo.

echo Now! 1/2 Please enter the input file path:
set /p input_file=
echo 2/2 Please enter the words you want to counter:
set /p input_words=
echo Counting...
call python word_counter.py "%input_file%" -w "%input_words%"
pause

:UI
call python word_counter_ui.py

:EOF
