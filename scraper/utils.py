def group(fn):
    d = {}
    with open(fn,'r') as f:
        data = f.readlines()
        for line in data[1:]:
            key,value = line.rsplit('/',1)
            d.setdefault(key,[]).append(value.strip())
    
    return d


print(group('out.csv'))
