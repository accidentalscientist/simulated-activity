# Simulated Python script
import pandas as pd
import numpy as np

data = pd.DataFrame({
    'value': np.random.rand(100),
    'timestamp': pd.date_range(start='2022-01-01', periods=100)
})

print(data.describe())
