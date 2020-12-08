### Descargar Proyecto

    cd ~/Documentos/github
    git clone git@github.com:oortega/dtable_project.git

### Crear Entorno

    cd ~/Documentos/github/dtable_project
    pipenv shell

### Instalamos Dependencias

    pipenv install

### Crear Base de datos
    
    CREATE DATABASE dtable;

### Crear Usuario:

    GRANT ALL PRIVILEGES ON dtable.* TO 'dtable_user'@'localhost' IDENTIFIED BY 'dtable_pass' WITH GRANT OPTION;
    FLUSH PRIVILEGES;

### Migraciones

    cd ~/Documentos/github/dtable_project/dtable
    ./manage.py migrate

### Cargar Json a la base de Datos
    
    cd ~/Documentos/github/dtable_project/dtable
    ./manage.py loaddata db.json

