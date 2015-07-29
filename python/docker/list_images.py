import json
from docker import Client

c = Client(base_url='unix://var/run/docker.sock')

print(json.dumps(c.images(), sort_keys=True, indent=4, separators=(',',': ')))


