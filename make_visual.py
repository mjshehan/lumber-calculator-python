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
   
    #relative_height = 2 / df['Bar_Sizes'].max()
    relative_height = 0.5

    #plt.barh(df['Lumber'], df['Bar_Sizes'], height = relative_height, color='gray')
    plt.barh(df.index, df['Bar_Sizes'], height = relative_height, color='gray')

    for i, row in df.iterrows():
        values = row['Cuts']
        for value in values:
            plt.plot([value, value], [i - relative_height/2, i + relative_height/2], color='blue')
    
    plt.yticks(df.index, df.index + 1) 
    plt.gca().invert_yaxis() 
    #plt.show()
    plt.savefig('website/static/visual.png')
    
def main():
   

    test_df = pd.DataFrame({
    'Lumber': [str(1), str(2), str(3), str(4), str(5), str(6), str(7), str(8)],
    'lumber length': [120, 120, 120, 96, 96, 96, 96, 96],
    'cuts': [[98, 9, 7, 0], [98, 7, 9], [120], [87], [90], [87, 6], [88,8], [67]]
    })
   
    make_visual(test_df)

if __name__ == "__main__":
    main()

    
