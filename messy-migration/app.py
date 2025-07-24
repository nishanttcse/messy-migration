from flask import Flask
from app.routes.users import user_routes #Import Blueprint for user-related routes
# Create a Flask application factory


def create_app():
    app = Flask(__name__)
    app.register_blueprint(user_routes)  # Registering routes cleanly via Blueprint
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0', port=5000)


#Created a Flask app factory and moved route registration here
#Modularizes the app instead of defining routes in the root file
# This allows for better organization and scalability of the application
# The app can now be run with `python app.py` and will listen on all interfaces
# at port 5000, making it accessible from other devices on the network.
