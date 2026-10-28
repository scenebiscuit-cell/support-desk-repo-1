# AI triage on the unseen tickets

Model: **Qwen 2.5 14B** running locally through Ollama on an AMD RX 9070 (ticket data never left the machine). Run on 2026-10-27:

```
python triage.py --backend ollama --model qwen2.5:14b --eval --tickets data/holdout_tickets.json --labels data/holdout_labels.json --out output/holdout
```

| Engine | Category | Priority |
|---|---|---|
| Keyword rules | 78% (28/36) | 72% (26/36) |
| **Qwen 2.5 14B** | **83% (30/36)** | **78% (28/36)** |

- Fixed by the AI: H-10 (board named "Refund Requests" is a setup question), H-11 (billed for wrong plan → refund), H-14 (seat overcharge → refund).
- New AI miss: H-01 ("Everything is read-only" after an expired card → outage; should be billing).
- Missed by both: H-02 and H-25 (feature requests phrased as questions), H-34 (notification complaint with a churn threat), **H-12 and H-35 (suspicious logins → should be security)**.

`summary.json` has the per-ticket category, priority, and macro from the run, scored against `data/holdout_labels.json`. The page's accuracy chart reads it at build time.
