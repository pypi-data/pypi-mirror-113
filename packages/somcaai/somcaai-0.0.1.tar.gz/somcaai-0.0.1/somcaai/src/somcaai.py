## Return a arry with accumulated values. Receive a dataframe and a reference col and for each row sums previous values
def accumulate_months(df, ref_col):
    df_acc = []
    for index, rows in df.iterrows():
        # sum the value of the current row with all previous
        parcial = df[0:index+1][ref_col].sum() 
        df_acc.append(parcial)
    return df_acc   

## Convert the row value into a % that represents the % that this value and all the previous ones represent in the whole period
def convert_to_perc(df,pct_col, ref_col,monthnum):
    # In theory the maximum will always be the value of the last month, which is equal to the sum of all the values.      
    total = df[ref_col].max()

    # declare lists to append values
    df_perc = [] 
    months = []
    row_number = []

    ## for each row in the df calculate the percentage and define the monthnum and the rownum.
    for index, rows in df.iterrows():
        perc = ((rows[ref_col]/total)*100).round(2)
        df_perc.append(perc)
        months.append(monthnum)
        row_number.append(index+1) ## the index starts in 0, so we need to increment 1 (to keep the compliance with SAS)
    
    df['rownum'] = row_number
    df['monthnum'] = months
    df[pct_col] = df_perc

    return df 