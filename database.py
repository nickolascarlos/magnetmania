import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="magnetmania",
    user="postgres",
    password="712893465a"
)

cursor = conn.cursor()

def register_media(nome, ano = -1):
    global cursor

    # Checks if media already exists
    if get_media_id(nome, ano):
        return True
    
    try:
        cursor.execute("INSERT INTO media (nome, ano) VALUES ('%s', %d)" % (nome, ano))
        conn.commit()
        return True
    except:
        return False

def get_media_id(nome, ano = -1):
    global cursor
    try:
        cursor.execute("SELECT * FROM media WHERE nome = '%s' AND ano = %d" % (nome, ano))
        conn.commit()
        return cursor.fetchone()[0]
    except:
        cursor.execute("ROLLBACK")
        return None

def delete_media(media_id):
    global cursor
    try:
        cursor.execute("DELETE FROM media WHERE id = %d"  % (media_id))
        conn.commit()
    except:
        return False

def set_media_metadata(media_id, property, value):
    global cursor
    try:
        cursor.execute("INSERT INTO media_metadata (media_id, property, value) VALUES (%d, '%s', '%s')" % (media_id, property, value))
        conn.commit()
        return True
    except:
        cursor.execute("ROLLBACK")
        return False
    

def get_media_metadata(media_id, property):
    global cursor
    try:
        cursor.execute("SELECT property, value FROM media_metadata WHERE media_id = %d AND property = '%s'" % (media_id, property))
        conn.commit()
        return cursor.fetchone()[1]
    except:
        return None
    

def register_magnet(hash, media_id):
    global cursor

    # Checks if media already exists
    if get_magnet(hash):
        return False # Retorna False para evitar recadastramento de metadados de magnets,
                     # Diferente de Media, que não tem esse problema e, portanto,
                     # retorna True em caso análogo

    try:
        cursor.execute("INSERT INTO magnet (hash, media_id) VALUES ('%s', %d)" % (hash, media_id))
        conn.commit()
        return True
    except:
        cursor.execute("ROLLBACK")
        return False
    
def get_magnet(hash):
    global cursor
    
    try:
        cursor.execute("SELECT * FROM magnet WHERE hash = '%s'" % (hash))
        conn.commit()
        return cursor.fetchone()
    except:
        return None
    
def set_magnet_metadata(hash, property, value):
    global cursor
    try:
        cursor.execute("INSERT INTO magnet_metadata (magnet_id, property, value) VALUES ('%s', '%s', '%s')" % (hash, property, value))
        conn.commit()
        return True
    except:
        cursor.execute("ROLLBACK")
        return False