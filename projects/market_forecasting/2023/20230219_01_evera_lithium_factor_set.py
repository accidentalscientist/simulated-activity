"""Archive task: Evera Lithium Factor Set.

Generated for 2023-02-19. This synthetic market research code is educational
only and is not financial advice.
"""

def build_lithium_factor_set(prices, volumes, benchmark):
    return {
        "momentum_20": prices[-1] / prices[-20] - 1,
        "volume_ratio": volumes[-5] / max(sum(volumes[-20:]) / 20, 1),
        "benchmark_spread": prices[-1] / benchmark[-1] - 1,
    }
