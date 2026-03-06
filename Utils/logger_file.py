import os,logging, pathlib, datetime, time

def setUpLogger():
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%S%f")
    
    export_dir = os.path.join(os.getcwd(),'Report',f'{timestamp}')

    if not os.path.exists(export_dir):
        os.makedirs(export_dir,exist_ok=True)

    logging.basicConfig(filename=os.path.join(export_dir,f'Report_{timestamp}.log'),
                        level= logging.INFO,
                        format = '%(asctime)s - %(levelname)s - %(message)s')
    
    logger = logging.getLogger()

    logger.setLevel(logging.INFO)

    return logger

