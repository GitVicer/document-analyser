from configparser import ConfigParser

def config(filename = 'database.ini', section = 'postgresql'):
    #create parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)
    db={}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(f"{section} is not found in {filename}")        
    return (db)

def database_uri_config(filename = 'database.ini', section = 'database_uri'):
    parser = ConfigParser()
    parser.read(filename)
    if parser.has_section(section):
        items = parser.items(section)
        uri = dict(items).get('uri')
    return uri    