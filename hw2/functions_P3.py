from efficient_apriori import apriori

def dataframe_to_transactions(df):
    transactions = []
    
    for _, row in df.iterrows():
        transaction = tuple(f"{col}:{row[col]}" for col in df.columns)
        transactions.append(transaction)
    
    return transactions
