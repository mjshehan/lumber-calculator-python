import pandas as pd

def sum_list(ls):
    
    sum = 0
    for i in range(len(ls)):
        ls[i] = ls[i] + sum
        sum = ls[i]

    return(ls)


df = pd.DataFrame({
    'Lumber': ['120', '120', '96'],
    'Bar_Sizes': [120, 120, 96],
    'Cuts': [[5, 10, 20], [5, 10, 20], [5, 10, 20]]
    })

df['Cuts'] = df['Cuts'].apply(sum_list)

