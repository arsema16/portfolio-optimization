Write-Host "=== Pushing All Tasks to Respective Branches ===" -ForegroundColor Cyan

# Task 1
Write-Host "`nPushing Task 1..." -ForegroundColor Yellow
git checkout task1-data-exploration
git add notebooks/01_data_exploration.ipynb run_task1.py interim_report.md
git commit -m "Task 1: Data extraction, EDA, stationarity testing, and risk metrics" -ErrorAction SilentlyContinue
git push origin task1-data-exploration
Write-Host "✓ Task 1 pushed" -ForegroundColor Green

# Task 2
Write-Host "`nPushing Task 2..." -ForegroundColor Yellow
git checkout task2-arima-model
git add notebooks/02_arima_model.ipynb run_task2.py
git commit -m "Task 2: ARIMA model implementation, optimization, and evaluation" -ErrorAction SilentlyContinue
git push origin task2-arima-model
Write-Host "✓ Task 2 pushed" -ForegroundColor Green

# Task 3
Write-Host "`nPushing Task 3..." -ForegroundColor Yellow
git checkout task3-forecasting
git add notebooks/03_forecasting.ipynb
git commit -m "Task 3: Future trend forecasting with confidence intervals" -ErrorAction SilentlyContinue
git push origin task3-forecasting
Write-Host "✓ Task 3 pushed" -ForegroundColor Green

# Task 4
Write-Host "`nPushing Task 4..." -ForegroundColor Yellow
git checkout task4-portfolio-optimization
git add notebooks/04_portfolio_optimization.ipynb
git commit -m "Task 4: Portfolio optimization using Modern Portfolio Theory" -ErrorAction SilentlyContinue
git push origin task4-portfolio-optimization
Write-Host "✓ Task 4 pushed" -ForegroundColor Green

# Task 5
Write-Host "`nPushing Task 5..." -ForegroundColor Yellow
git checkout task5-backtesting
git add notebooks/05_backtesting.ipynb
git commit -m "Task 5: Strategy backtesting against 60/40 benchmark" -ErrorAction SilentlyContinue
git push origin task5-backtesting
Write-Host "✓ Task 5 pushed" -ForegroundColor Green

# Merge to main
Write-Host "`nMerging all tasks to main..." -ForegroundColor Yellow
git checkout main
git merge task1-data-exploration -m "Merge Task 1" -ErrorAction SilentlyContinue
git merge task2-arima-model -m "Merge Task 2" -ErrorAction SilentlyContinue
git merge task3-forecasting -m "Merge Task 3" -ErrorAction SilentlyContinue
git merge task4-portfolio-optimization -m "Merge Task 4" -ErrorAction SilentlyContinue
git merge task5-backtesting -m "Merge Task 5" -ErrorAction SilentlyContinue
git push origin main

Write-Host "`n=== All Tasks Pushed Successfully! ===" -ForegroundColor Green
git branch -a
