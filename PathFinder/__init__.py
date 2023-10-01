import os, atexit, datetime, time, shutil, logging

from flask import Flask, render_template,request, make_response
from apscheduler.schedulers.background import BackgroundScheduler

def create_app(test_config=None):
    # create and configure the app
    logging.basicConfig(format="%(asctime)s  %(name)s  %(levelname)s: %(message)s")
    UPLOAD_FOLDER = "./PathFinder/files/"
    app = Flask(__name__, instance_relative_config=True)
    
    # configure upload folder path and file size
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.secret_key = os.getenv("SECRET_KEY")
        
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # create blueprint
    from . import graph
    app.register_blueprint(graph.bp)
    
    # set scheduler to remove old files
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=remove_files, trigger="interval", seconds=600)
    scheduler.start()
    
    # close scheduler 
    atexit.register(lambda: scheduler.shutdown())
    
    @app.route('/', methods=("GET","POST"))
    def index():
        # clear cookies
        if request.method == "POST":
            request.cookies.clear()
        
        # show index.html
        resp = make_response( render_template("index.html"))
        return resp

    return app


def remove_files():
    # check if download folder exists
    if not os.path.exists("./PathFinder/download/"):
        return
    
    # save current time to variable
    current_time = datetime.datetime.now()
    
    # check creation date of files
    for i in os.listdir("./PathFinder/download"):
        file_creation_time = os.path.getctime(f"./PathFinder/download/{i}")
        file_creation_date = time.ctime(file_creation_time)
        file_creation_datetime = datetime.datetime.strptime(file_creation_date,"%a %b %d %H:%M:%S %Y")
        time_delta : datetime.timedelta = current_time-file_creation_datetime
        
        # remove files that are older than 10 min
        if time_delta.seconds >= 600:
            shutil.rmtree(f"./PathFinder/files/{i[:-4]}", ignore_errors=True)
            logging.info(f"Removed folder: {i[:-4]}")
            os.remove(f"./PathFinder/download/{i}")
            logging.info(f"Removed zip file: {i}")