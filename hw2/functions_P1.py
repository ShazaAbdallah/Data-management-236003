import numpy
import numpy as np
import pandas as pd
from dowhy import CausalModel


def make_formal_education_binary(df):
    higher_ed = {"Bachelor's degree (BA, BS, B.Eng., etc.)",
    "Master's degree (MA, MS, M.Eng., MBA, etc.)",
    "Doctoral degree (PhD, EdD, etc.)",
    "Professional degree (JD, MD, etc.)"
    }
    df = df.copy()
    df["FormalEducation_binary"] = df["FormalEducation"].apply(
        lambda x: 1 if x in higher_ed else 0
    )
    return df


def make_undergrad_major_binary(df):
    df = df.copy()
    df["UndergradMajor"] = df["UndergradMajor"].apply(
        lambda x: 1 if x == 6 else 0
    )
    return df
    

def extract_confounders(DAG, treatment, outcome):
    """
    Given a DAG (list of 'A;' or 'A -> B;' strings), a treatment T and an outcome variable Y,
    return a sufficent set of confounding variables that block all backdoor paths between T and Y
    """
    ####TODO####

    parents = set()
    edges = {}
    reversed_edges = {}
    for item in DAG:
        if "->" in item:
            from_node, to_node = item.strip(';').split(" -> ")
            # find parents of X
            if to_node == treatment:
                parents.add(from_node)
                continue  # don't add edges between X and its parents to exclude these edges from search
            if from_node not in edges:
                edges[from_node] = []
            edges[from_node].append(to_node)
            if to_node not in reversed_edges:
                reversed_edges[to_node] = []
            reversed_edges[to_node].append(from_node)

    # only include a parent of X if they have a path to Y not through X
    reaches_outcome = set()
    q = [outcome]
    while q:
        for _ in range(len(q)):
            item = q.pop(0)
            reaches_outcome.add(item)
            for son in edges.get(item, []):
                if son not in q and son not in reaches_outcome:
                    q.append(son)
            for son in reversed_edges.get(item, []):
                if son not in q and son not in reaches_outcome:
                    q.append(son)
    confounders = parents & reaches_outcome
    return confounders




def compute_emprical_ate(treatment, outcome, df, DAG):
    confounders =  extract_confounders(DAG, treatment, outcome)
    print("Confounders:", confounders)
    
    #####TODO###########
    

    df = df.copy()

    grouped = df.groupby(list(confounders))
    valid_samples = 0
    valid_groups = []

    for _, group in grouped:
        group_t_1 = group.loc[group[treatment] == 1]
        group_t_0 = group.loc[group[treatment] == 0]
        if len(group_t_1) == 0 or len(group_t_0) == 0:  # drop group if there are no t_0 or t_1 samples
            continue
        l = len(group)  # to calculate empirical p_c
        valid_samples += l  # count the number of samples we didn't drop to calculate empirical p_c
        mean_t_1 = numpy.mean(group_t_1[outcome])
        mean_t_0 = numpy.mean(group_t_0[outcome])
        valid_groups.append((l, mean_t_1, mean_t_0))  # save group values to calculate once we know how many samples we have

    ate_per_group = [(g[0] / valid_samples) * (g[1] - g[2]) for g in valid_groups]
    return sum(ate_per_group)


def compute_causal_effect_linear_reg(treatment, outcome, df, confounders):

    model = CausalModel(
        data=df,
        common_causes=list(confounders),
        treatment=treatment,
        outcome=outcome)


    identified_estimand = model.identify_effect(proceed_when_unidentifiable=True)
    print(identified_estimand)

    estimands = model.identify_effect()

    causal_estimate_reg = model.estimate_effect(estimands,
                                                    method_name="backdoor.linear_regression",
                                                    test_significance=True)
    return causal_estimate_reg.value, causal_estimate_reg.test_stat_significance()['p_value']


def compute_causal_effect_prop(treatment, outcome, df, confounders):

    model = CausalModel(
        data=df,
        common_causes=list(confounders),
        treatment= treatment,
        outcome=outcome)

    identified_estimand = model.identify_effect(proceed_when_unidentifiable=True)
    print(identified_estimand)

    estimands = model.identify_effect()
    
    causal_estimate = model.estimate_effect(
    estimands,
    method_name="backdoor.propensity_score_weighting",
    method_params={"weighting_scheme":"ips_weight"}
        )

    return causal_estimate.value




    

    

