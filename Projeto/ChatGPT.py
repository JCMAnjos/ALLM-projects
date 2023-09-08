import json

import os
import openai

class ChamadaGPT:


  TAMANHO_MAXIMO_CHAT = 14
  mensagens = []

  API_KEY = "123412532456234514"

  Id_modelo = "gpt-3.5-turbo"

  def __init__(self):
    self.Headers = {"Authorization": f"Bearer ${self.API_KEY}", "content-type": "Application/json" }
    self.Link = "https://api.openai.com/v1/chat/completions"

    # openai.organization = "org-Iw1RkDQO49zCq4gAkejiuhGw"
    openai.api_key = self.API_KEY





  def addConversationMsg(self,query,user):
    tag = ""
    if(user) :
      tag = "user"
    else:
      tag = "assistant"

    self.mensagens.append({"role":tag,"content":query})

    if(len(self.mensagens)>self.TAMANHO_MAXIMO_CHAT):
      self.mensagens.pop(0)

    return self.mensagens.copy()

  def getLLmResponse(self,contextOrder,contextProducts,query):
    msg = self.addConversationMsg(query,True)

    msg.insert(0,{"role": "system","content": "pretend to be an online store clerk. Only give products informations that are on store product list or information about customers orders or information about the store politics" })
    # msg.insert(2,{"role": "system","content": "Only give products informations that are on store product list"})
    msg.insert(1,{"role": "system","content": "Store product list: " + contextProducts})
    msg.insert(2,{"role": "system","content": "User order: " + contextOrder})
    

    Body_mensagem = {

              "model": self.Id_modelo,

              "messages": msg #[{"role": "user", "content": "escreva um e-mail para o meu chefe dizendo a previsão do preço do dólar nos próximos 2 meses"}]

    }

    Body_mensagem = json.dumps(Body_mensagem)

    print(Body_mensagem)

    try:
      Requisicao = openai.ChatCompletion.create(model=self.Id_modelo, messages=msg)
    except:
      return "ERRO na API do GPT" 


    # print(Requisicao)

    # Resposta = Requisicao.json()

    Mensagem = Requisicao["choices"][0]["message"]["content"]

    # print(Mensagem)

    msg = self.addConversationMsg(Mensagem,False)

    # print(msg)

    return Mensagem
