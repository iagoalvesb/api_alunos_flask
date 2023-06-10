import json
from flask import request, jsonify
from flask import Flask, render_template

import os
from langchain import PromptTemplate, LLMChain
from langchain.chat_models import ChatOpenAI

def initiate_openai(key):
    os.environ['OPENAI_API_KEY'] = key
    
TEMPLATE = """  Você vai agir como um psicólogo que observa textos de alunos e consegue extrair informações sobre o sentimento do aluno, o
                real sentimento dele quando estava escrevendo o texto.
                As características que você irá relatar no texto são [com/sem violência], [com/sem bullying], [nível de risco baixo/médio/alto].
                Suas respostas devem sempre separar as características por virgula, jamais misture duas características sem a separação delas
                por vírgula. Lembre-se de sempre verificar minuciosamente para analisar corretamente o texto escrito pelo aluno. Lembre-se que
                bullying e violência são muito próximos, então caso haja um existe uma chance muito grande de que também haja o outro.
                
                Comece!

                Texto: "hoje nao teve nada demais"
                Psicólogo: sem violência, sem bullying, baixo

                Texto: "hoje eu sofri bullying, fizeram muitas piadas sobre mim"
                Psicólogo: com violência, com bullying, médio

                Texto: {student_text}
                Psicólogo: 
 """



def get_llm():
  return ChatOpenAI(temperature=0, model_name='gpt-3.5-turbo')

prompt = PromptTemplate(
    template=TEMPLATE,
    input_variables=['student_text']
)

def get_llm_chain(llm, prompt=prompt):
  return LLMChain(prompt=prompt,
                  llm=llm)

def classify_text(student_text, llm_chain):
    return llm_chain.run(student_text)
  
def extract_infos(infos):
  violencia, bullying, risco = infos.split(',')
  indicios_bullying = True if "com" in bullying.lower() else False
  indicios_violencia = True if "com" in violencia.lower() else False 
  risco = risco.strip().lower()
  return indicios_bullying, indicios_violencia, risco

app = Flask(__name__)


@app.route('/api', methods=['POST'])
def get_api_response():
    data = json.loads(request.data)
    text = data.get("texto",None)
    api_key = data.get("api_key", None)
    del data['api_key']
    if text is None:
      return jsonify({"message":"text not found"})
    
    if api_key is None:
      return jsonify({"api_key":"api not found"})
    
    try:
      initiate_openai(api_key)
    except:
      return jsonify({"api_key":"openai key not valid"})
    
    llm = get_llm()
    llm_chain = get_llm_chain(llm)
    infos = classify_text(text, llm_chain)
    
    indicios_bullying, indicios_violencia, risco = extract_infos(infos)
    
    data['indicios_bullying'] = indicios_bullying
    data['indicios_violencia'] = indicios_violencia
    data['risco'] = risco
    return jsonify(data)

if __name__ == "__main__":
    app.run()
