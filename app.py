from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, IntegerField, FieldList, FormField
from passlib.hash import sha256_crypt
from functools import wraps
from datetime import datetime


current_time = datetime.now()

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'myflaskapp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/articles')
def articles():
    cur = mysql.connection.cursor()

    result = cur.execute("SELECT * FROM articles")

    articles = cur.fetchall()

    if result > 0:
        return render_template('articles.html', articles=articles)
    else:
        msg = 'No Articles Found'
        return render_template('articles.html', msg=msg)
    cur.close()


@app.route('/article/<string:id>/')
def article(id):
    cur = mysql.connection.cursor()

    result = cur.execute("SELECT * FROM articles WHERE id = %s", [id])

    article = cur.fetchone()

    return render_template('article.html', article=article)


class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        cur = mysql.connection.cursor()

        cur.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)", (name, email, username, password))

        mysql.connection.commit()

        cur.close()

        flash('You are now registered and can log in', 'success')

        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password_candidate = request.form['password']

        cur = mysql.connection.cursor()

        result = cur.execute("SELECT * FROM users WHERE username = %s", [username])

        if result > 0:
            data = cur.fetchone()
            password = data['password']

            if sha256_crypt.verify(password_candidate, password):
                session['logged_in'] = True
                session['username'] = username

                flash('You are now logged in', 'success')
                return redirect(url_for('dashboard'))
            else:
                error = 'Invalid login'
                return render_template('login.html', error=error)
            cur.close()
        else:
            error = 'Username not found'
            return render_template('login.html', error=error)

    return render_template('login.html')

def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap

@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))

@app.route('/dashboard')
@is_logged_in
def dashboard():
    cur = mysql.connection.cursor()

    result = cur.execute("SELECT * FROM articles")

    articles = cur.fetchall()

    if result > 0:
        return render_template('dashboard.html', articles=articles)
    else:
        msg = 'No Articles Found'
        return render_template('dashboard.html', msg=msg)
    cur.close()

class Instructionform(Form):
    instruction_id = IntegerField('instructions.key')
    content = StringField('instructions.valye')

class ArticleForm(Form):
    recipe_name = StringField('recipe_name', [validators.Length(min=1, max=200)])
    ingredients = FieldList('ingredients')
    instructions = FieldList(FormField(Instructionform))
    serving_size = IntegerField('serving_size')
    category = StringField('category')
    notes = FieldList('notes')
    date_added = StringField('date_added')
    date_modified = StringField('date_modified')

@app.route('/add_article', methods=['GET', 'POST'])
@is_logged_in
def add_article():
    form = ArticleForm(request.form)
    if request.method == 'POST' and form.validate():
        recipe_name = form.recipe_name.data
        ingredients = form.ingredients.data
        instructions = form.instructions.data
        serving_size = form.serving_size.data
        category = form.category.data
        notes = form.notes.data
        date_added = form.date_added.data
        date_modified = form.date_modified.data

        cur = mysql.connection.cursor()

        cur.execute("INSERT INTO articles(recipe_name, ingredients, instructions, serving_size, category, notes, date_added, date_modified, author) VALUES(%s, %s, %s)",
                    (recipe_name,
                     ingredients,
                     instructions,
                     serving_size,
                     category,
                     notes,
                     date_added,
                     date_modified,
                     session['username']))

        mysql.connection.commit()

        cur.close()

        flash('Article Created', 'success')

        return redirect(url_for('dashboard'))

    return render_template('add_article.html', form=form)


@app.route('/edit_article/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def edit_article(id):
    cur = mysql.connection.cursor()

    result = cur.execute("SELECT * FROM articles WHERE id = %s", [id])

    article = cur.fetchone()
    cur.close()
    form = ArticleForm(request.form)

    form.recipe_name.data = article['recipe_name']
    form.ingredients.data = article['ingredients']
    form.instructions.data = article['instructions']
    form.serving_size.data = article['serving_size']
    form.category.data = article['category']
    form.notes.data = article['notes']
    form.date_added.data = article['date_added']
    form.date_modified.data = article['date_modified']

    if request.method == 'POST' and form.validate():
        recipe_name = request.form['recipe_name']
        ingredients = request.form['ingredients']
        instructions = request.form['instructions']
        serving_size = request.form['serving_size']
        category = request.form['category']
        notes = request.form['notes']
        date_added = request.form['date_added']
        date_modified = current_time.strftime('%m/%d/%Y')

        cur = mysql.connection.cursor()
        app.logger.info(recipe_name)
        cur.execute ("UPDATE articles SET recipe_name=%s, ingredients=%s, instructions=%s, serving_size=%s, category=%s, notes=%s date_added=%s WHERE id=%s",(recipe_name, ingredients, instructions, serving_size, category, notes, date_added, date_modified, id))
        mysql.connection.commit()

        cur.close()

        flash('Article Updated', 'success')

        return redirect(url_for('dashboard'))

    return render_template('edit_article.html', form=form)

@app.route('/delete_article/<string:id>', methods=['POST'])
@is_logged_in
def delete_article(id):
    cur = mysql.connection.cursor()

    cur.execute("DELETE FROM articles WHERE id = %s", [id])

    mysql.connection.commit()

    cur.close()

    flash('Article Deleted', 'success')

    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.secret_key='secret123'
    app.run(debug=True)
