import jwt
from flask import request, jsonify
from werkzeug.security import generate_password_hash
from app import app, db
from app.models import User, Role, Project, GradeRound1, GradeRound2
from app.middlewares import token_required


@app.route('/auth', methods=['POST'])
def user_login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify('User not found'), 404

    if user.check_password(generate_password_hash(password)):
        return jsonify('Wrong password'), 400

    token = jwt.encode({'id' : user.id}, app.config['SECRET_KEY'])

    return jsonify(token)


@app.route('/round1_top5', methods=['POST'])
@token_required
def top5(decoded):
    user = User.query.filter_by(id=decoded['id']).first()

    if not user:
        return jsonify('User\'s not found'), 404

    judges = db.session.query(User, Role).filter(Role.name=='Judge').join(User, User.role_id==Role.id).all()

    top5_round1 = db.session.execute(f"""
    select project.id as project_id, 
        project.name, 
        project.slide, 
        project.github, 
        project.youtube, 
        sum(graderound1.total) as total
    from project
    join graderound1 on graderound1.project_id = project.id
    join users on graderound1.mentor_id = users.id
    group by project.id
    order by total desc
    limit 5;
    """)

    for team in top5_round1:
        for judge in judges:
            g = GradeRound2(judge_id=judge[0].id, project_id=team.project_id)
            db.session.add(g)
            db.session.commit()

    return jsonify('Top 5 has been added to Round 2!'), 201

