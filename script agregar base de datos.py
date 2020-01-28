pip install djipsum
pip install redis
pip install django-redis

from djipsum.faker import FakerModel
faker = FakerModel(app='table', model='Autor')
##Creando autores ES RAPIDO
for _ in range(5000):
	fields = {
        'nombre': faker.fake.name(),
        'apellidos': faker.fake.word()+" "+faker.fake.word(),
        'email': faker.fake_email(),
    }
    faker.create(fields)

from djipsum.faker import FakerModel
faker = FakerModel(app='table', model='Libro')


##creando libros TARDA MUCHO
for _ in range(5000):
	fields = {
        'titulo': faker.fake.text(max_nb_chars=20),
        'autor': faker.fake_relations(
            type='m2m',
            field_name='autor'
        ),
        'fecha_publicacion': str(faker.fake.date()),
        'portada': 'portadas/'+faker.fake.word(),
    }
    faker.create(fields)
