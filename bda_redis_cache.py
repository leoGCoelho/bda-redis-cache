from default_func import *
from flask import Flask
from redis import Redis

app = Flask(__name__)

@app.route('/')
def status():
    return {'success': True}


@app.route('/carros')
def carros():
    return lista_carros()

@app.route('/carros_cache')
def carrosCache():
    r = Redis(host='redis', port=6379)

    data = r.get('listacarros')
    if data is None:
        r.set('listacarros', str(lista_carros()), ex=3600)
        data = r.get('listacarros')

    return data.decode('utf-8')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
