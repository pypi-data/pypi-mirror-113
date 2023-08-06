import re
def parse_ris(filename):
    with open(filename,'r') as f:
        content = ';'.join(f.readlines())
        print(content)
        _author = re.findall('AU\s\s-\s(.*)',content)
        _title = re.findall('TI\s\s-\s(.*)',content)[0]
        _journal = re.findall('JA\s\s-\s(.*)',content)[0]
        _year = re.findall('PY\s\s-\s(.*)',content)[0]
        _type = re.findall('TY\s\s-\s(.*)',content)[0]
        print(_author,_title)

if __name__ =='__main__':
    parse_ris('./8008942.ris')
