from flask import Blueprint, render_template, request 

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
def sign_up():
    data = None
    if request.method == 'POST': 
        #add checks for valid input
        #flesh messages as needed 
        size_1 = int(request.form.get("raw_lumber_length_1"))
        size_2 = int(request.form.get("raw_lumber_length_2"))
        size_3 = int(request.form.get("raw_lumber_length_3"))
        piece_list = request.form.get("piece_list")
        print("SUBMIT WAS DEPRESSED")
        print(size_1, size_2, size_3, piece_list)
    return render_template("calculator.html", text="Testing Calculator Text", boolean=True)        

