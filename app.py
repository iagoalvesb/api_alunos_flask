import json
from flask import request, jsonify
from flask import Flask, render_template

import os
from langchain import PromptTemplate, LLMChain
from langchain.chat_models import ChatOpenAI


# TEMPLATE = """  Você vai agir como um psicólogo que observa textos de alunos e consegue extrair informações sobre o sentimento do aluno, o
#                 real sentimento dele quando estava escrevendo o texto.
#                 As características que você irá relatar no texto são [positivo/negativo/neutro], [com/sem violência], [nível de preocupação baixo/médio/alto].
#                 Suas respostas devem sempre separar as características por virgula, jamais misture duas características sem a separação delas por
#                 vírgula. Lembre-se de sempre verificar se o texto possui um sentimento negativo, se relata alguma violência (física ou verbal), e
#                 você sabe que bullying também é violência.
                
#                 Comece!

#                 Texto: "hoje nao teve nada demais"
#                 Psicólogo: neutro, sem violência, baixo.

#                 Texto: "hoje eu sofri bullying, fizeram muitas piadas sobre mim"
#                 Psicólogo: negativo, com violência, médio.

#                 Texto: {student_text}
#                 Psicólogo: 
#  """

# os.environ['OPENAI_API_KEY'] = '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'
# llm = ChatOpenAI(temperature=0, model_name='gpt-3.5-turbo')

# prompt = PromptTemplate(
#     template=TEMPLATE,
#     input_variables=['student_text']
# )

# llm_chain = LLMChain(
#     prompt=prompt,
#     llm=llm
# )

# def classify_text(student_text):
#     return llm_chain.run(student_text)

app = Flask(__name__)

# @app.route('/api', methods=['POST'])
# def get_api_response():
#     return jsonify(request.json)
#     output = request.get_json()
#     dict_values = json.loads(output)
#     return json.dumps(dict_values)
#     dict_values['texto'] = classify_text(dict_values['texto'])
#     return json.dumps(dict_values)


@app.route('/api', methods=['POST'])
def get_api_response():
    data = json.loads(request.data)
    text = data.get("texto",None)
    api_key = data.get("api_key",None)
    
    if text is None:
      return jsonify({"message":"text not found"})
    
    if api_key is None:
      return jsonify({"api_key":"api not found"})
    
    return jsonify(data)
    dict_values['texto'] = classify_text(dict_values['texto'])
    return json.dumps(dict_values)

@app.route('/returnjson', methods = ['GET'])
def ReturnJSON():
    if(request.method == 'GET'):
        data = {
            "Modules" : 15,
            "Subject" : "Data Structures and Algorithms",
        }
  
        return jsonify(data)

  
@app.route('/service', methods=['POST'])
def service():
    data = json.loads(request.data)
    text = data.get("text",None)
    if text is None:
        return jsonify({"message":"text not found"})
    else:
        return jsonify(data)
 

@app.route('/process_json', methods=['POST'])
def process_json():
    json_data = request.get_json()  # Obtém o JSON enviado pelo consumidor
    return jsonify(json_data)
  
if __name__ == "__main__":
    app.run()
