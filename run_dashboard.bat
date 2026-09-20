@echo off
echo ========================================
echo  IPL Cricket Data Analytics Dashboard
echo ========================================
echo.
echo Step 1: Running data analysis pipeline...
"C:\Users\Dell\AppData\Local\Programs\Python\Python311\python.exe" analysis\data_analysis.py
if %errorlevel% neq 0 (
    echo ERROR: Data analysis failed.
    pause
    exit /b 1
)
echo.
echo Step 2: Launching Streamlit dashboard...
echo Open your browser at http://localhost:8501
echo.
"C:\Users\Dell\AppData\Local\Programs\Python\Python311\python.exe" -m streamlit run frontend\app.py
pause
