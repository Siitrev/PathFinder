import os

from flask import Flask, render_template,request, make_response


def create_app(test_config=None):
    # create and configure the app
    UPLOAD_FOLDER = "./PathFinder/files/"
    app = Flask(__name__, instance_relative_config=True)
    
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    
    if not os.path.exists(f"{app.config['UPLOAD_FOLDER']}"):
        os.mkdir(f"{app.config['UPLOAD_FOLDER']}")
        
    if not os.path.exists("./PathFinder/download/"):
        os.mkdir("./PathFinder/download/")
        
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    from . import graph
    app.register_blueprint(graph.bp)
    
    
    
    @app.route('/', methods=("GET","POST"))
    def index():
        if request.method == "POST":
            request.cookies.clear()
        resp = make_response( render_template("index.html"))
        return resp

    return app