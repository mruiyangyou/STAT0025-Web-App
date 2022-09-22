import numpy as np
import json

def input_preprocess(input):
    return np.array(json.loads(input))