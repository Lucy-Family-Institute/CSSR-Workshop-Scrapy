#%%
import pandas as pd
import os
from pathlib import Path

#%%
cwd = Path(os.getcwd())
ROOT_DIR = cwd.parent.parent
data = pd.read_json(str(ROOT_DIR)+"/crawldata/reuters_crawl.jsonl",lines=True)