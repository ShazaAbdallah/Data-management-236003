

# IMPORTANT: copy all your code from problem 4, as is, to file "code_P4.py" # 
# We will not try to run this code from the py file.

#our result code:
# --- 1. Load and Preprocess ---
df = pd.read_csv('./loan_approval_dataset.csv')
df.columns = df.columns.str.strip()
df['loan_status_binary'] = df['loan_status'].map({' Approved': 1, ' Rejected': 0})

# --- 2. Define the Column (Loan Term) ---
# We bin loan_term into Short, Medium, Long to make it categorical
def term_bin(t):
    if t <= 8:
        return 'ShortTerm (<8y)'
    elif t <= 14:
        return 'MediumTerm (8-14y)'
    else:
        return 'LongTerm (>14y)'

df['term_bin'] = df['loan_term'].apply(term_bin)

# Order for plotting
order = ['ShortTerm (<8y)', 'MediumTerm (8-14y)', 'LongTerm (>14y)']

# --- 3. Global Plot (Entire Data) ---
avg_all = (
    df.groupby('term_bin')['loan_status_binary']
      .mean()
      .reindex(order)
      .reset_index()
)

print("--- Entire Data (Global Trend) ---")
print(avg_all)

plt.figure(figsize=(8, 5))
plt.bar(avg_all['term_bin'], avg_all['loan_status_binary'], color='skyblue')
plt.title('Global Trend: Loan Term vs Approval')
plt.ylim(0, 1)
plt.ylabel('Approval Rate')
plt.show()

# --- 4. Define Subpopulation (Borderline/Low CIBIL) ---
# We look at people with scores between 300 and 550.
# These are "risky" applicants where term length matters more.
df_sub = df[
    (df['cibil_score'] >= 300) &
    (df['cibil_score'] <= 549)
]

avg_sub = (
    df_sub.groupby('term_bin')['loan_status_binary']
          .mean()
          .reindex(order, fill_value=0) # fill_value=0 ensures we don't crash if a bin is empty, though unlikely here
          .reset_index()
)

print("\n--- Subpopulation (Low CIBIL Score) ---")
print(avg_sub)

plt.figure(figsize=(8, 5))
plt.bar(avg_sub['term_bin'], avg_sub['loan_status_binary'], color='salmon')
plt.title('Subpopulation Trend: Low CIBIL vs Approval')
plt.ylim(0, 1)
plt.ylabel('Approval Rate')
plt.show()


Q = avg_all['loan_status_binary'].values

# P = Target Distribution (Subpopulation Trend)
P = avg_sub['loan_status_binary'].values

# 2. Compute KL Divergence
# The function will automatically handle normalizing them so they sum to 1
divergence_score = safe_kl_div(P, Q)

print(f"KL Divergence Score: {divergence_score}")

low_cibil_df = df[
    (df['cibil_score'] >= 300) &
    (df['cibil_score'] <= 549)
]

# 2. Create a "Cross-Tabulation" table
# This counts how many applicants exist for each Loan Term in your Low CIBIL group.
counts = pd.crosstab(low_cibil_df['term_bin'], columns='count')

print("--- Counts for Low CIBIL Subpopulation ---")
print(counts)



#another try that might work:
df = pd.read_csv('./loan_approval_dataset.csv')
df.columns = df.columns.str.strip()
df['loan_status_binary'] = df['loan_status'].map({' Approved': 1, ' Rejected': 0})
def income_bin(x):
    if x <= 3_000_000:
        return 'LowIncome'
    elif x <= 7_000_000:
        return 'MediumIncome'
    else:
        return 'HighIncome'

df['income_bin'] = df['income_annum'].apply(income_bin)

avg_all = (
    df.groupby('income_bin')['loan_status_binary']
      .mean()
      .reset_index()
)

print("Entire data")
print(avg_all)
import matplotlib.pyplot as plt

# Ensure consistent order
order = ['LowIncome', 'MediumIncome', 'HighIncome']

avg_all = avg_all.set_index('income_bin').reindex(order).reset_index()

plt.figure(figsize=(8, 5))
plt.bar(
    avg_all['income_bin'],
    avg_all['loan_status_binary']
)
plt.xlabel('Income Level')
plt.ylabel('Average Loan Approval')
plt.title('Income Level vs Average Loan Approval (Entire Dataset)')
plt.ylim(0, 1)
plt.show()

df_sub = df[
    df['loan_amount'] >= 25_000_000
]

avg_sub = (
    df_sub.groupby('income_bin')['loan_status_binary']
          .mean()
          .reset_index()
)

print("Subpopulation")
print(avg_sub)

avg_sub = avg_sub.set_index('income_bin').reindex(order, fill_value=0).reset_index()

plt.figure(figsize=(8, 5))
plt.bar(
    avg_sub['income_bin'],
    avg_sub['loan_status_binary']
)
plt.xlabel('Income Level')
plt.ylabel('Average Loan Approval')
plt.title('Income Level vs Loan Approval\n(High Loan Amount Subpopulation)')
plt.ylim(0, 1)
plt.show()


avg_sub = avg_sub.set_index('income_bin').reindex(
    avg_all['income_bin'], fill_value=1e-6
).reset_index()

Q = avg_all['loan_status_binary'].values
P = avg_sub['loan_status_binary'].values

kl_value = safe_kl_div(P, Q)
print("KL divergence:", kl_value)



#tries that didnt work:
df = pd.read_csv('./loan_approval_dataset.csv')

def term_bin(x):
    if x <= 5:
        return 'Short'
    elif x <= 15:
        return 'Medium'
    else:
        return 'Long'

df['term_bin'] = df['loan_term'].apply(term_bin)
df['loan_status_binary'] = df['loan_status'].map({' Approved': 1, ' Rejected': 0})

avg_all = (
    df.groupby('term_bin')['loan_status_binary']
      .mean()
      .reset_index()
)

print("Entire data")
print(avg_all)

df_sub = df[
    (df['luxury_assets_value'] >= 15_000_000) &
    (df['bank_asset_value'] >= 5_000_000)
]

avg_sub = (
    df_sub.groupby('term_bin')['loan_status_binary']
          .mean()
          .reset_index()
)

print("Subpopulation")
print(avg_sub)
Q = avg_all.sort_values('term_bin')['loan_status_binary'].values
P = avg_sub.sort_values('term_bin')['loan_status_binary'].values

kl_value = safe_kl_div(P, Q)
print("KL divergence:", kl_value)

#another try that didnt work:
#TODO add your code here


# IMPORTANT: copy all your code from problem 4, as is, to file "code_P4.py" #
# We will not try to run this code from the py file, but you have to copy and submit it over there.
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('./loan_approval_dataset.csv')

# loan_status already binary in your table, but ensure consistency
# df['loan_status_binary'] = df['loan_status'].map({' Approved': 1, ' Rejected': 0})

# Discretize CIBIL score
def cibil_bin(x):
    if x <= 450:
        return 'LowCredit'
    elif x <= 700:
        return 'MediumCredit'
    else:
        return 'HighCredit'

df['cibil_bin'] = df['cibil_score'].apply(cibil_bin)

df.columns = df.columns.str.strip()
df['loan_status_binary'] = df['loan_status'].map({' Approved': 1, ' Rejected': 0})

average_loan_status = (
    df.groupby('cibil_bin')['loan_status_binary']
      .mean()
      .reset_index()
)

plt.figure(figsize=(8, 5))
plt.bar(
    average_loan_status['cibil_bin'],
    average_loan_status['loan_status_binary']
)
plt.xlabel('CIBIL Score Bin')
plt.ylabel('Average Loan Status')
plt.title('CIBIL Score vs Average Loan Approval (Entire Dataset)')
plt.show()

avg1 = average_loan_status.sort_values('cibil_bin')
print("Entire data:")
print(avg1)


df_sub = df[
    (df['no_of_dependents'] >= 4) &
    (df['bank_asset_value'] <= 2_000_000)
]

average_loan_status_pattern = (
    df_sub.groupby('cibil_bin')['loan_status_binary']
          .mean()
          .reset_index()
)

plt.figure(figsize=(8, 5))
plt.bar(
    average_loan_status_pattern['cibil_bin'],
    average_loan_status_pattern['loan_status_binary']
)
plt.xlabel('CIBIL Score Bin')
plt.ylabel('Average Loan Status')
plt.title('CIBIL Score vs Loan Approval (High Loan Amount & Long Term)')
plt.show()

avg2 = average_loan_status_pattern.sort_values('cibil_bin')
print("Subpopulation:")
print(avg2)
Q = avg1['loan_status_binary'].values
P = avg2['loan_status_binary'].values

kl_value = safe_kl_div(P, Q)
print("KL divergence:", kl_value)
