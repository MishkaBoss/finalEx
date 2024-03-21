import sqlite3
from flask import Flask, render_template, request, redirect, url_for, abort
from init_db import init_database
 



app = Flask(__name__)

init_database()

def get_db_connection():
    con = sqlite3.connect('database.db')
    con.row_factory = sqlite3.Row
    return con

def get_todo(todo_id):
    conn = get_db_connection()
    todo = conn.execute('SELECT * FROM todos WHERE id = ?',
                        (todo_id,)).fetchone()
    conn.close()
    if todo is None:
        abort(404)
    return todo


@app.route('/')
def index():
    con = get_db_connection()
    todos = con.execute('SELECT * FROM todos').fetchall()
    con.close()
    return render_template('index.html', todos=todos)



@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        con = get_db_connection()
        con.execute('INSERT INTO todos (title, content) VALUES (?,?)',(title,content))
        con.commit()
        con.close()
        return redirect(url_for('index'))

    return render_template('create.html')

# ...

@app.route('/<int:id>/edit/', methods=('GET', 'POST'))
def edit(id):
    todo = get_todo(id)
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        conn = get_db_connection()
        conn.execute('UPDATE todos SET title = ?, content = ?'
                         ' WHERE id = ?',
                         (title, content, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('edit.html', todo=todo)


@app.route('/<int:id>/delete/', methods=('GET','POST'))
def delete(id):
    todo = get_todo(id)
    print(todo)
    conn = get_db_connection()
    conn.execute('DELETE FROM todos WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    # flash('"{}" was successfully deleted!'.format(todo['title']))
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

