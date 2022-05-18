"""
Takes the cleaned dataframe and computes all statistics needed for the report (e.g. for tables and visualizations).
IN: cleaned dataframe
OUT: dict of dicts, e.g.
{
    "full":{
        "basic_stats":{"num_started_and_ended": int, "num_started_but_not_ended": int,
                        "num_not_started_but_ended": int, "num_ended": int, "num_started": int},

        "task_metrics":{"alloccpu":[0,256,45], # [min, max, median] # only include tasks which started AND ended in timeframe
                        "elapsed":[0,10383739848,2894894]},

        "termination":{"n_complete":int, "n_cancelled":int, "n_failed":int, "n_timeout":int} # only include tasks which started AND ended in timeframe
    },
        
    "user_split":{
        "user_names": list,
        "basic_stats": {"num_started_and_ended":list[int], ...},
        "task_metrics": {"alloccpu":[[user1min, user1max, user1median],
                                     [user2min, user2max, user2median]
                                     ...]}
        # NO TERMINATION SUBDICT
    },

    "partition_split:{
        "partition_names": list,
        "basic_stats": {"num_started_and_ended":list[int], ...},
        "task_metrics": ...,
        # NO TERMINATION SUBDICT
    }

}
})
"""