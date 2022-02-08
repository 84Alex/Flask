import traceback

from Tools.scripts.make_ctype import method
from flask import Flask, render_template, url_for, redirect, session, flash, request
from datetime import datetime
import random
from src import Database
from validators import Auth, Marca


app = Flask(__name__)
app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['TESTING'] = True
app.config['SECRET_KEY'] = random._urandom(24)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/auth', methods=['POST', 'GET'])
def authenticate():
    form = Auth.Login()
    return render_template('authentication/login.html', form=form)


# Method Login - Authenticate


@app.route('/login', methods=['POST', 'GET'])
def auth():
    cn = Database.connect()
    form = Auth.Login()
    if request.method == 'POST':
        if form.validate_on_submit():
            u = form.user.data
            p = form.passw.data
            with cn.cursor() as cursor:
                sql = "SELECT * FROM User WHERE email=%s"
                cursor.execute(sql, (u,))
                account = cursor.fetchone()
                if account:
                    if account[5] == p and account[8] == 1:
                        session['loggedin'] = True
                        session['id'] = account[0]
                        session['user'] = account[1]
                        return redirect(url_for('dashboard'))
                        return render_template('dashboard.html', user=session['user'])
                    else:
                        flash('Usuario y/o Clave incorrectos')
                        return redirect(url_for('authenticate'))
                else:
                    flash('El usuario no se encuentra registrado en el sistema')
                    return redirect(url_for('authenticate'))

    return render_template('authentication/login.html', form=form)


@app.route('/dashboard', methods=["POST", "GET"])
def dashboard():
    if 'loggedin' in session:
        return render_template('dashboard.html', user=session['user'])
    else:
        flash('Debe Iniciar sesion')
        return redirect(url_for('authenticate'))


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('user', None)
    return redirect(url_for('authenticate'))


# Modulo Marcas
@app.route('/marcas', methods=['POST', 'GET'])
def marca():
    cn = Database.connect()
    if 'loggedin' in session:
        # List all Marcas
        with cn.cursor() as cursor:
            sql = "SELECT * FROM Marca ORDER BY id DESC"
            cursor.execute(sql)
            rows = cursor.fetchall()
        return render_template('marca/marca.html', user=session['user'], rows=rows)
        cn.close()
    else:
        flash('Debe Iniciar sesion')
        return redirect(url_for('authenticate'))


@app.route('/registro/marca', methods=['GET'])
def register_marca():
    form = Marca.Marca()
    cd = datetime.now()
    return render_template('marca/marca_new.html', form=form, cd=cd)


@app.route('/marca-store', methods=['POST'])
def marca_store():
    cn = Database.connect()
    form = Marca.Marca()
    cd = datetime.now()
    e = 1
    if request.method == 'POST':
        if form.validate_on_submit():
            m = form.marca.data
            d = form.description.data
            with cn.cursor() as cursor:
                sql = "INSERT INTO marca (marca, description, create_at, estado) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (m, d, cd, e))
                try:
                    cn.commit()
                    cn.close()
                    flash('La Marca ha sido registrada de forma exitosa!!')
                    return redirect(url_for('marca'))
                except:
                    traceback.print_exc()
                    flash('Error al registrar la Marca')
                    return redirect(url_for('marca'))

    return render_template('marca/marca_new.html', form=form, cd=cd)


# show marca

@app.route('/marca/show/<int:id>', methods=['GET'])
def marca_show(id):
    cn = Database.connect()
    id = request.args.get('id', id, type=int)
    if request.method == 'GET':
        with cn.cursor() as cursor:
            sql = "SELECT * FROM marca WHERE id = %s"
            cursor.execute(sql, (id,))
            row = cursor.fetchone()
            if row is not None:
                return render_template('marca/show.html', row=row)
            else:
                flash('La marca no se encuentra registrada')
                return redirect(url_for('marca'))
    return render_template('marca/marca.html', id=id)


@app.route('/marca/edit/<int:id>', methods=['GET'])
def marca_edit(id):
    cn = Database.connect()
    form = Marca.Marca()
    id = request.args.get('id', id, type=int)
    with cn.cursor() as cursor:
        sql = "SELECT * FROM marca WHERE id = %s"
        cursor.execute(sql, (id,))
        row = cursor.fetchone()
        return render_template('marca/edit.html', row=row, form=form)

    return render_template('marca/marca.html', id=id)


@app.route('/maraca/update', methods=['POST', 'PUT'])
def marca_update():
    cn = Database.connect()
    form = Marca.Marca()
    if request.method == 'POST':
        if form.validate_on_submit():
            i = request.form['id']
            e = request.form['estado']
            m = form.marca.data
            d = form.description.data
            print(i, m, d, e)
            with cn.cursor() as cursor:
                sql = "UPDATE marca SET marca=%s, description=%s, estado=%s WHERE id=%s"
                cursor.execute(sql, (m, d, e, i,))
                try:
                    cn.commit()
                    cn.close()
                    flash('La marca ha sido actualizada')
                    return redirect(url_for('marca'))
                except:
                    traceback.print_exc()
                    flash('Ooops!!, ha ocurrido un error al actualizar la Marca')
                    return redirect(url_for('marca'))

    return render_template('marca/edit.html', form=form)


@app.route('/marca/delete/<int:id>', methods=['GET'])
def marca_delete(id):
    cn = Database.connect()
    form = Marca.Marca()
    id = request.args.get('id', id, type=int)
    with cn.cursor() as cursor:
        sql = "SELECT * FROM Marca WHERE id=%s"
        cursor.execute(sql, (id,))
        row = cursor.fetchone()
        print(row)
        if row[4] == 1:
            flash("La marca no se puede eliminar debido a que se encuentra Activa")
            return redirect(url_for('marca'))
        else:
            query = "DELETE FROM Marca WHERE id=%s"
            print('estoy antes del query delete')
            print(cursor.execute(query, (id,)))
            cn.commit()
            cn.close()
            flash('La marca ha sido emiminada')
            return redirect(url_for('marca'))

    return render_template('marca/marca.html', form=form)


if __name__ == '__main__':
    app.run(port=5000, debug=True)
