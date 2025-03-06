from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import pymysql
from dotenv import load_dotenv
import os
pymysql.install_as_MySQLdb()

load_dotenv()

app = Flask(__name__)

# Configurações do banco de dados MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa o banco de dados
db = SQLAlchemy(app)


# Modelo de Jogo
class Jogo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data_partida = db.Column(db.Date, nullable=False)
    time1 = db.Column(db.String(100), nullable=False)
    time2 = db.Column(db.String(100), nullable=False)
    gols_time1 = db.Column(db.Integer, nullable=False)
    gols_time2 = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Jogo {self.time1} vs {self.time2} - {self.data_partida}>'


# Cria as tabelas no banco de dados
with app.app_context():
    db.create_all()


# Página inicial que exibe todos os jogos
@app.route('/')
def index():
    jogos = Jogo.query.all()
    return render_template('index.html', jogos=jogos)


# Página para criar ou editar um jogo
@app.route('/jogo', methods=['GET', 'POST'])
@app.route('/jogo/<int:id>', methods=['GET', 'POST'])
def jogo(id=None):
    if id:
        jogo = Jogo.query.get_or_404(id)
    else:
        jogo = Jogo()

    if request.method == 'POST':
        jogo.data_partida = request.form['data_partida']
        jogo.time1 = request.form['time1']
        jogo.time2 = request.form['time2']
        jogo.gols_time1 = int(request.form['gols_time1'])
        jogo.gols_time2 = int(request.form['gols_time2'])

        if not id:  # Se não for edição, é criação
            db.session.add(jogo)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('jogo.html', jogo=jogo)


# Página para excluir um jogo
@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    jogo = Jogo.query.get_or_404(id)
    db.session.delete(jogo)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
