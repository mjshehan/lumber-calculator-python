import matplotlib.pyplot as plt  # Uncommented this line
import pandas as pd


categories = ['A', 'B', 'C']
values_A = [2, 5]
values_B = [1, 13]
values_C = [1, 3, 4]

df = pd.DataFrame({
    'Lumber': ['144', '120', '96'],
    'Bar_Sizes': [144, 120, 96],
    'Cuts': [[13,26, 66], [4,65, 67], [65, 76, 90]]
})

#relative_height = 2 / df['Bar_Sizes'].max()
relative_height = 0.25

bars = plt.barh(df['Lumber'], df['Bar_Sizes'], height = relative_height, color='gray')

for i, row in df.iterrows():
    values = row['Cuts']
    for value in values:
        plt.plot([value, value], [i - relative_height/2, i + relative_height/2], color='blue')

plt.show()
