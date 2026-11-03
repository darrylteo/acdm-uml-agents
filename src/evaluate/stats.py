"""Agreement statistics between two graders over the items both graded (credit 0, 0.5, 1).

Gwet's AC2 (linearly weighted AC1) is the reported statistic; linearly weighted Cohen's kappa is
computed for the record. Kappa is uninformative at the prevalence these grades have (most items
1): its chance term approaches 1 and the coefficient collapses at 84% raw agreement; AC2's chance
term does not (Gwet 2008). Used by reliability.py; checked by selftest.py.
"""


def weighted_kappa(a: list[float], b: list[float], levels=(0.0, 0.5, 1.0)) -> float:
    """Linearly weighted Cohen's kappa for two raters over the same items."""
    n = len(a)
    idx = {v: i for i, v in enumerate(levels)}
    k = len(levels)
    obs = [[0] * k for _ in range(k)]
    for x, y in zip(a, b):
        obs[idx[x]][idx[y]] += 1
    ra = [sum(row) for row in obs]
    rb = [sum(obs[i][j] for i in range(k)) for j in range(k)]
    w = [[abs(i - j) / (k - 1) for j in range(k)] for i in range(k)]
    disagree_obs = sum(w[i][j] * obs[i][j] for i in range(k) for j in range(k)) / n
    disagree_exp = sum(w[i][j] * ra[i] * rb[j] for i in range(k) for j in range(k)) / (n * n)
    return 1.0 - disagree_obs / disagree_exp if disagree_exp else 1.0


def gwet_ac2(a: list[float], b: list[float], levels=(0.0, 0.5, 1.0)) -> tuple[float, float]:
    """Gwet's AC2 (linearly weighted AC1; Gwet 2008, Br J Math Stat Psychol 61(1):29-48) for two
    raters over the same items, with its standard error from Gwet's variance estimator. Returns
    (coefficient, se). With q categories, weights w_kl = 1 - |k-l|/(q-1) and T_w their sum, the
    chance term is p_e = T_w * sum_k pi_k (1-pi_k) / (q (q-1)), pi_k the two raters' mean share of
    category k, which stays small when one category dominates; Cohen's kappa's p_e tends to 1 there
    and kappa collapses although the raters agree on nearly every item (Feinstein and Cicchetti
    1990). Binary levels give AC1. Tested against hand-computed cases in selftest.py."""
    n = len(a)
    idx = {v: i for i, v in enumerate(levels)}
    q = len(levels)
    obs = [[0] * q for _ in range(q)]
    for x, y in zip(a, b):
        obs[idx[x]][idx[y]] += 1
    w = [[1.0 - abs(i - j) / (q - 1) for j in range(q)] for i in range(q)]
    tw = sum(map(sum, w))
    pkl = [[obs[i][j] / n for j in range(q)] for i in range(q)]
    pa = sum(w[i][j] * pkl[i][j] for i in range(q) for j in range(q))
    ra = [sum(row) / n for row in obs]
    rb = [sum(obs[i][j] for i in range(q)) / n for j in range(q)]
    pi = [(ra[k] + rb[k]) / 2 for k in range(q)]
    pe = tw * sum(x * (1 - x) for x in pi) / (q * (q - 1))
    ac = (pa - pe) / (1 - pe) if pe < 1 else 1.0
    s1 = sum(pkl[k][l] * (w[k][l] - 2 * (1 - ac) * tw * (1 - (pi[k] + pi[l]) / 2) / (q * (q - 1))) ** 2
             for k in range(q) for l in range(q))
    var = max((s1 - (pa - 2 * (1 - ac) * pe) ** 2) / (n * (1 - pe) ** 2), 0.0) if n > 1 and pe < 1 else 0.0
    return ac, var ** 0.5
