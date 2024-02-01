from flask import Blueprint, render_template, redirect

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return redirect("/calc", code=302)

