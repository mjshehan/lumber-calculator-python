from flask import Blueprint, render_template, request, flash 
from board_cutter_2_knap import calculate

auth = Blueprint('auth', __name__)

"""
"""
@auth.route('/login')
def login():
    return "<p>Login</p>"
    
@auth.route('/logout')
def logout():
    return "<p>Logout</p>"

@auth.route('/calc', methods = ['GET', 'POST'])


def calculator(): 
    data = None
    text = "Welcome!"
    def hello():
        print("hello world")

    def convert_list(list):
        str_list = []
        for entry in list:
            if entry != "":
                str_list.append((entry))
        int_list = []
        for entry in str_list:
            int_list.append( int(entry))
        return int_list
    
    if request.method == 'POST': 
        #add checks for valid input
        #flsh messages as needed 
        if not request.form.get("raw_lumber_length_1").isdigit():
            flash('Please enter a valid number for Size 1', 'error')
            return render_template("calculator.html", table="", boolean=False)
        else:
            size_1 = int(request.form.get("raw_lumber_length_1"))

        size_2_input = request.form.get("raw_lumber_length_2")  
        if size_2_input is None or size_2_input.strip() == "":
            size_2 = 0
        elif size_2_input.isdigit() == False:
            flash('Please enter a valid number for Size 2', 'error')
            return render_template("calculator.html", table="", boolean=False)
        elif size_2_input.isdigit() == True: 
            size_2 = int(size_2_input)
            
        #ADD SIZE 3 EXCEPTION HANDLING
        #size_3 = int(request.form.get("raw_lumber_length_3"))
        #---- SIZE 3 THROWING ERROR
        size_3_input = request.form.get("raw_lumber_length_3")  
        if size_3_input is None or size_3_input.strip() == "":
            size_3 = 0
        elif size_3_input.isdigit() == False:
            flash('Please enter a valid number for Size 2', 'error')
            return render_template("calculator.html", table="", boolean=False)
        elif size_3_input.isdigit() == True: 
            size_3 = int(size_3_input)


        piece_list = convert_list((request.form.get("piece_list")).replace(" ", ",").split(","))
        print("SUBMIT WAS DEPRESSED -- let's cheer it up")
        print(type(piece_list), piece_list, type(piece_list[0]))
        print(piece_list)
        lumber = [12*size_1, 12*size_2, 12*size_3]
        
        solution_df = calculate(lumber, piece_list)
        print(solution_df)
        table = solution_df.to_html()
        print("Lumber options = ", lumber, "Piece List = ", piece_list)
        print()
        #---CHECK---convert piece list 
        #---CHECK---call board_cutter_2_knap.py
        #store data
        #render template with data...
        #grouped_df = pd.DataFrame(solution_df.groupby(["bin"]))
        #print(grouped_df)
  
      
    else:
        table = ""

    return render_template("calculator.html", table=table, boolean=True)        

