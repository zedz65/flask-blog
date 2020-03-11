
from flask import render_template, redirect, url_for, request
from application import app, db, bcrypt
from application.models import Posts, Users
from flask_login import login_user, current_user, logout_user,login_required
from application.forms import PostForm, RegistrationForm, LoginForm

@app.route('/')
@app.route('/home')
def home():
 postData = Posts.query.all() #all shows all entries(but then add loop in home)
 return render_template('home.html', title='Home', post=postData)

@app.route('/about')
def about():
 return render_template('about.html', title='About')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hash_pw = bcrypt.generate_password_hash(form.password.data)

        user = Users(email=form.email.data, password=hash_pw)

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('post'))
    return render_template('register.html', title='Register', form=form)



@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated: #checks to see if user is already logged in
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit(): #if the form is valid- check if username or pass exist using bcrypt
        user=Users.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data): #if correct log in user
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next') #after log in go to next page
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('home')) #else go back to home
    return render_template('login.html', title='Login', form=form)



@app.route('/post', methods=['GET', 'POST']) #post refers to plog post page and POST refers to method
@login_required
def post():
    form = PostForm()
    if form.validate_on_submit():
        postData = Posts(
            first_name = form.first_name.data,
            last_name = form.last_name.data,
            title = form.title.data,
            content = form.content.data
        )

        db.session.add(postData)
        db.session.commit()

        return redirect(url_for('home'))

    else:
        print(form.errors)

    return render_template('post.html', title='Post', form=form)



@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))