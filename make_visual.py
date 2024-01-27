import matplotlib.pyplot as plt  # Uncommented this line
import pandas as pd
#add test


def sum_list(ls):
    sum = 0
    for i in range(len(ls)):
        ls[i] = ls[i] + sum
        sum = ls[i]

    return(ls)



def make_visual(df):
    print(df)
    
    df1 = df
    df = pd.DataFrame({
    'Lumber': [],
    'Bar_Sizes': [],
    'Cuts': []
    })

    for index, row in df1.iterrows():
        df.loc[index, 'Lumber'] = str(row['lumber length'])
        df.loc[index, 'Bar_Sizes'] = row['lumber length']
        #df.loc[index, 'Cuts'] = list([5,10,20])
    

    df['Cuts'] = df1['cuts'].apply(sum_list)
        #df.iat[index, 2] = row['cuts']
    print("MAKING VISUAL")
    #relative_height = 2 / df['Bar_Sizes'].max()
    relative_height = 0.25

    bars = plt.barh(df['Lumber'], df['Bar_Sizes'], height = relative_height, color='gray')

    for i, row in df.iterrows():
        values = row['Cuts']
        for value in values:
            plt.plot([value, value], [i - relative_height/2, i + relative_height/2], color='blue')

    #plt.savefig('website/static/visual.png')

    plt.show()
