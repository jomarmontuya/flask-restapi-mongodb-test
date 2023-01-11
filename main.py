from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId



app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/admin"
mongo = PyMongo(app)

# Create a new user
@app.route("/user", methods=["POST"])
def create_user():
    try:
        data = request.get_json()
        mongo.db.users.insert_one(data)
        return jsonify({"message": "user created successfully"})
    except Exception as e:
        # Handle any errors that might occur when inserting the new user
        return jsonify({"error": f"Error creating new user: {e}"}), 400

# Get all users
@app.route("/user", methods=["GET"])
def get_all_users():
    try:
        users = list(mongo.db.users.find())
        for user in users:
            user['_id'] = str(user['_id'])
        return jsonify(users)
    except Exception as e:
        return jsonify({"error": f"Error retrieving users: {e}"}), 500

# Get a single user
@app.route("/user/<id>", methods=["GET"])
def get_user(id):
    try:
        user = mongo.db.users.find_one({"_id": ObjectId(id)})
        if user:
            user['_id'] = str(user['_id'])
            return jsonify(user)
        else:
            return jsonify({"error": "User not found"}), 404
    except  Exception as e:
        return jsonify({"error": f"Error retrieving user: {e}"}), 500

# Update a user
@app.route("/user/<id>", methods=["PUT"])
def update_user(id):
    try:
        data = request.get_json()
        mongo.db.users.update_one({"_id": ObjectId(id)}, {"$set": data})
        return jsonify({"message": "user updated successfully"})
    except Exception as e:
        return jsonify({"error": f"Error updating user: {e}"}), 500

# Delete a user
@app.route("/user/<id>", methods=["DELETE"])
def delete_user(id):
    try:
        mongo.db.users.delete_one({"_id": ObjectId(id)})
        return jsonify({"message": "user deleted successfully"})
    except Exception as e:
        return jsonify({"error": f"Error deleting user: {e}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
