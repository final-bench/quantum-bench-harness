# -*- coding: utf-8 -*-
"""VQE scoring: ground-state energy error vs exact diagonalization (FCI) for H2 / STO-3G (4 qubit).
Generic hardware-efficient ansatz (Ry layers + CX ladder), numpy statevector. Standard; no private solver.
"""
import numpy as np, math
from scipy.optimize import minimize
from openfermionpyscf import run_pyscf
from openfermion import MolecularData, get_fermion_operator, jordan_wigner, get_sparse_operator

N = 4
X = np.array([[0,1],[1,0]], complex); P0 = np.array([[1,0],[0,0]], complex); P1 = np.array([[0,0],[0,1]], complex); I2 = np.eye(2, dtype=complex)
def kron(ms):
    o = ms[0]
    for m in ms[1:]: o = np.kron(o, m)
    return o
def op1(g, q): return kron([g if i == q else I2 for i in range(N)])
def cx(c, t): return kron([P0 if i == c else I2 for i in range(N)]) + kron([P1 if i == c else (X if i == t else I2) for i in range(N)])
def ry(a):
    s, co = math.sin(a/2), math.cos(a/2); return np.array([[co, -s], [s, co]], complex)
CXL = [cx(q, q+1) for q in range(N-1)]
def ansatz(p, reps=3):
    psi = np.zeros(2**N, complex); psi[0] = 1.0; k = 0
    for _ in range(reps):
        for q in range(N): psi = op1(ry(p[k]), q) @ psi; k += 1
        for g in CXL: psi = g @ psi
    for q in range(N): psi = op1(ry(p[k]), q) @ psi; k += 1
    return psi

if __name__ == "__main__":
    mol = run_pyscf(MolecularData([("H",(0,0,0)),("H",(0,0,0.7414))], "sto-3g", 1, 0), run_scf=True, run_fci=True)
    H = get_sparse_operator(jordan_wigner(get_fermion_operator(mol.get_molecular_hamiltonian())), n_qubits=N).toarray()
    exact = float(np.linalg.eigvalsh(H)[0]); reps = 3; npar = N*(reps+1)
    f = lambda p: float(np.real(np.vdot(ansatz(p, reps), H @ ansatz(p, reps))))
    best = min((minimize(f, np.random.default_rng(s).uniform(-np.pi, np.pi, npar), method="COBYLA",
                options={"maxiter":4000}) for s in range(12)), key=lambda r: r.fun)
    print("H2/STO-3G 4-qubit VQE (hardware-efficient ansatz)")
    print("FCI        : %.8f Ha" % float(mol.fci_energy))
    print("VQE        : %.8f Ha" % best.fun)
    print("error      : %.5f mHa  (chemical accuracy = 1.6 mHa)" % ((best.fun - exact)*1000))
