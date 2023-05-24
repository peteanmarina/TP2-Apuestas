import http.client

conn = http.client.HTTPSConnection("v3.football.api-sports.io")

headers = {
    'x-rapidapi-host': "v3.football.api-sports.io",
    'x-rapidapi-key': "daeb6aa8bc02aa81529f3cd03698f6b8"
    }

conn.request("GET", "/{endpoint}", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))
