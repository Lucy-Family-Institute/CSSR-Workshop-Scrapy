import pandas as pd
import os

ROOT_DIR = os.getcwd()

data = pd.read_json("../../crawldata/reuterscrawl.jsonl",lines=True)