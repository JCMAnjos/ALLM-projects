from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain.vectorstores import Chroma
import chromadb

import json
import re

class ProductsDB:

  CHROMADB_PATH = "/content/drive/MyDrive/ALLM/DB"
  EMBEDDING_MODEL_ID = "all-MiniLM-L6-v2"


  def __init__(self):

    self.embedding_function = SentenceTransformerEmbeddings(model_name=self.EMBEDDING_MODEL_ID)

    self.db = Chroma(persist_directory=self.CHROMADB_PATH, embedding_function=self.embedding_function)



  def retornaJson(self,input_string):
    data = {}
    current_key = None
    
    lines = input_string.split('\n')
    for line in lines:
        if line.strip() == "":
            continue
        if line.startswith(":"):
            data["id"] = int(line.strip(": ").strip())
        else:
            #print(re.split(r'\s*:\s*', line, maxsplit=1))
            try:
              key, value = re.split(r'\s*:\s*', line, maxsplit=1)
            except:
              #print("Erro")
              #print(re.split(r'\s*:\s*', line, maxsplit=1))
              key = re.split(r'\s*:\s*', line, maxsplit=1)[0]
              value = ""
            if key == "product_details":
                # Para o campo "product_details", analisamos a lista JSON
                # print(value)
                lines2 = value.replace("[","").replace("]","").split('}, ')
                w = {}
                for o in lines2:
                  # print(o)
                  key2, value2 = re.split(r'\s*:\s*', o, maxsplit=1)
                  # print(key2 + "  " + value2)
                # value = json.loads(value)
            data[key] = value

    # Converte o dicionário Python em uma string JSON formatada
    json_data = json.dumps(data, indent=4)

    return json_data


  def searchDoc(self,query,number_results=3):
    docs = self.db.similarity_search(query, number_results)
    result = []
    for i in docs:
      a = i.to_json()['kwargs']['page_content']
      result.append(self.retornaJson(a))
    
    return result