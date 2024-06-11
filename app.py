#from flask import Flask, render_template, request
#from models.db import db, instance
from controllers.app_controller import create_app
from utils.create_db import create_db

if __name__ == "__main__":
    app = create_app()
    create_db(app)
    app.run(host='0.0.0.0', port=8080, debug=True) #trocar para false