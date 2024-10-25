import os
from flask import Flask, render_template, request, jsonify
from groq import Groq
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from fpdf import FPDF

# Carregar variáveis de ambiente do .env
load_dotenv()
API_KEY = os.getenv('API_KEY')

# Inicializando o cliente Groq
client = Groq(api_key=API_KEY)

# Configurando o template da conversa
template = """Você é um assistente virtual.
Responda apenas em Português.

Input: {input}
"""

# Criando o PromptTemplate
base_prompt = PromptTemplate(input_variable="input", template=template)

# Configurando a memória de conversação
memory = ConversationBufferMemory(memory_key="chat_history", input_key='input')

app = Flask(__name__)

def categorize_problem(problem):
    # Função para usar a API do Groq para categorizar o problema
    messages = [
        {"role": "user", "content": f"Categorize o problema '{problem}' usando o Diagrama de Ishikawa."}
    ]
    response = client.chat.completions.create(
        messages=messages,
        model="gemma2-9b-it"
    )
    return response.choices[0].message.content

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/categorize', methods=['POST'])
def categorize():
    data = request.get_json()
    problem = data['problem']
    causes = categorize_problem(problem)
    return jsonify({'causes': causes})

@app.route('/generate_pdf', methods=['POST'])
def generate_pdf():
    data = request.get_json()
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Relatório de Problema", ln=True, align='C')
    
    # Adicionar problema e causas no PDF
    pdf.multi_cell(0, 10, txt=f"Problema: {data['problem']}")
    pdf.multi_cell(0, 10, txt=f"Causas: {data['causes']}")
    
    # Salvar PDF
    pdf_output = "relatorio.pdf"
    pdf.output(pdf_output)
    
    return jsonify({'pdf': pdf_output})

if __name__ == "__main__":
    app.run(debug=True)
