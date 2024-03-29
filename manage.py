from app import app, db
from app.models import User, Project, Role, GradeRound1, GradeRound2

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db, 
        'User': User,
        'Role': Role,
        'Project': Project,
        'GradeRound1': GradeRound1,
        'GradeRound2': GradeRound2
    }