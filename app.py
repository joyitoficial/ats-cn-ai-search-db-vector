from src.services.search_vector import CandidateSearchService
from src.infrastructure.adapters.db_connection_adapter import PostgresDBAdapter
from flask_cors import CORS

from flask import Flask, request, jsonify
app = Flask(__name__)

CORS(app)
db_connection = PostgresDBAdapter()
candidate_search_service = CandidateSearchService(db_connection)

@app.route('/searchdb/entities', methods=['POST'])
def search_entities():
    # Recibir los datos JSON
    print("Buscando...")
    data = request.get_json()
    role = data["entities"]["role"]
    capabilities = data["entities"]["capabilities"]

    # Llamar a la función de búsqueda con el término combinado
    aplicantes_filtrados = candidate_search_service.buscar_candidatos(role, capabilities)

    return jsonify(aplicantes_filtrados)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
