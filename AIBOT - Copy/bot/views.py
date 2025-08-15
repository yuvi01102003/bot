from flask import Flask, Blueprint, render_template, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from .models import Users, Chats
from bot import db


views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def indexPage():
    if request.method == 'POST':
        userinput = request.form.get('userinput')
        flash('Please wait for a moment', category='error')
        if userinput:
            import google.generativeai as genai
            import time

            genai.configure(api_key="AIzaSyDDahx4sA4UJOoVmCbWdZ-OoCvqDVoYUbE")

            model = genai.GenerativeModel("gemini-1.5-flash")

            while True:
                try:
                    prompt = userinput
                    response = model.generate_content(prompt)
                    new_chat = Chats(userip=userinput, aiop=response.text, user_id=current_user.id)
                    db.session.add(new_chat)
                    db.session.commit()
                    break
                except Exception as e:
                    print("Error:", e)
                    print("Retrying in 5 seconds...")
                    flash('error', category='error')
                    time.sleep(5)
        else:
            flash('Ask Something Interesting', category='error')
    return render_template('home.html', user=current_user)

