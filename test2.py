import json
jstr='```json\n{\n  "truth_value": "FALSE",\n  "explanation": "Moderna\'s patent filings relate to mRNA technology used for vaccine development, such as the COVID-19 vaccine. There is no credible evidence or documentation that suggests Moderna had a master patent for \'cell disruptive nano-technology that can be remote controlled.\' mRNA vaccines work by instructing cells to produce a protein that is part of the virus, which the immune system then learns to fight. This technology does not involve remote control or intentionally disruptive nano-devices."\n}\n```'

jstr = jstr.strip('```').strip('json').strip()
parsed = json.loads(jstr)
truth_value = parsed['truth_value']
explanation = parsed['explanation']
print(truth_value)
print(explanation)