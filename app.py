from flask import Flask,jsonify,request
from sqlalchemy.exc import SQLAlchemyError
from db import db 
from models import Student

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.db"

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/api/student/create", methods=["POST"])
def create_student():
    data = request.get_json()
    name = data.get("name")
    if not name:
        return jsonify({"status": 400, "message": "Name is required"}), 400
    new_student = Student(name=name)
    try:
        db.session.add(new_student)
        db.session.commit()
        return jsonify({
            "id": new_student.id,
            "name": new_student.name,
            "created_at": new_student.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"status": 500, "message": str(e)}), 500

@app.route("/api/student/get", methods=["GET"])
def get_student():
    try:
        student_id = request.args.get("id")
        name = request.args.get("name")

        if student_id:
            student = Student.query.get_or_404(student_id)
            return jsonify({
                "id": student.id,
                "name": student.name,
                "created_at": student.created_at.strftime("%Y-%m-%d %H:%M:%S")
            }), 200

        elif name:
            students = Student.query.filter_by(name=name).all()
            results = [{
                "id": s.id,
                "name": s.name,
                "created_at": s.created_at.strftime("%Y-%m-%d %H:%M:%S")
            } for s in students]
            return jsonify(results), 200

        else:
            students = Student.query.all()
            results = [{
                "id": s.id,
                "name": s.name,
                "created_at": s.created_at.strftime("%Y-%m-%d %H:%M:%S")
            } for s in students]
            return jsonify(results), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"status": 500, "message": str(e)}), 500


@app.route("/api/student/update",methods=["POST"])
def update_student():
    try:
        data = request.get_json()
        student_id = data.get("id")
        student_name = data.get("name")

        if not student_id or not student_name:
            return jsonify({"status": 400, "message": "id and name are required"}), 400

        student = Student.query.get_or_404(student_id)
        student.name = student_name
        db.session.commit()

        return jsonify({
            "id": student.id,
            "name": student.name,
            "created_at": student.created_at
        })
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"status": 500, "message": str(e)}), 500
    
@app.route("/api/student/delete",methods=["GET"])
def delete_student():
    try:
        student_id = request.args.get("id")
        student = Student.query.get_or_404(student_id)
        db.session.delete(student)
        db.session.commit()
        return jsonify({"status":200,"massege":"Delted Successfully"}),200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"status":500,"massege":str(e)}),500    




if __name__ == "__main__":
    app.run(debug=True)