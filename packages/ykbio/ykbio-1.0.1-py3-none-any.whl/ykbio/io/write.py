

def pandas_write(dataframe, name):
    if name.endswith(('.tsv', '.csv')):
        dataframe.to_csv(name, index=False, sep='\t')
    elif name.endswith('.xlsx'):
        dataframe.to_excel(name, index=False)