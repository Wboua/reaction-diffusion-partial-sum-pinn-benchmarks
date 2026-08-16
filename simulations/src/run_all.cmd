@echo off
cd /d "%~dp0"
python run_study.py --mode publication
python reference_convergence.py
python run_ablations.py
python make_article_diagnostics.py
