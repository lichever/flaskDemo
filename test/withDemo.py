

from contextlib import contextmanager
import json

# obj = dict(name='小明', age=20)
obj = {'name':'小明', 'age':20}
s = json.dumps(obj, ensure_ascii=False)
print(s)



@contextmanager
def file_manager(name, mode):
    try:
        f = open(name, mode)
        yield f
    finally:
        f.close()

try:
    with file_manager('test.txt', 'r') as f:
        print(f.read())
except Exception as e:
    print("文件未找到，请检查文件路径。", e)
    exit(0)
    
    