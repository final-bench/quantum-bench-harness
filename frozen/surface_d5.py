# -*- coding: utf-8 -*-
"""Frozen surface-code test circuits for the FINAL-Bench Quantum QEC event.
These definitions are FIXED (do not change) so every submission is scored on the identical problem.
Rotated surface code, memory Z, rounds = distance, circuit-level depolarizing noise on all channels = p.
"""
import stim

def frozen_circuit(p, d=5):
    return stim.Circuit.generated(
        "surface_code:rotated_memory_z", distance=d, rounds=d,
        after_clifford_depolarization=p,
        before_round_data_depolarization=p,
        before_measure_flip_probability=p,
        after_reset_flip_probability=p,
    )

# Frozen scoring points and sampler seed (fixed).
FROZEN_P = [0.002, 0.003, 0.004, 0.005, 0.007, 0.01]
FROZEN_SEED = 13
FROZEN_SHOTS = 40000
