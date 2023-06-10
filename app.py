import json
from flask import request, jsonify
from flask import Flask, render_template

import os
from langchain import PromptTemplate, LLMChain
from langchain.chat_models import ChatOpenAI


TEMPLATE = """  Você vai agir como um psicólogo que observa textos de alunos e consegue extrair informações sobre o sentimento do aluno, o
                real sentimento dele quando estava escrevendo o texto.
                As características que você irá relatar no texto são [com/sem violência], [com/sem bullying], [nível de risco baixo/médio/alto].
                Suas respostas devem sempre separar as características por virgula, jamais misture duas características sem a separação delas
                por vírgula. Lembre-se de sempre verificar minuciosamente para analisar corretamente o texto escrito pelo aluno.
                
                Comece!

                Texto: "hoje nao teve nada demais"
                Psicólogo: sem violência, sem bullying, baixo

                Texto: "hoje eu sofri bullying, fizeram muitas piadas sobre mim"
                Psicólogo: com violência, com bullying, médio

                Texto: {student_text}
                Psicólogo: 
 """

def initiate_openai(key):
    os.environ['OPENAI_API_KEY'] = key

def get_llm():
  return ChatOpenAI(temperature=0, model_name='gpt-3.5-turbo')

prompt = PromptTemplate(
    template=TEMPLATE,
    input_variables=['student_text']
)

def get_llm_chain(prompt, llm):
  return LLMChain(prompt=prompt,
                  llm=llm)

def classify_text(student_text, llm_chain):
    return llm_chain.run(student_text)
  
def extract_infos(text):
  violencia, bullying, risco = infos.split(',')
  violencia = violencia.strip()
  bullying = bullying.strip()
  risco = risco.strip()
  return violencia, bullying, risco

app = Flask(__name__)


@app.route('/api', methods=['POST'])
def get_api_response():
    data = json.loads(request.data)
    text = data.get("texto",None)
    api_key = data.get("api_key", None)

    if text is None:
      return jsonify({"message":"text not found"})
    
    if api_key is None:
      return jsonify({"api_key":"api not found"})
    
    try:
      initiate_openai(api_key)
    except:
      return jsonify({"api_key":"openai key not valid"})
    
    infos = classify_text(text)
    violencia, bullying, risco = extract_infos(infos)
    data['violencia'] = violencia
    data['bullying'] = bullying
    data['risco'] = risco
    return jsonify(data)

if __name__ == "__main__":
    app.run()
