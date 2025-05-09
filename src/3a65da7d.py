import pandas as pd
from sklearn.linear_model import LinearRegression

df = pd.read_csv('data/sample.csv')
X, y = df.drop('target', axis=1), df['target']
model = LinearRegression().fit(X, y)
print('R²:', model.score(X, y))
