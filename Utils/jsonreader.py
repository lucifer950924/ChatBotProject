import os, json, pathlib

def readconifgJson(filename):
    cwd = os.getcwd()
    jsonPath = pathlib.Path(os.path.join(cwd,
                            'config'))
    
    filepath = (str(fp) for fp in list(jsonPath.iterdir()) if fp.is_file() and fp.name == filename and fp.suffix == '.json').__next__()

    with open(filepath,'r',encoding = 'utf-8') as file:
        return json.load(file)

        