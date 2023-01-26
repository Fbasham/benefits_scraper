import json

def group(fn):
    d = {}
    with open(fn,'r') as f:
        data = json.load(f)
        for item in data:
            key,value = item['url'].rsplit('/',1)
            d.setdefault(key,[]).append(value)

    return d


# test:
data = group('out.json')
for key in data:
    print(key)
    print(data[key])
    print('-'*75)
    print()
