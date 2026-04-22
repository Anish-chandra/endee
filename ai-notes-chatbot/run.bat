@echo off
call venv\Scripts\activate.bat
pip install -r requirements.txt
uvicorn main:app --reload
pause
