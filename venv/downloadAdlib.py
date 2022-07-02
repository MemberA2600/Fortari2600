import requests
import os

source = open("source.txt", "r").read()
import re

links = re.findall(r'\/cdrom\/nightowl\-005\/050A\/[a-zA-Z0-9\s]+\.(?:ROL|ZIP)', source)

for link in links:
    link = "http://www.retroarchive.org/"+link
    name = "D:\Archieve-Copy\MEMBER\Adlib Music\ROLs\\"+link.split("/")[-1]
    if os.path.exists(name) == False:
        response = requests.get(link)
        open(name, "wb").write(response.content)
