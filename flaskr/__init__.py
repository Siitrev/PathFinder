import os

from flask import Flask, render_template,request, make_response


def create_app(test_config=None):
    # create and configure the app
    UPLOAD_FOLDER = "./flaskr/files/"
    app = Flask(__name__, instance_relative_config=True)
    
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
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
        resp = make_response( render_template("index.html"))
        if request.method == "POST":   
            resp.delete_cookie("edges",samesite=None,secure=True)
        return resp

    return app