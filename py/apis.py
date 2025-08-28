from flask import Blueprint, request, jsonify
from py.db import db   
import base64
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user 
apis = Blueprint("apis", __name__)

class Curso(db.Model):
    __tablename__ = "cursos"
    id_curso = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(50), default="-")

class CursoUsuario(db.Model):
    __tablename__ = "cursos_usuarios"
    id_conexion = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_curso = db.Column(db.Integer, db.ForeignKey("cursos.id_curso", ondelete="CASCADE", onupdate="CASCADE"))
    email = db.Column(db.String(40), db.ForeignKey("usuario.email", ondelete="SET NULL", onupdate="CASCADE"))

class Post(db.Model):
    __tablename__ = "posts"
    id_post = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_curso = db.Column(db.Integer, db.ForeignKey("cursos.id_curso"))
    titulo = db.Column(db.String(100), default="-")
    contenido = db.Column(db.Text)
    autor = db.Column(db.String(40))  
    fecha_publicacion = db.Column(db.DateTime, server_default=db.func.now())


class Entrega(db.Model):
    __tablename__ = "entrega"
    id_entrega = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_post = db.Column(db.Integer, db.ForeignKey("posts.id_post"))
    autor = db.Column(db.String(40))  
    fecha_entrega = db.Column(db.DateTime, server_default=db.func.now())

class Archivo(db.Model):
    __tablename__ = "archivos"
    id_archivo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_post = db.Column(db.Integer, db.ForeignKey("posts.id_post"))
    id_entrega = db.Column(db.Integer, db.ForeignKey("entrega.id_entrega"))
    tipo = db.Column(db.String(50))
    tamano = db.Column(db.BigInteger)
    pixel = db.Column(db.LargeBinary) 

class Comentario(db.Model):
    __tablename__ = "comentario"
    id_comentario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_post = db.Column(db.Integer, db.ForeignKey("posts.id_post"))
    autor = db.Column(db.String(40))  
    contenido = db.Column(db.Text)
    fecha_comentario = db.Column(db.DateTime, server_default=db.func.now())


@apis.route("/api/posts", methods=["POST"])
def add_post():
    id_curso = request.form.get("id_curso")
    titulo = request.form.get("titulo", "")
    contenido = request.form.get("contenido")
    autor = request.form.get("autor")
    archivo = request.files.get("archivo")

    nuevo_post = Post(
        id_curso=id_curso,
        titulo=titulo,
        contenido=contenido,
        autor=autor
    )
    db.session.add(nuevo_post)
    db.session.commit()

    if archivo:
        data = archivo.read() 
        nuevo = Archivo(
            id_post=nuevo_post.id_post,  
            id_entrega=request.form.get("id_entrega"),
            tipo=archivo.content_type,
            tamano=len(data),
            pixel=data
        )
        db.session.add(nuevo)
        db.session.commit()

    return jsonify(success=True, post={"id_post": nuevo_post.id_post})

@apis.route("/api/cursos", methods=["GET"])
def get_cursos():
    conexiones = CursoUsuario.query.filter_by(email=current_user.email).all()

    if not conexiones:
        return jsonify(success=False, error="No se encontraron cursos para este usuario"), 404

    cursos_conectados = [cu.id_curso for cu in conexiones]

    cursos = Curso.query.filter(Curso.id_curso.in_(cursos_conectados)).all()

    return jsonify([
        {"id_curso": c.id_curso, "nombre": c.nombre}
        for c in cursos
    ])


@apis.route("/api/cursos/<int:id>", methods=["PUT"])
def update_curso(id):

    curso = Curso.query.get(id)
    if not curso:
        return jsonify(success=False, error="Curso no encontrado"), 404
    data = request.get_json()
    curso.nombre = data.get("nombre", curso.nombre)
    db.session.commit()
    return jsonify(success=True)


@apis.route("/api/cursos/<int:id>", methods=["DELETE"])
def delete_curso(id):
    curso = Curso.query.get(id)
    if not curso:
        return jsonify(success=False, error="Curso no encontrado"), 404
    db.session.delete(curso)
    db.session.commit()
    return jsonify(success=True)



@apis.route("/api/posts", methods=["GET"])
def get_posts():
    posts = Post.query.all()
    result = []
    for p in posts:
        result.append({
            "id_post": p.id_post,
            "id_curso": p.id_curso,
            "titulo": p.titulo,
            "contenido": p.contenido,
            "autor": p.autor,
            "fecha_publicacion": p.fecha_publicacion
        })
    return jsonify(result)

@apis.route("/api/posts/<int:id>", methods=["PUT"])
def update_post(id):
    post = Post.query.get(id)
    if not post:
        return jsonify(success=False, error="Post no encontrado"), 404
    data = request.get_json()
    post.titulo = data.get("titulo", post.titulo)
    post.contenido = data.get("contenido", post.contenido)
    post.id_curso = data.get("id_curso", post.id_curso)
    db.session.commit()
    return jsonify(success=True)


@apis.route("/api/posts/<int:id>", methods=["DELETE"])
def delete_post(id):
    post = Post.query.get(id)
    if not post:
        return jsonify(success=False, error="Post no encontrado"), 404
    db.session.delete(post)
    db.session.commit()
    return jsonify(success=True)

@apis.route("/api/entregas", methods=["POST"])
def add_entrega():
    data = request.get_json()
    nueva = Entrega(
        id_post=data.get("id_post"),
        autor=data.get("autor")
    )
    db.session.add(nueva)
    db.session.commit()
    return jsonify(success=True, entrega={"id_entrega": nueva.id_entrega})


@apis.route("/api/entregas", methods=["GET"])
def get_entregas():
    entregas = Entrega.query.all()
    return jsonify([
        {"id_entrega": e.id_entrega, "id_post": e.id_post, "autor": e.autor, "fecha_entrega": e.fecha_entrega}
        for e in entregas
    ])



@apis.route("/api/archivos/<int:id>", methods=["GET"])
def get_archivos(id):
    archivos = Archivo.query.filter_by(id_post=id).all()
    return jsonify([
        {
            "id_archivo": a.id_archivo,
            "id_entrega": a.id_entrega,
            "tipo": a.tipo,
            "tamano": a.tamano,
            "pixel": base64.b64encode(a.pixel).decode("utf-8") if a.pixel else None
        } for a in archivos
    ])



@apis.route("/api/comentarios", methods=["POST"])
def add_comentario():
    data = request.get_json()
    nuevo = Comentario(
        id_post=data.get("id_post"),
        autor=data.get("autor"),
        contenido=data.get("contenido")
    )
    db.session.add(nuevo)
    db.session.commit()
    return jsonify(success=True, comentario={"id_comentario": nuevo.id_comentario})


@apis.route("/api/comentarios", methods=["GET"])
def get_comentarios():
    comentarios = Comentario.query.all()
    return jsonify([
        {
            "id_comentario": c.id_comentario,
            "id_post": c.id_post,
            "autor": c.autor,
            "contenido": c.contenido,
            "fecha_comentario": c.fecha_comentario
        }
        for c in comentarios
    ])


@apis.route("/api/cursos_usuarios", methods=["POST"])
def add_curso_usuario():
    data = request.get_json()
    nuevo = CursoUsuario(
        id_curso=data.get("id_curso"),
        email=data.get("email")
    )
    db.session.add(nuevo)
    db.session.commit()
    return jsonify(success=True, conexion={
        "id_conexion": nuevo.id_conexion,
        "id_curso": nuevo.id_curso,
        "email": nuevo.email
    })

@apis.route("/api/cursos_usuarios/<int:id>", methods=["GET"])
def get_cursos_usuarios(id):
    conexiones = CursoUsuario.query.filter_by(id_curso=id).all()

    if not conexiones:
        return jsonify(success=False, error="No se encontraron cursos para este usuario"), 404

    cursos = [cu.email for cu in conexiones]
    return jsonify(cursos)


@apis.route("/api/cursos_usuarios/<int:id>/<string:email>", methods=["DELETE"])
def delete_cursos_usuarios(id,email):
    conexion = CursoUsuario.query.filter_by(id_curso=id, email=email).first()
    if not conexion:
        return jsonify(success=False, error="conexion no encontrada"), 404
    
    db.session.delete(conexion)
    db.session.commit()
    return jsonify(success=True)