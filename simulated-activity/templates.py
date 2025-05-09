TEMPLATES = {
    "py": """\
import pandas as pd
from sklearn.linear_model import LinearRegression

df = pd.read_csv('data/sample.csv')
X, y = df.drop('target', axis=1), df['target']
model = LinearRegression().fit(X, y)
print('R²:', model.score(X, y))
""",

    "sql": "SELECT * FROM customers WHERE signup_date > CURRENT_DATE - INTERVAL '30 days';",

    "json": '{"experiment": "AB_test", "variant": "control", "metric": "conversion"}\n',

    "md": "# Daily Findings\nSome quick notes on today’s run.\n"
}
