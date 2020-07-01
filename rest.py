import requests
url = 'https://lf8q0kx152.execute-api.us-east-2.amazonaws.com/default/computeFitnessScore'
x = requests.post(url,json={"qconfig": "3 6 2 7 1 4 8 5","userID":799945, "githubLink":"https://github.com/Prem38sri/Samples/blob/master/8QueensProblem.ipynb"})
print(x.text)
