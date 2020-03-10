
from flask import render_template, redirect, url_for
from application import app, db
from application.models import Posts
from application.forms import PostForm

@app.route('/')
@app.route('/home')
def home():
 postData = Posts.query.all() #all shows all entries(but then add loop in home)
 return render_template('home.html', title='Home', post=postData)

@app.route('/about')
def about():
 return render_template('about.html', title='About')

@app.route('/register')
def register():
 return render_template('register.html', title='Register')


@app.route('/post', methods=['GET', 'POST']) #post refers to plog post page and POST refers to method
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