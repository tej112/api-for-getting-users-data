from flask import Flask,jsonify,request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

"""
    Usage Run main.py file.
"""
#Below line of code is used to connect to postgreSQL: Server
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:2505@localhost/flasksql'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "Your-Secret-Key-Here"
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    age = db.Column(db.Integer,nullable=False)
    city = db.Column(db.String(30), nullable=False)

@app.route("/",methods=['GET','POST',"PUT","DELETE"])
def get_user_byID():
    
    """Token is Provided Through Header

    Returns:
        Json : Response
    """
    # Check if Access token is provided or not
    if not request.headers['x-access-tokens']:
        return jsonify(status="No X-Acess-Token Provided.")
    
    #if Access Token is provided it check with app.secret_key
    if app.secret_key == request.headers['x-access-tokens']:
        
        # TO retrieve User Data such as name,age,city
        if request.method == "GET":
            num = request.args.get("id")

            user = db.session.query(User).filter_by(id=num).first()
            if not user:
                return jsonify(data="User not found")
            else:
                # print(user)
                return jsonify(
                    id=user.id,
                    name=user.name,
                    age=user.age,
                    city=user.city
                    )
        
        #TO ADD New User to the Database and if any information is missing that data will be blank
        if request.method == "POST":
            name = request.args.get("name") if  (request.args.get("name")) else ""
            age = request.args.get("age") if  request.args.get("age") else ""
            city = request.args.get("city") if request.args.get("city") else ""
            
            new_user = User(name=name,age=age,city=city)

            db.session.add(new_user)
            db.session.commit()
            
            return jsonify(
                status="User added successfully"
            )
        
        #To Update user data with given ID 
        if request.method == "PUT":
            id = request.args.get("id")
            user = db.session.query(User).filter_by(id=id).first()
            if user:
                # print(user.name,user.age,user.city)
                name = request.args.get("name") if  (request.args.get("name")) else user.name
                age = request.args.get("age") if  request.args.get("age") else user.age
                city = request.args.get("city") if request.args.get("city") else user.city

                user.name = name
                user.age = age
                user.city = city
                db.session.commit()
                return jsonify(
                    status="Sucessfully updated details",
                    name=user.name,
                    age=user.age,
                    city = user.city
                )
            else:
                return jsonify(
                    status=f"No user with ID:{id} found"
                )
        
        #TO DELETE an User With given ID Number
        if request.method == "DELETE":
            id = request.args.get("id")
            user = db.session.query(User).get(id)
            if user:
                db.session.delete(user)
                db.session.commit()
                return jsonify(
                    status=f"Permanantly Deleted user with ID: {id} and name: {user.name}."
                )
            else:
                return jsonify(
                    status= f"No User found with ID: {id}"
                )

    else:
        #if Token is Not valid returs this
        return jsonify(
            result="InValid X-Access-Token"
        )

if __name__ == '__main__':
    db.create_all()
    db.session.commit()
    app.run(debug=False)
