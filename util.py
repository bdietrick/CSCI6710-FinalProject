import os

def get_uploads_path():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    image_path = os.path.join(base_dir, 'static/images/')
    return image_path

def get_db_uri():
    # sysname = os.uname().sysname
    sysname = os.name

    base_dir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(base_dir, 'data2.sqlite')

    if sysname == 'windows' or sysname == 'nt':
        db_uri = 'sqlite:///' + db_path
    elif sysname == 'linux':
        db_uri = 'sqlite:////' + db_path
    elif sysname == 'darwin':
        db_uri = 'sqlite:////' + db_path
    else:
        db_uri = 'sqlite:///' + db_path

    db_uri = 'sqlite:///GardenExchange.db'
    return db_uri


