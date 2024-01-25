import mysql.connector
from flask import Flask, render_template, redirect, request, flash, url_for

app = Flask(__name__)
# Configurando a chave secreta
app.secret_key = 'flash_message'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'sua senha'
app.config['MYSQL_DB'] = 'seu banco'

mysql_conn = mysql.connector.connect(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'],
    password=app.config['MYSQL_PASSWORD'],
    database=app.config['MYSQL_DB']
)

@app.route('/')
def home():
    cursor = mysql_conn.cursor()
    cursor.execute("SELECT * FROM estudantes")
    data = cursor.fetchall()
    cursor.close()
    return render_template('home.html', estudantes=data)


@app.route('/insert', methods = ['POST'])
def insert():
    flash("Estudante adicionado com sucesso!")
    if request.method == "POST":
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        
        # INSERIR OS DADOS
        cursor = mysql_conn.cursor()
        query = 'INSERT INTO estudantes (nome, email, phone) VALUES (%s, %s, %s)'
        cursor.execute(query, (nome, email, telefone))
        mysql_conn.commit()
        return redirect(url_for('home'))
    
@app.route('/update', methods = ['POST', 'GET'])
def update():
    id_data = request.form['id']
    nome = request.form['nome']
    email = request.form['email']
    telefone = request.form['telefone']
    
    cursor = mysql_conn.cursor()
    cursor.execute("""
     UPDATE estudantes
     SET nome = %s, email = %s, phone = %s
     WHERE id = %s         
    """, (nome, email, telefone, id_data))
    flash("Estudante atualizado com sucesso!")
    mysql_conn.commit()
    return redirect(url_for('home'))

@app.route('/delete/<string:id_data>', methods = ['GET'])
def delete(id_data):
    cursor = mysql_conn.cursor()
    cursor.execute("DELETE FROM estudantes WHERE id = %s", (id_data,))
    flash("Estudante deletado com sucesso!")
    mysql_conn.commit()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)
