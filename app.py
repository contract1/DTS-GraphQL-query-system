from flask import Flask, render_template, request
import requests
import json

app = Flask(__name__)

# URL do endpoint GraphQL do Substreams Uniswap v3 Ethereum
subgraph_endpoint = "https://api.thegraph.com/subgraphs/name/subgraphs/uniswap-v3"

# Consulta GraphQL
subgraph_gql_query = """
{
  swaps(orderBy: amountInUSD, orderDirection: desc, first: 10) {
    amountInUSD
    from
    to
    timestamp
    tokenIn {
      name
    }
    tokenOut {
      name
    }
  }
}
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Enviar consulta GraphQL para o endpoint do subgráfico
        response = requests.post(subgraph_endpoint, json={"query": subgraph_gql_query})
        
        # Verificar se a solicitação foi bem-sucedida
        if response.status_code == 200:
            data = response.json()
            # Processar os dados conforme necessário
            swaps = data.get("data", {}).get("swaps", [])
            return render_template('index.html', swaps=swaps)
        else:
            # Lidar com erros de solicitação
            return "Erro ao acessar o endpoint do subgráfico."
    else:
        return render_template('index.html') 

if __name__ == '__main__':
    app.run(debug=True)
