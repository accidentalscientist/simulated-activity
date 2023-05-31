"""Archive task: Origin Energy Volatility Study.

Generated for 2023-05-31. This synthetic market research code is educational
only and is not financial advice.
"""

def rolling_volatility(values: list[float], window: int = 20) -> list[float]:
    returns = [(values[i] / values[i - 1]) - 1 for i in range(1, len(values))]
    output = []
    for index in range(len(returns) - window + 1):
        sample = returns[index:index + window]
        mean = sum(sample) / window
        output.append((sum((value - mean) ** 2 for value in sample) / window) ** 0.5)
    return output
