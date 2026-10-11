# -*- coding: utf-8 -*-
"""QEC decoder scoring: logical error rate (LER) + 95% Wilson CI on the frozen surface-code problem.
Standard decoders only (PyMatching MWPM, BP+OSD). Distance scaling d=3,5,7 and threshold study.
"""
import math, numpy as np, stim, pymatching
from frozen.surface_d5 import frozen_circuit, FROZEN_SEED

def wilson(k, n, z=1.96):
    if n == 0: return (0.0, 0.0)
    p = k/n; d = 1+z*z/n; c = p+z*z/(2*n); h = z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))
    return ((c-h)/d, (c+h)/d)

def mwpm_ler(p, d, shots=20000):
    c = frozen_circuit(p, d); dem = c.detector_error_model(decompose_errors=True)
    det, obs = c.compile_detector_sampler(seed=FROZEN_SEED).sample(shots, separate_observables=True)
    m = pymatching.Matching.from_detector_error_model(dem)
    err = int(np.sum(m.decode_batch(det)[:, 0] != obs[:, 0]))
    lo, hi = wilson(err, shots)
    return err/shots, lo, hi

if __name__ == "__main__":
    print("QEC surface-code (frozen), PyMatching MWPM, 20k shots, 95% Wilson CI")
    print("%6s %4s %10s %22s" % ("p", "d", "LER", "95% CI"))
    for p in (0.002, 0.005, 0.007):
        for d in (3, 5, 7):
            ler, lo, hi = mwpm_ler(p, d)
            print("%6.3f %4d %10.5f   [%.5f, %.5f]" % (p, d, ler, lo, hi))
