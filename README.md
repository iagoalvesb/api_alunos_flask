# API para Hackaton Campus Party Goiás - 2023

API para a extração de informação em textos para a solução  do Hackaton Campus Party GO 2023.

O tema para está edição foi "Como podemos agregar tecnologia de forma benéfica à segurança, prevenção e/ou identificação da violência em ambientes educacionais?"

## Tecnologias utilizadas:
- Flask
- Langchain

## Executar localmente
- clonar repositório
- pip install -r requirements.txt
- flask run

## Realizar chamadas à API
- Passar um json para <link_aplicacao>/api contendo ao menos as seguintes chaves:
- - api_key: chave de acesso à API da OpenAI
- - texto: texto para ser analisado

## Retorno da API
- Json original adicionado as seguintes chaves:
- - indicios_bullying: booleano relatando se há ou não há indícios de bullying no texto
- - indicios_violencia: booleano relatando se há ou não há indícios de violência no texto
- - risco: classificação de risco que o texto apresenta [baixo/médio/alto]
