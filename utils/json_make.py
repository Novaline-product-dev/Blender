import json, os, pickle
os.chdir(os.getenv('HOME') + '/Documents/Blender')


with open('yc_objs.p', 'rb') as f:
    objs = pickle.load(f)
descriptions = objs[0]
targets = objs[1]
names = objs[2]
weights = objs[3]
urls = objs[4]

yc_list = []
for i, el in enumerate(names):
    dict_i = dict()
    name_i = names[i]
    desc_i = [d[1] for d in descriptions if d[0] == name_i]
    dict_i['Description'] = desc_i[0]
    dict_i['Name'] = name_i
    dict_i['Weight'] = weights[i]
    url_i = [u[1] for u in urls if u[0] == name_i]
    dict_i['URL'] = url_i[0]
    yc_list.append(dict_i)

with open('yc.json', 'w') as f:
    json.dump(yc_list, f)

with open('targets.json', 'w') as f:
	json.dump(targets, f)

