# -*- coding: utf-8 -*-
"""Score a submitted QEC prediction file against the frozen ground truth (no code execution).
Submission format: a .npy int array of predicted logical observable (0/1), one per shot, aligned to the
frozen detector sampler (seed, shot count). Outputs LER + 95% Wilson CI.
Usage: python score_predictions.py predictions.npy --p 0.005 --d 5
"""
import argparse, math, numpy as np
from frozen.surface_d5 import frozen_circuit, FROZEN_SEED, FROZEN_SHOTS

def wilson(k, n, z=1.96):
    p=k/n; d=1+z*z/n; c=p+z*z/(2*n); h=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n)); return ((c-h)/d,(c+h)/d)

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("pred"); ap.add_argument("--p", type=float, default=0.005); ap.add_argument("--d", type=int, default=5); ap.add_argument("--shots", type=int, default=FROZEN_SHOTS)
    a = ap.parse_args()
    c = frozen_circuit(a.p, a.d)
    _, obs = c.compile_detector_sampler(seed=FROZEN_SEED).sample(a.shots, separate_observables=True)
    y = obs[:, 0].astype(int)
    pred = np.load(a.pred).astype(int).ravel()[:a.shots]
    assert len(pred) == a.shots, "prediction length %d != frozen shots %d" % (len(pred), a.shots)
    err = int(np.sum(pred != y)); lo, hi = wilson(err, a.shots)
    # leakage guard: implausibly-perfect agreement flagged
    ler = err/a.shots
    print("submitted LER: %.5f  95%% CI [%.5f, %.5f]  (n=%d)" % (ler, lo, hi, a.shots))
    if ler < 1e-4: print("WARNING: near-zero error - organizer will re-verify for leakage.")
