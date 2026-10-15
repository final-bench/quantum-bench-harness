# FINAL-Bench Quantum — evaluation harness (open)

[![Leaderboard](https://img.shields.io/badge/Leaderboard-HF%20Space-2563eb)](https://huggingface.co/spaces/FINAL-Bench/quantum-bench-leaderboard)
[![Open Quantum Challenge](https://img.shields.io/badge/Open%20Quantum%20Challenge-Join-06b6d4)](https://huggingface.co/spaces/FINAL-Bench/quantum-bench-leaderboard)
[![Harness](https://img.shields.io/badge/Harness-GitHub-181717?logo=github)](https://github.com/final-bench/quantum-bench-harness)

Reproducible scoring code and **frozen** test problems for the FINAL-Bench Quantum leaderboard.
Everything here is the **evaluation layer**: anyone can run it and obtain the same numbers shown on the
leaderboard (Track A). Competitive methods (our neural decoder weights, private solver engines) are **not**
part of this repo — a leaderboard is only trustworthy when its yardstick is public, so the yardstick is open
and the contestants' secret sauce stays with them.

Leaderboard: https://huggingface.co/spaces/FINAL-Bench/quantum-bench-leaderboard

## What is here
- `bench_qec.py` — surface-code decoder scoring (logical error rate + 95% Wilson CI) with standard decoders
  (PyMatching / BP+OSD). Distance scaling and threshold study.
- `bench_vqe.py` — molecular VQE scoring: ground-state energy error vs exact diagonalization (FCI).
- `frozen/surface_d5.py` — the **frozen** circuit generator (fixed distance, rounds, noise, seed) every QEC
  submission is scored against.
- `score_predictions.py` — score a submitted prediction file against the frozen ground truth (no code execution).

## Reproduce
```
pip install -r requirements.txt
python bench_qec.py          # prints LER + CI for d=3,5,7
python bench_vqe.py          # prints H2 VQE error vs FCI
```
Numbers match the leaderboard's Track A. Measurement-gated: controls + confidence intervals, no cherry-picking.

## Scope / honesty
- Current stage is **emulator / simulation**. No claim of quantum advantage, below-threshold real hardware,
  or fault-tolerant QEC. Real-hardware entries are labeled separately on the board.
- Track A = reproducible self-measurement here. Track B = published literature (cited, different setups).

## NOT in this repo (by design)
- Any competitive method's internals (e.g. a neural-ensemble decoder's weights / training data).
- Private solver or scoring engines.
- Credentials, tokens, or participant contact data.

## Open Quantum Challenge (OQC)

A vendor-neutral, fully reproducible challenge you can enter with **only a GPU and this harness — no quantum
hardware**. Answer keys are held privately; every submission is auto-scored against a frozen ground truth, so
the ranking is reproducible and hardware-independent. Live board + Submit: the leaderboard Space above
(**🏆 Open Quantum Challenge** tab).

| Season | Track | Opens | Deadline | Prize |
|--------|-------|-------|----------|-------|
| **1** | **Quantum Simulation** — Fermi-Hubbard ground-state energy (lowest total energy wins; report all systems) | 2026-10-11 | **2027-02-28** | $1,000 (🥇600 / 🥈300 / 🥉100) |
| **2** | **QEC Decoder** — rotated surface code d=5, p=0.005 (logical error rate, lower wins) | 2026-10-11 | **2027-03-31** | $1,000 (🥇600 / 🥈300 / 🥉100) |

Public inputs: **`FINAL-Bench/oqc-data`** (HF dataset).
- Season 1: `qsim/systems.json` — lattice, U/t and qubit count per system. Report each ground-state energy.
- Season 2: `qec/detectors.npy` (shots × detectors) + `qec/dem.txt` (stim DetectorErrorModel). Decode each shot.

Submit a JSON `{ "hf_user": "...", "method": "...", "predictions": { "<item_id>": value } }` via the Space's
Submit tab. A background worker scores it against the private key and updates the ranked table automatically.

## License
Code: MIT. Benchmark data / leaderboard content: CC-BY-NC-4.0.
