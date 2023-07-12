import os

from flask import Flask, render_template,session


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev"
    )
    
    if test_config is None:
        app.config.from_pyfile("config.py",silent=True)
    else:
        app.config.from_mapping(test_config)
        
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    from . import graph
    app.register_blueprint(graph.bp)
    
    
    @app.route('/', methods=("GET","POST"))
    def index():
        for key in list(session.keys()):
            session.pop(key)
        return render_template("index.html")

    return app