import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt  # Uncommented this line
import pandas as pd

def sum_list(ls):
    sum = 0
    for i in range(len(ls)):
        ls[i] = ls[i] + sum
        sum = ls[i]
    return(ls)


#Creates the cut diagram using matplotlib
def make_visual(df):
    plt.clf()
    
    df1 = df
    df = pd.DataFrame({
    'Lumber': [],
    'Bar_Sizes': [],
    'Cuts': [],
    'Piece_Sizes': []
    })
    plot_width = 6
    num_bars = len(df1.index)
    plt.figure(figsize=[plot_width, num_bars * 1]) 
    plt.title('Cut Diagram')
    plt.box(False)

    for index, row in df1.iterrows():
        df.loc[index, 'Lumber'] = str(row['lumber length'])
        df.loc[index, 'Bar_Sizes'] = row['lumber length']
         
    df['Piece_Sizes'] = [list(x) for x in df1['cuts']]
    df['Cuts'] = df1['cuts'].apply(sum_list)
         
    relative_height = 0.5

    plt.barh(df.index, df['Bar_Sizes'], height = relative_height, color='Peru')
   
    for i, row in df.iterrows():
        values = row['Cuts']
        pieces = row['Piece_Sizes']
       
        for j in range(len(values)):
            plt.plot([values[j], values[j]], [i - relative_height/2, i + relative_height/2], color='black')
            plt.text(values[j]-(pieces[j])/2-1.75, i, str(pieces[j]), color='black', fontsize=10, fontweight='bold')
            plt.text(int(df['Bar_Sizes'][i]) + 1, i, str(int(df['Bar_Sizes'][i]) // 12) + " ft", color = "black", fontsize=10 )
                
    plt.yticks(df.index, df.index + 1) 
    plt.xticks([])
    plt.gca().invert_yaxis() 
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

    
