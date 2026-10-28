@echo off
cd /d "%~dp0"
"C:\Program Files\Git\cmd\git.exe" fetch origin
"C:\Program Files\Git\cmd\git.exe" checkout scenebiscuit-cell-improve-ai-triage-prompt
python triage.py --backend ollama --model qwen2.5:14b --eval --tickets data/holdout_tickets.json --labels data/holdout_labels.json --out output/holdout-ai-v2
python triage.py --backend ollama --model qwen2.5:14b --eval --tickets data/fresh_tickets.json --labels data/fresh_labels.json --out output/fresh-ai
"C:\Program Files\Git\cmd\git.exe" add output/holdout-ai-v2 output/fresh-ai
"C:\Program Files\Git\cmd\git.exe" commit -m "Add AI v2 results"
"C:\Program Files\Git\cmd\git.exe" push
pause