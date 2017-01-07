import os
os.chdir(os.getenv('HOME') + '/Documents/Blender')
from pytrends import request
import pandas as pd


def ethno_fun_gen(baseline_term):
    client = request.TrendReq(
    'centaurific@gmail.com', 
    'learningglasssolutions')

    def ethno_eval(idea):
        query = baseline_term + ',' + idea
        payload = {'q':query, 
            'date':'today 24-m', 'geo': 'US'}
        trend = client.trend(payload, 
            return_type = 'dataframe')
        trend_mean = trend.mean()
        # strangely pytrends reverses the order
        out = trend_mean[0]/trend_mean[1]
        return out
    return ethno_eval

#ethno_eval = ethno_fun_gen('wallet')
#a = ethno_eval('pen wallet')
#print(a)