from datetime import datetime
import os, pathlib, logging , subprocess

def setUpLogger():
    cwd = os.getcwd()
    timestamp = datetime.now().strftime('%Y%m%d%H%S')
    exportdir = os.path.join(cwd,'Exports',f'{timestamp}')
    os.makedirs(exportdir,exist_ok=True)
    try:
        reportfp = os.path.join(exportdir,'report.log')
        
        logging.basicConfig(filename= reportfp,
                            level = logging.INFO,
                            format = '%(asctime)s - %(levelname)s - %(message)s')
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        
        return logger,reportfp
    except OSError:
        print('Make Export directory and run')
    
    