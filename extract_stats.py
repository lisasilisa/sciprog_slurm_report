"""
Dev script for using the stat_extractor module. Loads the cleaned dataframe and computes statistics.
"""

import pandas as pd

from stats_extractor import StatsExtractor

# Load df
df = pd.read_csv("dev_df.csv")

# Initialize StatExtractor
S = StatsExtractor(df)

print("-- "*20)
print("Account Information")
print()
print("Account:", S.account)
print("Users:", S.users)
print("Partitions:", S.partitions)
print()

# Get basic stats for full sample, user split, and partition split
print("-- "*20)
print("Basic Stats")
for split in ["Full", "User", "Partition"]:
    print(split)
    print(S.get_basic_stats(split=split))
print()

# Get task metrics for full sample, user split, and partition split
print("-- "*20)
print("Task Metrics")
for split in ["Full", "User", "Partition"]:
    print(split)
    print(S.get_task_metrics(split=split))
print()

# Get termination stats for full sample only
print("-- "*20)
print("Termination Stats")
print(S.get_termination_stats())
print()

# Extract full stats dict
print("-- "*20)
print("Full Stat Dict")
print(S.extract_stats())
print()
