# File: simulate_git_activity.py

import os
import random
import subprocess
from datetime import datetime, timedelta
from faker import Faker
import numpy as np

fake = Faker()

# Constants
START_DATE = datetime(2022, 1, 1)
END_DATE = datetime.now()
COMMITS_PER_WEEK = 4
REPO_DIR = os.getcwd()  # current folder

VERBS = ["add", "update", "fix", "refactor", "optimize", "clean", "tune", "document"]
OBJECTS = [
    "data cleaning", "EDA", "feature engineering", "model training", "notebook",
    "pipeline", "script", "dashboard", "report"
]
TOOLS = [
    "pandas", "numpy", "seaborn", "matplotlib", "scikit-learn",
    "xgboost", "statsmodels", "regression", "clustering", "PCA"
]
EXTENSIONS = [".py", ".md", ".csv"]

# Generates a commit message
def generate_commit_message():
    return f"{random.choice(VERBS)}: {random.choice(OBJECTS)} [{random.choice(TOOLS)}]"

# Generates random file content
def generate_file_content(extension):
    if extension == ".py":
        return f"""# Simulated Python script\nimport pandas as pd\nimport numpy as np\n\ndata = pd.DataFrame({{\n    'value': np.random.rand(100),\n    'timestamp': pd.date_range(start='2022-01-01', periods=100)\n}})\n\nprint(data.describe())\n"""
    elif extension == ".md":
        return f"""## Data Science Report\n\nGenerated summary:\n\n- Author: {fake.name()}\n- Analysis Topic: {random.choice(OBJECTS)}\n- Tools Used: {random.sample(TOOLS, 3)}\n"""
    elif extension == ".csv":
        return "date,value\n" + "\n".join(
            [f"{(START_DATE + timedelta(days=random.randint(0, 1000))).strftime('%Y-%m-%d')},{random.uniform(0, 100):.2f}" for _ in range(10)]
        )
    else:
        return ""

# Creates a commit on a specific datetime
def make_commit(commit_date: datetime):
    filename = f"file_{commit_date.strftime('%Y%m%d%H%M%S')}{random.choice(EXTENSIONS)}"
    filepath = os.path.join(REPO_DIR, filename)

    with open(filepath, 'w') as f:
        f.write(generate_file_content(os.path.splitext(filename)[1]))

    subprocess.run(["git", "add", filename], cwd=REPO_DIR)

    env = os.environ.copy()
    iso_date = commit_date.strftime('%Y-%m-%dT%H:%M:%S')
    env["GIT_AUTHOR_DATE"] = iso_date
    env["GIT_COMMITTER_DATE"] = iso_date
    subprocess.run(["git", "commit", "-m", generate_commit_message()], cwd=REPO_DIR, env=env)

# Main simulation loop
def simulate_commits():
    current_date = START_DATE
    while current_date < END_DATE:
        commits_this_week = np.random.poisson(COMMITS_PER_WEEK)
        for _ in range(commits_this_week):
            random_day = current_date + timedelta(days=random.randint(0, 6))
            random_time = timedelta(minutes=random.randint(0, 1440))
            commit_datetime = random_day + random_time
            if commit_datetime < END_DATE:
                make_commit(commit_datetime)
        current_date += timedelta(days=7)

if __name__ == "__main__":
    simulate_commits()
    print("✅ Simulated commits complete. Run `git push` to sync with GitHub.")
