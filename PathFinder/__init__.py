import os, atexit, datetime, time, shutil, logging

from flask import Flask, render_template,request, make_response
from apscheduler.schedulers.background import BackgroundScheduler

def create_app(test_config=None):
    # create and configure the app
    
    logging.basicConfig(format="%(asctime)s  %(name)s  %(levelname)s: %(message)s")
    UPLOAD_FOLDER = "./PathFinder/files/"
    app = Flask(__name__, instance_relative_config=True)
    
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
        
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    from . import graph
    app.register_blueprint(graph.bp)
    
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=print_date_time, trigger="interval", seconds=10)
    scheduler.start()
    
    atexit.register(lambda: scheduler.shutdown())
    
    @app.route('/', methods=("GET","POST"))
    def index():
        if request.method == "POST":
            request.cookies.clear()
        resp = make_response( render_template("index.html"))
        return resp

    return app


def print_date_time():
    current_time = datetime.datetime.now()
    for i in os.listdir("./PathFinder/download"):
        file_creation_time = os.path.getctime(f"./PathFinder/download/{i}")
        file_creation_date = time.ctime(file_creation_time)
        file_creation_datetime = datetime.datetime.strptime(file_creation_date,"%a %b %d %H:%M:%S %Y")
        time_delta : datetime.timedelta = current_time-file_creation_datetime
        if time_delta.seconds >= 0:
            shutil.rmtree(f"./PathFinder/files/{i[:-4]}", ignore_errors=True)
            logging.info(f"Removed folder: {i[:-4]}")
            os.remove(f"./PathFinder/download/{i}")
            logging.info(f"Removed zip file: {i}")