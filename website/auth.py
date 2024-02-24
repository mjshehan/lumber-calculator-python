from flask import Blueprint, render_template, request, flash, redirect 
from board_cutter_2_knap import calculate
from make_visual import make_visual
import matplotlib.pyplot as pltp

auth = Blueprint('auth', __name__)

"""
"""
@auth.route('/')
def home():
    return redirect('/calc', code=302)

@auth.route('/about')
def about():
    return render_template("about.html")        

    
@auth.route('/instructions')
def Instructions():
    return render_template("instructions.html", table="", boolean=False)

@auth.route('/calc', methods = ['GET', 'POST'])


def calculator(): 
    data = None
    text = "Welcome!"
    text2 = ""
    text3 = ""
    
    def convert_list(list):
        str_list = []
       
        for entry in list:
            if entry.isdigit() == False and entry != " " and entry != "":
                print("found a bad piece")
                return False
            if entry != "":
                str_list.append((entry))
        int_list = []
        for entry in str_list:
            int_list.append( int(entry))
        return int_list
    
    if request.method == 'POST': 

        raw_units = request.form.get("unit_input")
        cut_units = request.form.get("cut_unit_input")
       
        #conversion factor -- use inches as base unit
        # if raw_units == inches then do nothing
        # if raw units == feet then multiply by 12
        # if raw units = cm then multiply by 0.393701

        #transform INPUT

        #inverse transform OUTPUT


        if not request.form.get("raw_lumber_length_1").strip().isdigit():
            flash('Please enter a valid number for Size 1', 'error')
            return render_template("calculator.html", table="", boolean=False)
        else:
            size_1 = int(request.form.get("raw_lumber_length_1").strip())
        
        size_2_input = request.form.get("raw_lumber_length_2").strip()  
        if size_2_input is None or size_2_input == "":
            size_2 = 0
        elif size_2_input.isdigit() == False :
            flash('Please enter a valid number for Size 2', 'error')
            return render_template("calculator.html", table="", boolean=False)
        elif size_2_input.isdigit() == True: 
            size_2 = int(size_2_input.strip())
            
        size_3_input = request.form.get("raw_lumber_length_3") .strip() ##
        if size_3_input is None or size_3_input == "":
            size_3 = 0
        elif size_3_input.isdigit() == False:
            flash('Please enter a valid number for Size 3', 'error')
            return render_template("calculator.html", table="", boolean=False)
        elif size_3_input.isdigit() == True: 
            size_3 = int(size_3_input.strip())


        piece_list = convert_list((request.form.get("piece_list")).replace(" ", ",").split(","))
        if piece_list == False:
            flash('You have an invalid value in your list of pieces', 'error')
            return render_template("calculator.html", table="", boolean=False)
           
        lumber = [12*size_1, 12*size_2, 12*size_3]
        for piece in piece_list:
            if piece > max(size_1*12, size_2*12, size_3*12):
                flash('One of your cut pieces is too darn big for the lumber sizes', 'error')
                return render_template("calculator.html", table="", boolean=False)
        solution_df = calculate(lumber, piece_list)

        curated_df = solution_df[['lumber length', 'cuts', 'inches used', 'waste' ]]

        print(curated_df.columns)
        for index, row in curated_df.iterrows():
            curated_df.loc[index, 'lumber length'] = int(row['lumber length'])//12
            curated_df.loc[index, 'cuts'] = ', '.join(map(str, row['cuts']))
        raw_units = "ft"
        cut_units = "in"
        cut_title = "Inches"
        curated_df.rename(columns={'lumber length': f'Lumber Length ({raw_units})'}, inplace=True)
        curated_df.rename(columns={'cuts': f'Cuts ({cut_units})'}, inplace=True)
        curated_df.rename(columns={'inches used': f'{cut_title} Used'}, inplace=True)
        curated_df.rename(columns={'waste': f'Waste ({cut_units})'}, inplace=True)
        curated_df.insert(0, '#', range(1, len(curated_df)+1))
        table = curated_df.to_html(classes='table table-striped',
                                   index=False)
        total_waste = sum(solution_df['waste'])
        total_needed = sum(piece_list)
        text2 = f"Total Waste = " + str(total_waste) + " inches" 
        text3 = f"Percent Waste = " + str(round(total_waste/total_needed*100, 2)) + "%"
   
        make_visual(solution_df) 
      
    else:
        table = ""

    return render_template("calculator.html", text2=text2, text3=text3, table=table, boolean=True)        

