import json
from cw20190516gridl import gridLO
from cw20190516gridl2 import gridLO2

from cw20190517across import across_clues
from cw20190517down import down_clues

# a Python object (dict):
x = gridLO

# convert into JSON:
y = json.dumps(x)
z = json.loads(y)
# the result is a JSON string:
print(x)