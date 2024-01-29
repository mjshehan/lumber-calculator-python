import matplotlib
matplotlib.use('Agg')
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
    plt.clf()
    
    df1 = df
    df = pd.DataFrame({
    'Lumber': [],
    'Bar_Sizes': [],
    'Cuts': [],
    'Piece_Sizes': []
    })
    
    num_bars = len(df1.index)
    plt.figure(figsize=[6, num_bars * 1]) 
    plt.title('Cut Diagram')

    for index, row in df1.iterrows():
        df.loc[index, 'Lumber'] = str(row['lumber length'])
        df.loc[index, 'Bar_Sizes'] = row['lumber length']
        #df.loc[index, 'Cuts'] = list([5,10,20])
    
    df['Piece_Sizes'] = [list(x) for x in df1['cuts']]
    df['Cuts'] = df1['cuts'].apply(sum_list)
        #df.iat[index, 2] = row['cuts']
   
    #relative_height = 2 / df['Bar_Sizes'].max()
    relative_height = 0.5

    #plt.barh(df['Lumber'], df['Bar_Sizes'], height = relative_height, color='gray')
    plt.barh(df.index, df['Bar_Sizes'], height = relative_height, color='saddlebrown')
    print("this is the DF you're looking FOR!-----------------\n", df)
    for i, row in df.iterrows():
        values = row['Cuts']
        pieces = row['Piece_Sizes']
        start = 0
        last = 0
        for j in range(len(values)):
            plt.plot([values[j], values[j]], [i - relative_height/2, i + relative_height/2], color='black')
            plt.text(values[j]-(pieces[j])/2-1.75, i, str(pieces[j]), color='black', fontsize=10, fontweight='bold')
            
            last = pieces[j]
    
    plt.yticks(df.index, df.index + 1) 
   

    plt.gca().invert_yaxis() 

    #plt.text(5, 0, '10', fontsize=10, color='red')
    print("values ---------------", values)
  
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

    
