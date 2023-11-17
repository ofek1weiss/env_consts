# env_consts
Use environment variables as consts in python

## Usage
First, define a class for your consts. Then, decorate it with `env_const`. Finally, use the class as you would use any other class.
```python
from env_consts import env_const

@env_const
class Consts:
    SERVER_HOST: str = 'localhost'
    SERVER_PORT: int = 8080

print(Consts.SERVER_HOST, Consts.SERVER_PORT)
```
When running the above code normally, it will print `localhost 8080`. However, if you set the environment variables `SERVER_HOST` and `SERVER_PORT` to something else, it will print those values instead.

## Installation
```bash
pip install env-consts
```
