from torch import cuda, bfloat16
import transformers
import torch
from transformers import StoppingCriteria, StoppingCriteriaList

# define custom stopping criteria object
class StopOnTokens(StoppingCriteria):
    def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor, stop_token_id, **kwargs) -> bool:
        for stop_ids in stop_token_id:
            if torch.eq(input_ids[0][-len(stop_ids):], stop_ids).all():
                return True
        return False

class FineTunedModel:

    MODEL_ID = "ianagra/Llama-2-7b-ALLM-virtual-sales-assistant"

    TAMANHO_MAXIMO_CHAT = 14
    mensagens = []
    history = ""

    def __init__(self):
        self.device = f'cuda:{cuda.current_device()}' if cuda.is_available() else 'cpu'

        bnb_config = transformers.BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type='nf4',
            bnb_4bit_use_double_quant=True,
            bnb_4bit_compute_dtype=bfloat16
        )


        hf_auth = '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'
        model_config = transformers.AutoConfig.from_pretrained(
            self.MODEL_ID,
            use_auth_token=hf_auth
        )

        self.model = transformers.AutoModelForCausalLM.from_pretrained(
            self.MODEL_ID,
            trust_remote_code=True,
            config=model_config,
            quantization_config=bnb_config,
            device_map='auto',
            use_auth_token=hf_auth
        )

        # enable evaluation mode to allow model inference
        self.model.eval()

        #print(f"Model loaded on {self.device}")

        self.tokenizer = transformers.AutoTokenizer.from_pretrained(
            self.MODEL_ID,
            use_auth_token=hf_auth
        )
    
        stop_list = ['</s>', '\n```\n']

        stop_token_ids = [self.tokenizer(x)['input_ids'] for x in stop_list]
        
        stop_token_ids = [torch.LongTensor(x).to(self.device) for x in stop_token_ids]

        stopping_criteria = StoppingCriteriaList([StopOnTokens()],stop_token_id=stop_token_ids)


        self.generate_text = transformers.pipeline(
            model=self.model,
            tokenizer=self.tokenizer,
            return_full_text=False,  # langchain expects the full text
            task='text-generation',
            # we pass model parameters here too
            #stopping_criteria=stopping_criteria,  # without this model rambles during chat
            temperature=0.1,  # 'randomness' of outputs, 0.0 is the min and 1.0 the max
            max_new_tokens=512,  # max number of tokens to generate in the output
            repetition_penalty=1.1  # without this output begins repeating
        )

    def addConversationMsg(self,query,user):
        tag = ""
        if(user) :
            tag = "user: "
        else:
            tag = "assistant"

        self.mensagens.append({"role":tag,"content":query})

        if(len(self.mensagens)>self.TAMANHO_MAXIMO_CHAT):
            self.mensagens.pop(0)

        return self.mensagens

#    def getLLmResponse(self,contextOrder,contextProducts,query):
#        chatHistory = self.addConversationMsg(query,True)
#
#        prompt = context + "Chat history: \n"
#        for i in chatHistory:
#            prompt = prompt + i['role'] + ": " + i['content'] + "\n"

        
#        res = self.generate_text(prompt)
#        self.addConversationMsg(res[0]["generated_text"],False)

#        return res[0]["generated_text"]

    def getLLmResponse(self, contextOrder, contextProducts, query, FirstPrompt):
        if FirstPrompt:
            instruction = "<s>[INST] <<SYS>>\n\nPretend to be an online store clerk. Only give products informations that are on store product list or information about customers orders or information about the store politics\n\n<</SYS>>\n\n"
            self.history += instruction + query + "[/INST]"
            prompt = instruction + f"{query}\n\nStore product list: {contextProducts}\nUser orders: {contextOrder}[/INST]"
        else:
            prompt = self.history + f"[INST]{query}\n\nStore product list: {contextProducts}\nUser orders: {contextOrder}[/INST]"
            self.history += f"[INST]{query}[/INST]"
                
        res = self.generate_text(prompt)
        texto_gerado = res[0]["generated_text"]
        self.history += texto_gerado
        saida = f"===\nPROMPT\n===\n\n{prompt}\n\n===\nRESPOSTA GERADA\n===\n\n{texto_gerado}"
        return saida