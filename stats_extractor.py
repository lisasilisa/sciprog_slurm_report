"""
Takes the cleaned dataframe and computes all statistics needed for the report (e.g. for tables and visualizations).
IN: cleaned dataframe
OUT: dict of dicts, e.g.
{
    "full":{
        "basic_stats":{"n_start_end": int, "n_end": int, "n_start": int},

        "task_metrics":{"AllocCPUS":[0,25,45,102,256,60], # [min, 25quant, median, 75quant, max, mean] # only include tasks which started AND ended in timeframe
                        "ElapsedRaw":[0,238484,10383739848,2894894556,39438484384,949237]},
                        "CPUTimeRaw":...}

        "termination_stats":{"n_complete":int, "n_cancelled":int, "n_failed":int, "n_timeout":int} # only include tasks which started AND ended in timeframe
    },

    "user_split":{
        "user_names": list,
        "user_counts": list,
        "basic_stats": {"num_started_and_ended":list[int], ...},
        "task_metrics": {"alloccpu":[[user1_min, user1_05quant, user1_25quant, user1_median, user1_75quant, user1_95quant, user1_max, user1mean],
                                     [user2_min, user2_05quant, user2_25quant, user2_median, user2_75quant, user2_95quant, user2_max, user2mean],
                                     ...]}
    },

    "partition_split:{
        "partition_names": list,
        "partition_counts": list,
        "basic_stats": {"num_started_and_ended":list[int], ...},
        "task_metrics": ...,
    }
}
})
"""

import pandas as pd
import numpy as np


class StatsExtractor:


    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.account = df["Account"].iloc[0]
        self.partitions = df["Partition"].value_counts(ascending=False).index.tolist()
        self.partition_counts = df["Partition"].value_counts(ascending=False).values.tolist()
        self.users = df["User"].value_counts(ascending=False).index.tolist()
        self.user_counts = df["User"].value_counts(ascending=False).values.tolist()


    def extract_stats(self) -> dict:
        """
        Extracts the full stats_dict.
        -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
        Arguments:
        None
        -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
        Returns:
        dict; full stats dict.
        """

        stats_dict = {}

        # Extract stats for full dataset
        stats_dict["full"] = {"basic_stats":self.get_basic_stats(split="Full"),
                              "task_metrics":self.get_task_metrics(split="Full"),
                              "termination_stats":self.get_termination_stats()
        }

        if len(self.users) >= 2:
            stats_dict["user_split"] = {"user_names":self.users,
                                        "user_counts":self.user_counts,
                                        "basic_stats":self.get_basic_stats(split="User"),
                                        "task_metrics":self.get_task_metrics(split="User")
            }

        if len(self.partitions) >= 2:
            stats_dict["partition_split"] = {"partition_names":self.partitions,
                                            "partition_counts":self.partition_counts,
                                            "basic_stats":self.get_basic_stats(split="Partition"),
                                            "task_metrics":self.get_task_metrics(split="Partition")
            }

        return stats_dict

    def get_basic_stats(self, split:str="Full") -> dict:
        """
        Extracts basic stats:
            * number of jobs started
            * number of jobs ended
            * number of jobs started and ended
            * number of jobs started but not ended
            * number of jobs not started but ended
        in the given time period.
        -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
        Arguments:
        split: str in ["Full", "User", or "Partition"]; default: "Full".
        -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
        Returns:
        dict with int or list values.
        -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
        """

        # If split=="Full", extract stats for full sample
        if split=="Full":

            basic_dict = {}

            basic_dict["n_start_end"] = ((self.df["StartDate"] >= self.df["PeriodStartDate"]) & (self.df["EndDate"] <= self.df["PeriodEndDate"])).sum()
            basic_dict["n_start"] = (self.df["StartDate"] >= self.df["PeriodStartDate"]).sum()
            basic_dict["n_end"] = (self.df["EndDate"] <= self.df["PeriodEndDate"]).sum()


        # If split "User" or "Partition", extract stats for each user or partition
        elif split=="User" or split=="Partition":
            
            basic_dict = {"n_start_end":[], "n_start":[], "n_end":[]}

            split_list = self.users if split=="User" else self.partitions # Set appropriate iterable

            for element in split_list:
                
                df_sub = self.df[self.df[split] == element] # Slice df down to specific user or partition

                basic_dict["n_start_end"].append(((df_sub["StartDate"] >= df_sub["PeriodStartDate"]) & (df_sub["EndDate"] <= df_sub["PeriodEndDate"])).sum())
                basic_dict["n_start"].append((df_sub["StartDate"] >= df_sub["PeriodStartDate"]).sum())
                basic_dict["n_end"].append((df_sub["EndDate"] <= df_sub["PeriodEndDate"]).sum())
                
        else:
            raise NameError("Please set the 'split' argument to 'Full', 'User', or 'Partition'.")
        return basic_dict


    def get_task_metrics(self, split:str="Full") -> dict:
        """
        Extracts task metrics:
            * number of allocated CPUs
            * elapsed time
            * CPU time
        in the given time period.
        -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
        Arguments:
        split: str in ["Full", "User", or "Partition"]; default: "Full".
        -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
        Returns:
        dict with int or list values.
        -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
        """

        df_time_sub = self.df[(self.df["StartDate"] >= self.df["PeriodStartDate"]) & (self.df["EndDate"] <= self.df["PeriodEndDate"])]

        metrics = ["AllocCPUS", "ElapsedRaw", "CPUTimeRaw"]

        if split=="Full":

            metrics_dict = {}

            for metric in metrics:
                metrics_dict[metric] = [df_time_sub[metric].min(), df_time_sub[metric].quantile(.05), df_time_sub[metric].quantile(.25), df_time_sub[metric].median(),
                df_time_sub[metric].quantile(.75), df_time_sub[metric].quantile(.95), df_time_sub[metric].max(), round(df_time_sub[metric].mean(),3)]

        elif split=="User" or split=="Partition":
            
            metrics_dict = {m:[] for m in metrics}

            split_list = self.users if split=="User" else self.partitions # Set appropriate iterable

            for element in split_list:
                
                df_sub = df_time_sub[df_time_sub[split] == element] # Slice df down to specific user or partition
                
                for metric in metrics:
                    metrics_dict[metric].append([df_sub[metric].min(), df_sub[metric].quantile(.05), df_sub[metric].quantile(.25), df_sub[metric].median(),
                                                df_sub[metric].quantile(.75), df_sub[metric].quantile(.95), df_sub[metric].max(), round(df_sub[metric].mean(),3)])
                

        return metrics_dict


    def get_termination_stats(self) -> dict:
        """
        Extracts task metrics:
            * number of completed tasks
            * number of cancelled tasks
            * number of failed tasks
            * number of timeouted tasks
        in the given time period.
        -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
        Arguments:
        No arguments.
        -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
        Returns:
        dict with int.
        -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
        """
        df_time_sub = self.df[(self.df["StartDate"] >= self.df["PeriodStartDate"]) & (self.df["EndDate"] <= self.df["PeriodEndDate"])]

        termination_dict = {}

        termination_dict["n_complete"] = (df_time_sub["State"] == "COMPLETED").sum()
        termination_dict["n_cancelled"] = (df_time_sub["State"] == "CANCELLED").sum()
        termination_dict["n_failed"] = (df_time_sub["State"] == "FAILED").sum()
        termination_dict["n_timeout"] = (df_time_sub["State"] == "TIMEOUT").sum()

        return termination_dict




        



