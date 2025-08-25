from flask import Blueprint, request, jsonify
from py.db import db   # conexión global SQLAlchemy

apis = Blueprint("apis", __name__)

# ============================
# MODELOS
# ============================

class Curso(db.Model):
    __tablename__ = "cursos"
    id_curso = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(50), default="-")


class Post(db.Model):
    __tablename__ = "posts"
    id_post = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_curso = db.Column(db.Integer, db.ForeignKey("cursos.id_curso"))
    titulo = db.Column(db.String(100), default="-")
    contenido = db.Column(db.Text)
    autor = db.Column(db.String(40))  # FK a usuario.email
    fecha_publicacion = db.Column(db.DateTime, server_default=db.func.now())


class Entrega(db.Model):
    __tablename__ = "entrega"
    id_entrega = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_post = db.Column(db.Integer, db.ForeignKey("posts.id_post"))
    autor = db.Column(db.String(40))  # FK a usuario.email
    fecha_entrega = db.Column(db.DateTime, server_default=db.func.now())


class Archivo(db.Model):
    __tablename__ = "archivos"
    id_archivo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_post = db.Column(db.Integer, db.ForeignKey("posts.id_post"))
    id_entrega = db.Column(db.Integer, db.ForeignKey("entrega.id_entrega"))
    ruta_archivo = db.Column(db.String(255), nullable=False)


class Comentario(db.Model):
    __tablename__ = "comentario"
    id_comentario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_post = db.Column(db.Integer, db.ForeignKey("posts.id_post"))
    autor = db.Column(db.String(40))  # FK a usuario.email
    contenido = db.Column(db.Text)
    fecha_comentario = db.Column(db.DateTime, server_default=db.func.now())

# ============================
# RUTAS CRUD
# ============================

# -------- Cursos ----------
@apis.route("/api/cursos", methods=["POST"])
def add_curso():
    data = request.get_json()
    nuevo = Curso(nombre=data.get("nombre", "-"))
    db.session.add(nuevo)
    db.session.commit()
    return jsonify(success=True, curso={"id_curso": nuevo.id_curso, "nombre": nuevo.nombre})


@apis.route("/api/cursos", methods=["GET"])
def get_cursos():
    cursos = Curso.query.all()
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

# -------- Posts ----------
@apis.route("/api/posts", methods=["POST"])
def add_post():
    data = request.get_json()
    nuevo = Post(
        id_curso=data.get("id_curso"),
        titulo=data.get("titulo", "-"),
        contenido=data.get("contenido"),
        autor=data.get("autor")
    )
    db.session.add(nuevo)
    db.session.commit()
    return jsonify(success=True, post={"id_post": nuevo.id_post, "titulo": nuevo.titulo})


@apis.route("/api/posts", methods=["GET"])
def get_posts():
    posts = Post.query.all()
    return jsonify([
        {
            "id_post": p.id_post,
            "id_curso": p.id_curso,
            "titulo": p.titulo,
            "contenido": p.contenido,
            "autor": p.autor,
            "fecha_publicacion": p.fecha_publicacion
        }
        for p in posts
    ])


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

# -------- Entregas ----------
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


# -------- Archivos ----------
@apis.route("/api/archivos", methods=["POST"])
def add_archivo():
    data = request.get_json()
    nuevo = Archivo(
        id_post=data.get("id_post"),
        id_entrega=data.get("id_entrega"),
        ruta_archivo=data["ruta_archivo"]
    )
    db.session.add(nuevo)
    db.session.commit()
    return jsonify(success=True, archivo={"id_archivo": nuevo.id_archivo, "ruta_archivo": nuevo.ruta_archivo})


@apis.route("/api/archivos", methods=["GET"])
def get_archivos():
    archivos = Archivo.query.all()
    return jsonify([
        {"id_archivo": a.id_archivo, "id_post": a.id_post, "id_entrega": a.id_entrega, "ruta_archivo": a.ruta_archivo}
        for a in archivos
    ])


# -------- Comentarios ----------
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
