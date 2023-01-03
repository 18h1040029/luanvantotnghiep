import requests

for i in range(1000):
    url= "https://simple-and-complex.herokuapp.com/store/"






    response = requests.get(url)

    print(response)