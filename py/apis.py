from flask import Blueprint, request, jsonify
from py.db import db   
import base64
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import random
import string

def generar_codigo():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
 
apis = Blueprint("apis", __name__)

class Curso(db.Model):
    __tablename__ = "cursos"
    nombre = db.Column(db.String(50), default="-")
    codigo = db.Column(db.String(20),  primary_key=True)

class CursoUsuario(db.Model):
    __tablename__ = "cursos_usuarios"
    id_conexion = db.Column(db.Integer, primary_key=True, autoincrement=True)
    codigo = db.Column(db.String(20), db.ForeignKey("cursos.codigo", ondelete="CASCADE", onupdate="CASCADE"))
    email = db.Column(db.String(40), db.ForeignKey("usuario.email", ondelete="SET NULL", onupdate="CASCADE"))

class Post(db.Model):
    __tablename__ = "posts"
    id_post = db.Column(db.Integer, primary_key=True, autoincrement=True)
    codigo = db.Column(db.String(20), db.ForeignKey("cursos.codigo"))
    contenido = db.Column(db.Text)
    autor = db.Column(db.String(40))  
    fecha_publicacion = db.Column(db.DateTime, server_default=db.func.now())

class Tarea(db.Model):
    __tablename__ = "Tarea"
    id_tarea = db.Column(db.Integer, primary_key=True, autoincrement=True)
    codigo = db.Column(db.String(20), db.ForeignKey("cursos.codigo"))
    contenido = db.Column(db.Text)
    autor = db.Column(db.String(40))  
    fecha_publicacion = db.Column(db.DateTime, server_default=db.func.now())
    titulo = db.Column(db.String(100), default="-")

class Entrega(db.Model):
    __tablename__ = "entrega"
    id_entrega = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_tarea = db.Column(db.Integer, db.ForeignKey("Tarea.id_tarea"))
    autor = db.Column(db.String(40), db.ForeignKey("usuario.email"))  
    fecha_entrega = db.Column(db.DateTime, server_default=db.func.now())

class Archivo(db.Model):
    __tablename__ = "archivos"
    id_archivo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_post = db.Column(db.Integer, db.ForeignKey("posts.id_post"))
    id_entrega = db.Column(db.Integer, db.ForeignKey("entrega.id_entrega"))
    tipo = db.Column(db.String(50))
    tamano = db.Column(db.BigInteger)
    pixel = db.Column(db.LargeBinary) 
    nombre = db.Column(db.String(255))

class Comentario(db.Model):
    __tablename__ = "comentario"
    id_comentario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_post = db.Column(db.Integer, db.ForeignKey("posts.id_post"))
    autor = db.Column(db.String(40))  
    contenido = db.Column(db.Text)
    fecha_comentario = db.Column(db.DateTime, server_default=db.func.now())



@apis.route("/api/cursos", methods=["GET"])
def get_cursos():
    conexiones = CursoUsuario.query.filter_by(email=current_user.email).all()

    if not conexiones:
        return jsonify(success=False, error="No se encontraron cursos para este usuario"), 404

    cursos_conectados = [cu.codigo for cu in conexiones]

    cursos = Curso.query.filter(Curso.codigo.in_(cursos_conectados)).all()

    return jsonify([
        {"codigo": c.codigo, "nombre": c.nombre}
        for c in cursos
    ])

@apis.route("/api/cursos", methods=["POST"])
def add_curso():
    data = request.get_json()
    nombre = data.get("nombre")
    if not nombre:
        return jsonify(success=False, error="Falta el nombre del curso"), 400

    codigo = generar_codigo()
    while Curso.query.filter_by(codigo=codigo).first():
        codigo = generar_codigo()

    nuevo_curso = Curso(nombre=nombre, codigo=codigo)
    db.session.add(nuevo_curso)
    db.session.commit()

    nuevo_conexion = CursoUsuario(codigo=nuevo_curso.codigo, email=current_user.email)
    db.session.add(nuevo_conexion)
    db.session.commit()

    return jsonify(success=True, curso={
        "nombre": nuevo_curso.nombre,
        "codigo": nuevo_curso.codigo
    })
    
@apis.route("/api/unirse", methods=["POST"])
def unirse_curso():
    if not current_user.is_authenticated:
        return jsonify(success=False, error="Debes iniciar sesión"), 401
    if current_user.rango != "Alumno":
        return jsonify(success=False, error="Solo los alumnos pueden unirse"), 403

    data = request.get_json()
    codigo = data.get("codigo")
    if not codigo:
        return jsonify(success=False, error="Falta el código"), 400

    curso = Curso.query.filter_by(codigo=codigo).first()
    if not curso:
        return jsonify(success=False, error="Código inválido"), 404

    if CursoUsuario.query.filter_by(codigo=curso.codigo, email=current_user.email).first():
        return jsonify(success=False, error="Ya estás en este curso"), 400

    conexion = CursoUsuario(codigo=curso.codigo, email=current_user.email)
    db.session.add(conexion)
    db.session.commit()

    return jsonify(success=True, mensaje="Te uniste al curso", curso={"codigo": curso.codigo, "nombre": curso.nombre})

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




@apis.route("/api/posts", methods=["POST"])
def add_post():
    codigo = request.form.get("codigo")
    contenido = request.form.get("contenido")
    autor = request.form.get("autor")
    archivo = request.files.get("archivo")

    nuevo_post = Post(
        codigo=codigo,
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

@apis.route("/api/posts", methods=["GET"])
def get_posts():
    posts = Post.query.all()
    result = []
    for p in posts:
        result.append({
            "id_post": p.id_post,
            "codigo": p.codigo,
            "contenido": p.contenido,
            "autor": p.autor,
            "fecha_publicacion": p.fecha_publicacion
        })
    return jsonify(result)

@apis.route("/api/posts/<string:codigo>", methods=["PUT"])
def update_post(codigo):
    post = Post.query.get(codigo)
    if not post:
        return jsonify(success=False, error="Post no encontrado"), 404
    data = request.get_json()
    post.contenido = data.get("contenido", post.contenido)
    post.codigo = data.get("codigo", post.codigo)
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



@apis.route("/api/Tarea", methods=["POST"])
@login_required
def add_Tarea():
    if current_user.rango != "Profe":
        return jsonify(success=False, error="Solo los profesores pueden crear tareas"), 403

    data = request.get_json()
    codigo = data.get("codigo")
    titulo = data.get("Titulo")
    contenido = data.get("contenido")
    autor = current_user.email

    if not (codigo and titulo):
        return jsonify(success=False, error="Faltan datos"), 400

    nueva_tarea = Tarea(
        codigo=codigo,
        titulo=titulo,
        contenido=contenido,
        autor=autor
    )
    db.session.add(nueva_tarea)
    db.session.commit()

    return jsonify(success=True, tarea={
        "id_tarea": nueva_tarea.id_tarea,
        "codigo": nueva_tarea.codigo,
        "titulo": nueva_tarea.titulo,
        "contenido": nueva_tarea.contenido,
        "autor": nueva_tarea.autor,
        "fecha_publicacion": nueva_tarea.fecha_publicacion
    })


@apis.route("/api/Tarea", methods=["GET"])
@login_required
def get_Tareas():
    tareas = Tarea.query.all()
    result = []
    for t in tareas:
        result.append({
            "id_tarea": t.id_tarea,
            "codigo": t.codigo,
            "titulo": t.titulo,
            "contenido": t.contenido,
            "autor": t.autor,
            "fecha_publicacion": t.fecha_publicacion
        })
    return jsonify(result)


@apis.route("/api/Tarea/<int:id>", methods=["DELETE"])
@login_required
def delete_Tarea(id):
    tarea = Tarea.query.get(id)
    if not tarea:
        return jsonify(success=False, error="Tarea no encontrada"), 404

    if current_user.rango != "Profe":
        return jsonify(success=False, error="No tienes permiso para eliminar tareas"), 403

    db.session.delete(tarea)
    db.session.commit()
    return jsonify(success=True)



@apis.route("/api/entregas", methods=["POST"])
@login_required
def add_entrega():
    id_tarea = request.form.get("id_tarea")
    archivo = request.files.get("archivo")

    if not id_tarea:
        return jsonify(success=False, error="Falta id_tarea"), 400

    # validar que no entregue dos veces
    existente = Entrega.query.filter_by(id_tarea=id_tarea, autor=current_user.email).first()
    if existente:
        return jsonify(success=False, error="Ya has entregado esta tarea"), 400

    nueva = Entrega(
        id_tarea=id_tarea,
        autor=current_user.email
    )
    db.session.add(nueva)
    db.session.commit()

    # guardar archivo si existe
    if archivo:
        data = archivo.read()
        nuevo_archivo = Archivo(
            id_entrega=nueva.id_entrega,
            tipo=archivo.content_type,
            tamano=len(data),
            pixel=data,
            nombre=archivo.filename   # guardar nombre original
        )
        db.session.add(nuevo_archivo)
        db.session.commit()

    return jsonify(success=True, entrega={"id_entrega": nueva.id_entrega})

#Api para que el alumno vea su entrega de una tarea
@apis.route("/api/entregas/<int:id_tarea>", methods=["GET"])
@login_required
def get_entrega_by_tarea(id_tarea):
    entrega = Entrega.query.filter_by(id_tarea=id_tarea, autor=current_user.email).first()
    if not entrega:
        return jsonify(success=False, error="No has entregado nada aún"), 404

    archivos = Archivo.query.filter_by(id_entrega=entrega.id_entrega).all()
    archivos_data = [
        {
            "id_archivo": a.id_archivo,
            "nombre": a.nombre,
            "tipo": a.tipo,
            "tamano": a.tamano,
            "pixel": base64.b64encode(a.pixel).decode("utf-8") if a.pixel else None
        }
        for a in archivos
    ]

    return jsonify(success=True, entrega={
        "id_entrega": entrega.id_entrega,
        "autor": entrega.autor,
        "fecha_entrega": entrega.fecha_entrega,
        "archivos": archivos_data
    })

#Api para que el profe vea todas las entregas de una tarea
@apis.route("/api/entregas/tarea/<int:id_tarea>", methods=["GET"])
@login_required
def get_entregas_by_tarea(id_tarea):
    if current_user.rango != "Profe":
        return jsonify(success=False, error="No autorizado"), 403

    entregas = Entrega.query.filter_by(id_tarea=id_tarea).all()
    result = []
    for e in entregas:
        archivos = Archivo.query.filter_by(id_entrega=e.id_entrega).all()
        archivos_data = [
            {
                "id_archivo": a.id_archivo,
                "nombre": a.nombre,
                "tipo": a.tipo,
                "tamano": a.tamano,
                "pixel": base64.b64encode(a.pixel).decode("utf-8") if a.pixel else None
            }
            for a in archivos
        ]

        result.append({
            "id_entrega": e.id_entrega,
            "autor": e.autor,
            "fecha_entrega": e.fecha_entrega,
            "archivos": archivos_data
        })

    return jsonify(success=True, entregas=result)



@apis.route("/api/entregas/<int:id_entrega>", methods=["DELETE"])
@login_required
def delete_entrega(id_entrega):
    entrega = Entrega.query.get(id_entrega)
    if not entrega:
        return jsonify(success=False, error="Entrega no encontrada"), 404

    if entrega.autor != current_user.email:
        return jsonify(success=False, error="No puedes borrar entregas de otros"), 403

    db.session.delete(entrega)
    db.session.commit()
    return jsonify(success=True, mensaje="Entrega cancelada")


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

@apis.route("/api/archivos_entrega/<int:id_entrega>", methods=["GET"])
@login_required
def get_archivos_entrega(id_entrega):
    archivos = Archivo.query.filter_by(id_entrega=id_entrega).all()
    return jsonify([
        {
            "id_archivo": a.id_archivo,
            "nombre": a.nombre,
            "tipo": a.tipo,
            "tamano": a.tamano,
            "pixel": base64.b64encode(a.pixel).decode("utf-8") if a.pixel else None
        }
        for a in archivos
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
        codigo=data.get("codigo"),
        email=data.get("email")
    )
    db.session.add(nuevo)
    db.session.commit()
    return jsonify(success=True, conexion={
        "id_conexion": nuevo.id_conexion,
        "codigo": nuevo.codigo,
        "email": nuevo.email
    })

@apis.route("/api/cursos_usuarios/<string:codigo>", methods=["GET"])
def get_cursos_usuarios(codigo):
    conexiones = CursoUsuario.query.filter_by(codigo=codigo).all()

    if not conexiones:
        return jsonify(success=False, error="No se encontraron cursos para este usuario"), 404

    cursos = [cu.email for cu in conexiones]
    return jsonify(cursos)

@apis.route("/api/cursos_usuarios/<string:codigo>/<string:email>", methods=["DELETE"])
def delete_cursos_usuarios(codigo,email):
    conexion = CursoUsuario.query.filter_by(codigo=codigo, email=email).first()
    if not conexion:
        return jsonify(success=False, error="conexion no encontrada"), 404
    
    db.session.delete(conexion)
    db.session.commit()
    return jsonify(success=True)