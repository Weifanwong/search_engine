
import json


data = {
    'name' : 'ACME',
    'shares' : 100,
    'price' : 542.23
}

dict1 = json.dumps(data)

print(type(data),type(dict1))
print(dict1)