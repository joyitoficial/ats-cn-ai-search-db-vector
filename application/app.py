import sys
from os.path import dirname, abspath
from .search_vector import buscar_candidatos_postgre

sys.path.append(dirname(dirname(abspath(__file__))))

from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/searchdb/entities', methods=['POST'])
def search_entities():
    # Recibir los datos JSON
    print("Buscando...")
    data = request.get_json()
    role = data["entities"]["role"]
    capabilities = data["entities"]["capabilities"]

    # Llamar a la función de búsqueda con el término combinado
    aplicantes_filtrados = buscar_candidatos_postgre(role, capabilities)

    return jsonify(aplicantes_filtrados)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
