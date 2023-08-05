# Brisk
*The fast ASGI framework*
___

[Repository](https://github.com/endercheif/brisk_py)

### Table of Contents
1. [Usage](#usage)
2. [Documentation](#documentation)

---
### Usage

Install using pip:
`pip install brisk-py`

##### Basic Example:
```python
from brisk_py import brisk
app = brisk.App()

# simple routing
@app.get('/')
def route(request):
    return '<h1>Hello World</h1>'
# render html file
@app.get('/')
def route(request):
    return brisk.html('index.html')

```

##### Create an api
```python
from brisk_py import brisk 
app = brisk.App()

users = {'users': [{'user': 'John Doe', 'age': 34}, {'user': 'Jane Doe', 'age': 37}]}

@app.get('/users')
def route(request):
    return users

@app.get('/user')
def route(request):
    user = request.body.get('user')
    if user:
        return users.get(user, {'message': 'user not found'})
    else:
        return {'message': 'no user provided'}

@app.post('/users')
def route(request):
    user = request.body.get('user')
    age = request.body.get('age')

    if age and user:
        users.append({'user': user, 'age': age})
        return {'message': 'success'}
    else:
        return {'message': 'error'}

```
##### Run Python in HTML
```python
# main.py
from brisk_py import brisk 
app = brisk.App()

@app.get('/')
def route(request):
    fav_things = ['raindrops on roses', 'whiskers on kittens', 'bright copper kettles', 'warm woolen mittens']
    return html('index.html', fav_things=fav_things)

```


---
### Documentation
TBD