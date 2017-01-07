import os
os.chdir(os.getenv('HOME') + '/Documents/Blender')
from pytrends import request
import pandas as pd


def ethno_fun_gen():
    client = request.TrendReq(
    'centaurific@gmail.com', 
    'learningglasssolutions')

    def ethno_eval(idea):
        payload = {'q':idea, 'date':'today 24-m'}
        trend = client.trend(payload, 
            return_type = 'dataframe')
        out = trend.mean()[0]
        return out
    return ethno_eval

#ethno_eval = ethno_fun_gen()
#a = ethno_eval('wallet')
#print(a)