@echo off

cd %~dp0

echo Hello Miss Tang,
echo       Welcome to TANGTANG WORD COUNTER
echo.

echo Now! Please enter the words you want to counter:
set /p input_words=
echo Counting...
call python word_counter.py README.txt -w "%input_words%"

echo.
echo The result has been written to %cd%\words_frequency.csv
echo.
pause