from app import app, db  
from app import User  
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

with app.app_context():
    users = User.query.all()
    for user in users:
        if not user.password.startswith('$2b$'): 
            user.password = bcrypt.generate_password_hash(user.password).decode('utf-8')
            print(f"Rehashed password for user: {user.email}")

    db.session.commit()
    print("All passwords rehashed successfully!")
