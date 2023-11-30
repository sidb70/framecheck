import os
import json
from langchain.retrievers.you import YouRetriever
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI

yr = YouRetriever()
model = "gpt-4-1106-preview"
qa = RetrievalQA.from_chain_type(llm=ChatOpenAI(model=model), chain_type="stuff", retriever=yr)
instruction = "Verify the claim as 'TRUE' or 'FALSE' and explain why with factual evidence. Reply with JSON object with 'truth_value' and 'explanation' keys. In your explanation, do not use first-person tense, only provide a reasoning. Claim: "
claim = 'There have been lab accidents in the past where viruses have escaped.'
prompt = instruction + claim
res = qa.run(prompt)
res = res.strip('```').strip('json').strip()
parsed = json.loads(res)
truth_value = parsed['truth_value']
explanation = parsed['explanation']
print(truth_value)
print(explanation)