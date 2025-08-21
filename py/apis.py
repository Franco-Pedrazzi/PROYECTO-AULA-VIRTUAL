from flask import Flask,Blueprint, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from py.db import db

apis = Blueprint('apis', __name__,template_folder='templates')

    
class Jugador(db.Model):
    __tablename__ = 'Jugador'
    id = db.Column(db.Integer, primary_key=True)
    Nombre = db.Column(db.String(100))
    id_equipo = db.Column(db.Integer)
    DNI = db.Column(db.String(20))
    Telefono = db.Column(db.String(20))
    Email = db.Column(db.String(100))
    Fecha_nacimiento = db.Column(db.String(100))
    Comida_Especial = db.Column(db.String(100))

class Equipo(db.Model):
    __tablename__ = 'Equipo'
    id_equipo = db.Column(db.Integer, primary_key=True)
    Colegio = db.Column(db.String(50))
    Deporte = db.Column(db.String(10))
    Sexo = db.Column(db.String(10))
    Categoria = db.Column(db.String(10))

class Partido(db.Model):
    __tablename__ = 'Partido'
    id_partido = db.Column(db.Integer, primary_key=True)
    Deporte = db.Column(db.String(1))
    Categoria = db.Column(db.String(10))
    Sexo = db.Column(db.String(1))
    Arbitro = db.Column(db.Integer)
    Planillero = db.Column(db.Integer)
    Equipo_1 = db.Column(db.Integer)
    Equipo_2 = db.Column(db.Integer)
    Fase = db.Column(db.String(25))
    Horario_inicio = db.Column(db.String(8))
    Horario_final = db.Column(db.String(8))

class Staff(db.Model):
    __tablename__ = 'Staff'
    id_staff = db.Column(db.Integer, primary_key=True)
    Nombre = db.Column(db.String(40))
    DNI = db.Column(db.Integer)
    Telefono = db.Column(db.Integer)
    Email = db.Column(db.String(40))
    Trabajo = db.Column(db.String(15))
    Sector = db.Column(db.String(20))



class Responsable(db.Model):
    __tablename__ = 'Responsable'
    
    id_profesor = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_equipo = db.Column(db.Integer, db.ForeignKey('Equipo.id_equipo'), nullable=True)
    Nombre = db.Column(db.String(50), default='-')
    DNI = db.Column(db.String(10), nullable=True)
    Telefono = db.Column(db.String(15), nullable=True)
    Email = db.Column(db.String(40), nullable=True)
    Comida_especial = db.Column(db.String(3), default='N')
    Fecha_nacimiento = db.Column(db.Date, nullable=True)


@apis.route('/api/Staff', methods=['POST'])
def add_Staff():
    try:
        data = request.get_json()
        Nombre = data.get('Nombre')
        DNI = data.get('DNI')
        Telefono = data.get('Telefono')
        Email = data.get('Email')
        Trabajo = data.get('Trabajo')
        Sector = data.get('Sector')

        if not (Nombre and DNI and Telefono and Email and Trabajo and Sector):
            return jsonify({'success': False, 'error': 'Faltan campos requeridos'}), 400

        new_staff = Staff(
            Nombre=Nombre,
            DNI=DNI,
            Telefono=Telefono,
            Email=Email,
            Trabajo=Trabajo,
            Sector=Sector
        )

        db.session.add(new_staff)
        db.session.commit()

        return jsonify({
            'success': True,
            'Staff': {
                'id_staff': new_staff.id_staff,
                'Nombre': new_staff.Nombre,
                'DNI': new_staff.DNI,
                'Telefono': new_staff.Telefono,
                'Email': new_staff.Email,
                'Trabajo': new_staff.Trabajo,
                'Sector': new_staff.Sector
            }
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@apis.route('/api/Equipo', methods=['POST'])
def add_Equipo():
    try:
        data = request.get_json()
        Colegio = data.get('Colegio')
        Deporte = data.get('Deporte')
        Sexo = data.get('Sexo')
        Categoria = data.get('Categoria')

        if not (Colegio and Deporte and Sexo and Categoria):
            return jsonify({'success': False, 'error': (Colegio , Deporte , Sexo , Categoria)}), 400

        new_Equipo = Equipo(
            Colegio=Colegio,
            Deporte=Deporte,
            Sexo=Sexo,
            Categoria=Categoria
        )

        db.session.add(new_Equipo)
        db.session.commit()

        return jsonify({
            'success': True,
            'Equipo': {
                'id_equipo': new_Equipo.id_equipo,
                'Colegio': new_Equipo.Colegio,
                'Deporte': new_Equipo.Deporte,
                'Sexo': new_Equipo.Sexo,
                'Categoria': new_Equipo.Categoria
            }
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@apis.route('/api/Equipo', methods=['GET'])
def get_Equipos():
    try:
        new_Equipo = Equipo.query.all()
        result = []
        for j in new_Equipo:
            result.apisend({
                'id_equipo': Equipo.id_equipo,
                'Colegio':Equipo.Colegio,
                'Deporte':Equipo.Deporte,
                'Sexo':Equipo.Sexo,
                'Categoria':Equipo.Categoria
            })
        return jsonify({'success': True, 'Equipo': result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@apis.route('/api/Players', methods=['POST'])
def add_Player():
    try:
        data = request.get_json()
        Nombre = data.get('Nombre')
        Fecha_nacimiento = data.get('Fecha_nacimiento')
        DNI = data.get('DNI')
        id_equipo = data.get('id_equipo')
        Telefono = data.get('Telefono')
        Email = data.get('Email')
        Comida_especial = data.get('Comida_especial')

        if not (Nombre and Fecha_nacimiento and DNI and id_equipo and Telefono and Email and Comida_especial):
            return jsonify({'success': False, 'error': (Nombre , Fecha_nacimiento , DNI , id_equipo , Telefono , Email , Comida_especial)}), 400

        new_Jugador = Jugador(
            Nombre=Nombre,
            Fecha_nacimiento=Fecha_nacimiento,
            DNI=DNI,
            id_equipo=id_equipo,
            Telefono=Telefono,
            Email=Email,
            Comida_Especial=Comida_especial
        )

        db.session.add(new_Jugador)
        db.session.commit()

        return jsonify({
            'success': True,
            'Jugador': {
                'id': Jugador.id,
                'Nombre': Jugador.Nombre,
                'id_equipo': Jugador.id_equipo,
                'DNI': Jugador.DNI,
                'Telefono': Jugador.Telefono,
                'Email': Jugador.Email,
                'Fecha_nacimiento': Jugador.Fecha_nacimiento,
                'Comida_Especial': Jugador.Comida_Especial
                
            }
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@apis.route('/api/Players', methods=['GET'])
def get_Jugadores():
    try:
        nuevo_Jugador = Jugador.query.all()
        result = []
        for j in nuevo_Jugador:
            result.apisend({
                'id': j.id,
                'Nombre': j.Nombre,
                'Fecha_nacimiento': j.Fecha_nacimiento,
                'DNI': j.DNI,
                'id_equipo': j.id_equipo,
                'Telefono': j.Telefono,
                'Email': j.Email,
                'Comida_Especial': j.Comida_Especial
            })
        return jsonify({'success': True, 'Jugador': result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
    
@apis.route('/api/Matches', methods=['POST'])
def add_Matches():
    try:
        data = request.get_json()
        Deporte = data.get('Deporte')
        Categoria = data.get('Categoria')
        Sexo = data.get('Sexo')
        Equipo_1 = data.get('Equipo_1')
        Equipo_2 = data.get('Equipo_2')
        Arbitro = data.get('Arbitro')
        Planillero = data.get('Planillero')
        Horario_inicio = data.get('Horario_inicio')
        Horario_final = data.get('Horario_final')

        if not (Deporte and Sexo and Equipo_1 and Equipo_2 and Arbitro and Planillero and Horario_inicio and Horario_final):
            return jsonify({'success': False, 'error': (Deporte , Categoria , Sexo , Equipo_1 , Equipo_2 , Arbitro , Planillero , Horario_inicio , Horario_final)}), 400
        
        new_Partido = Partido(
            Deporte=Deporte,
            Categoria=Categoria,
            Sexo=Sexo,
            Equipo_1=Equipo_1,
            Equipo_2=Equipo_2,
            Arbitro=Arbitro,
            Planillero=Planillero,
            Horario_inicio=Horario_inicio,
            Horario_final=Horario_final
        )

        db.session.add(new_Partido)
        db.session.commit()

        return jsonify({
            'success': True,
            'Partido': {
                'Deporte': Partido.Deporte,
                'Categoria': Partido.Categoria,
                'Sexo': Partido.Sexo,
                'Equipo_1': Partido.Equipo_1,
                'Equipo_2': Partido.Equipo_2,
                'Arbitro': Partido.Arbitro,
                'Planillero': Partido.Planillero,
                'Horario_inicio': Partido.Horario_inicio,
                'Horario_final': Partido.Horario_final
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@apis.route('/api/Matches')
def get_matches():
    try:
        partidos = Partido.query.all()
        lista = []

        for partido in partidos:

            lista.apisend({
                "Fase": partido.Fase,
                "Arbitro": partido.Arbitro,
                "Planillero": partido.Planillero,
                "Equipo_1": partido.Equipo_1,
                "Equipo_2": partido.Equipo_2,
            })

        return jsonify(success=True, Matches=lista)

    except Exception as e:
        return jsonify(success=False, error=str(e)), 500

@apis.route('/api/responsable', methods=['POST'])
def agregar_responsable():
    try:
        data = request.get_json()

        id_equipo = data.get('id_equipo') 
        Nombre = data.get('Nombre', '-')
        DNI = data.get('DNI')
        Telefono = data.get('Telefono')
        Email = data.get('Email')
        Comida_especial = data.get('Comida_especial', 'N')
        Fecha_nacimiento = data.get('Fecha_nacimiento') 

        fecha_obj = None
        if Fecha_nacimiento:
            from datetime import datetime
            try:
                fecha_obj = datetime.strptime(Fecha_nacimiento, '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'success': False, 'error': 'Formato de fecha inválido, debe ser YYYY-MM-DD'}), 400

        nuevo_responsable = Responsable(
            id_equipo=id_equipo,
            Nombre=Nombre,
            DNI=DNI,
            Telefono=Telefono,
            Email=Email,
            Comida_especial=Comida_especial,
            Fecha_nacimiento=fecha_obj
        )

        db.session.add(nuevo_responsable)
        db.session.commit()

        return jsonify({
            'success': True,
            'Responsable': {
                'id_profesor': nuevo_responsable.id_profesor,
                'Nombre': nuevo_responsable.Nombre,
                'DNI': nuevo_responsable.DNI,
                'Telefono': nuevo_responsable.Telefono,
                'Email': nuevo_responsable.Email,
                'Comida_especial': nuevo_responsable.Comida_especial,
                'Fecha_nacimiento': str(nuevo_responsable.Fecha_nacimiento),
                'id_equipo': nuevo_responsable.id_equipo
            }
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@apis.route('/api/Equipos', methods=['GET'])
def get_equipos():
    equipos = Equipo.query.all()
    return jsonify([
        {
            'id': equipo.id_equipo,
            'colegio': equipo.Colegio,
            'deporte': equipo.Deporte,
            'sexo': equipo.Sexo,
            'categoria': equipo.Categoria
        }
        for equipo in equipos
    ])

@apis.route('/api/Equipo/<int:id>', methods=['PUT'])
def update_equipo(id):
    equipo = Equipo.query.get(id)
    if not equipo:
        return jsonify({'success': False, 'error': 'Equipo no encontrado'}), 404
    data = request.get_json()
    try:
        equipo.Colegio = data['Colegio']
        equipo.Deporte = data['Deporte']
        equipo.Sexo = data['Sexo']
        equipo.Categoria = data['Categoria']
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@apis.route('/api/Equipo/<int:id>', methods=['DELETE'])
def delete_equipo(id):
    equipo = Equipo.query.get(id)
    if not equipo:
        return jsonify({'success': False, 'error': 'Equipo no encontrado'}), 404
    try:
        db.session.delete(equipo)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400
