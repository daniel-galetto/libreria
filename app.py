from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Libro

app = Flask(__name__)

# CREA LA BASE DE DATOS Y LA SESION
engine = create_engine('sqlite:///libros.db?check_same_thread=False')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# INGRESA A LA HOME PAGE VISUALIZA TODOS LOS LIBROS
@app.route('/')
@app.route('/libros')
def mostrarLibros():
    libros = session.query(Libro).all()
    return render_template('libros.html', libros=libros)

# ORDEN ALFABETICO TITULO / GENERO / AUTOR
@app.route('/orden/titulo')
def ordenLibrosTitulo():
    libros = session.query(Libro).order_by(Libro.titulo).all()
    return render_template('libros.html', libros=libros)

@app.route('/orden/genero')
def ordenLibrosGenero():
    libros = session.query(Libro).order_by(Libro.genero)
    return render_template('libros.html', libros=libros)

@app.route('/orden/autor')
def ordenLibrosAutor():
    libros = session.query(Libro).order_by(Libro.autor)
    return render_template('libros.html', libros=libros)    


# REDIRECCIONA A LA PAGUINA RECOMIENDA 
@app.route('/recomienda')
def recomiendaLibro(): 
    libros = session.query(Libro).all()
    return render_template('recomiendaLibro.html', libros=libros) 


# CREA UN NUEVO LIBRO Y LO GUARDA EN LA BASE DE DATOS
@app.route('/libros/nuevo/', methods=['GET', 'POST'])
def nuevoLibro():
    if request.method == 'POST':
        nuevoLibro = Libro(titulo=request.form['nombre'],   
                       autor=request.form['autor'],
                       genero=request.form['genero'])
        session.add(nuevoLibro)
        session.commit()
        return redirect(url_for('mostrarLibros'))
    else:
        return render_template('nuevoLibro.html')


# ACTULIZA / EDITA LOS LIBROS Y LOS GUARDA EN LA BASE DE DATOS
@app.route("/libros/<int:libro_id>/editar/", methods=['GET', 'POST'])
def editarLibro(libro_id):
    libroEditado = session.query(Libro).filter_by(id=libro_id).one()
    if request.method == 'POST':
        if request.form['nombre']: 
            libroEditado.titulo = request.form['nombre'] 
            libroEditado.autor = request.form['autor'] 
            libroEditado.genero = request.form['genero'] 
            session.commit() 
        return redirect(url_for('mostrarLibros')) # modificacion de identacion bug en boton volver
    else:
        return render_template('editarLibro.html', libro=libroEditado)


# BORRA EL LIBRO
@app.route('/libros/<int:libro_id>/eliminar/', methods=['GET', 'POST'])
def eliminarLibro(libro_id):
    libroAEliminar = session.query(Libro).filter_by(id=libro_id).one()
    if request.method == 'POST':
        session.delete(libroAEliminar)
        session.commit()
        return redirect(url_for('mostrarLibros', libro_id=libro_id))
    else:
        return render_template('eliminarLibro.html', libro=libroAEliminar)


if __name__ == '__main__':
    app.run(debug=True)