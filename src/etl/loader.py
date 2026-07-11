import pandas as pd
from pathlib import Path

DATA_FOLDER = Path("data/raw")


def load_excel(file_name, header=1):
    file_path = DATA_FOLDER / file_name

    if not file_path.exists():
        raise FileNotFoundError(f"{file_path} not found")

    return pd.read_excel(file_path, header=header)