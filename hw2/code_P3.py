

# IMPORTANT: copy all your code from problem 3.2 and 3.3, as is, to file "code_P3.py" # 
# We will not try to run this code from the py file.


### 3.2 ###


### 3.3 ###



# IMPORTANT: copy all your code from problem 3.2 and 3.3, as is, to file "code_P3.py" #
# We will not try to run this code from the py file.


### 3.2 ###
### TODO: any additional code for q.3.2 ###

# IMPORTANT: copy all your code from problem 3.2, as is, to file "code_P3.py" #
# We will not try to run this code from the py file, but you have to copy and submit it over there.

#print(df.describe())
df.columns = df.columns.str.strip()

# ---- Residential assets: has vs does not have ----
df['res_assets_bin'] = pd.cut(
    df['residential_assets_value'],
    bins=[-float('inf'), 0, float('inf')],
    labels=['NoResidentialAssets', 'HasResidentialAssets']
)

df['res_assets_bin_2'] = pd.cut(
    df['residential_assets_value'],
    bins=[-float('inf'), 2.2e06, float('inf')],
    labels=['LowResidentialAssets', 'HighResidentialAssets']
)




transactions_apriori = dataframe_to_transactions(df)
itemsets, rules = apriori(transactions_apriori, min_support=0.9, min_confidence=0.9)
print("Residential assets bin: ≤ 0 = NoResidentialAssets, > 0 = HasResidentialAssets")
print(itemsets)
itemsets, rules = apriori(transactions_apriori, min_support=0.7, min_confidence=0.7)
print("Residential assets bin: ≤ 2.2e06 = LowResAssets, > 2.2e06 = HighResAssets")
print(itemsets)
#print(rules)


### 3.3 ###

### TODO: any additional code for q.3.3 ###


# IMPORTANT: copy all your code from problem 3.3, as is, to file "code_P3.py" #
# We will not try to run this code from the py file, but you have to copy and submit it over there.
df['dependents_bin'] = pd.cut(
    df['no_of_dependents'],
    bins=[-float('inf'), 1, float('inf')],
    labels=['LowDependents', 'HighDependents']
)

df['income_bin'] = pd.cut(
    df['income_annum'],
    bins=[-float('inf'), 2.7e6, float('inf')],
    labels=['LowIncome', 'HighIncome']
)

df['loan_amount_bin'] = pd.cut(
    df['loan_amount'],
    bins=[-float('inf'), 7.7e6, float('inf')],
    labels=['SmallLoan', 'LargeLoan']
)

df['loan_term_bin'] = pd.cut(
    df['loan_term'],
    bins=[-float('inf'), 6, float('inf')],
    labels=['ShortTerm', 'LongTerm']
)

df['cibil_bin'] = pd.cut(
    df['cibil_score'],
    bins=[-float('inf'), 450, float('inf')],
    labels=['LowCredit', 'HighCredit']
)

df['com_assets_bin'] = pd.cut(
    df['commercial_assets_value'],
    bins=[-float('inf'), 1.3e6, float('inf')],
    labels=['LowComAssets', 'HighComAssets']
)

df['lux_assets_bin'] = pd.cut(
    df['luxury_assets_value'],
    bins=[-float('inf'), 7.5e6, float('inf')],
    labels=['LowLuxuryAssets', 'HighLuxuryAssets']
)

df['bank_assets_bin'] = pd.cut(
    df['bank_asset_value'],
    bins=[-float('inf'), 2.3e6, float('inf')],
    labels=['LowBankAssets', 'HighBankAssets']
)
transactions_apriori = dataframe_to_transactions(df)
itemsets, rules = apriori(transactions_apriori, min_support=0.5, min_confidence=0.7)
print("\nAssociation Rules:")
for rule in rules:
    if tuple(rule.rhs) == ('loan_status: Approved',):
        print(f"{tuple(rule.lhs)}  -->  {tuple(rule.rhs)}")