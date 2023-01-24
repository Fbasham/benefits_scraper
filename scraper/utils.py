import json

def group(fn):
    d = {}
    with open(fn,'r') as f:
        data = json.load(f)
        for item in data:
            key,value = item['url'].rsplit('/',1)
            d.setdefault(key,[]).append(value)
    
    for k in d:
        print(k)
        print(d[k])
        print('----------------')
        print()

    return d


print(group('out.json'))
