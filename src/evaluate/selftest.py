"""Checks that the agreement statistics reproduce known values.

  python src/evaluate/selftest.py

Linearly weighted kappa and Gwet's AC1/AC2 (stats.py) are checked on hand-computed cases,
including the kappa paradox.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from stats import gwet_ac2, weighted_kappa  # noqa: E402


def check(cond: bool, msg: str):
    print(("  ok   " if cond else "  FAIL ") + msg)
    if not cond:
        sys.exit(1)


def main():
    check(weighted_kappa([1, 1, 0.5, 0, 0], [1, 1, 0.5, 0, 0]) == 1.0, "weighted kappa: identical graders = 1")
    check(weighted_kappa([1, 1, 1, 0, 0], [0, 0, 0, 1, 1]) < 0, "weighted kappa: systematic disagreement < 0")
    check(abs(weighted_kappa([1, 0.5, 0, 1, 0.5, 0], [1, 0.5, 0.5, 1, 0, 0]) - 0.625) < 1e-9, "weighted kappa: mixed case = 0.625")
    # Gwet's AC1 on the kappa paradox: 90 items both graded 1, 5 graded (1, 0), 5 graded (0, 1).
    # Raw agreement 0.90; each rater marks 95% ones, so kappa's p_e = 0.95^2 + 0.05^2 = 0.905 and
    # kappa = (0.90 - 0.905) / 0.095 = -0.053, while AC1's p_e = 2 * 0.95 * 0.05 = 0.095 and
    # AC1 = (0.90 - 0.095) / 0.905 = 0.8895.
    xa = [1.0] * 95 + [0.0] * 5
    xb = [1.0] * 90 + [0.0] * 5 + [1.0] * 5
    ac1, se1 = gwet_ac2(xa, xb, levels=(0.0, 1.0))
    check(abs(ac1 - 0.805 / 0.905) < 1e-9 and weighted_kappa(xa, xb, levels=(0.0, 1.0)) < 0, "Gwet's AC1 on the kappa paradox: 0.890 where kappa is -0.053")
    check(0 < se1 < 0.1, f"Gwet's AC1 standard error is finite and small at n=100 ({se1:.4f})")
    check(gwet_ac2([1, 1, 0.5, 0, 0], [1, 1, 0.5, 0, 0])[0] == 1.0, "Gwet's AC2: identical graders = 1")
    check(gwet_ac2([1, 1, 1, 0, 0], [0, 0, 0, 1, 1])[0] < 0, "Gwet's AC2: systematic disagreement < 0")
    # Three levels, linear weights: q=3, T_w = 3 + 4*0.5 = 5. Six items: (1,1) (0.5,0.5) (0,0.5) (1,1) (0.5,0) (0,0).
    # p_a = (1+1+0.5+1+0.5+1)/6 = 5/6; marginals A: 1:2/6, 0.5:2/6, 0:2/6; B: 1:2/6, 0.5:2/6, 0:2/6, so
    # pi = (1/3, 1/3, 1/3), sum pi(1-pi) = 3 * 2/9 = 2/3, p_e = 5 * (2/3) / 6 = 5/9, AC2 = (5/6 - 5/9)/(1 - 5/9) = (5/18)/(4/9) = 0.625.
    check(abs(gwet_ac2([1, 0.5, 0, 1, 0.5, 0], [1, 0.5, 0.5, 1, 0, 0])[0] - 0.625) < 1e-9, "Gwet's AC2: mixed case = 0.625 by hand")
    print("all checks passed")


if __name__ == "__main__":
    main()
