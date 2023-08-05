import typer
import os

app = typer.Typer()

### Templates for our Scaffolding Features
apiTemplateV2 = """from solace import Api

def greet(req, res, next):
    res.json = {"Hello": "World" }

api = Api()
api.get("/", greet)

# NOTE: to run your api in development mode
# just run 'solace dev' in the root of your 
# project. Feel free to remove this note.

# NOTE: to test the api, you can curl it.
# curl -s http://127.0.0.1:5000
# You should be greeted with the message:
# {"Hello": "World"}
"""

dockerfileTemplate = """FROM python:3.9.5-alpine3.13
RUN pip install gunicorn solace
EXPOSE 5000
COPY src/ /src
WORKDIR /
CMD ["gunicorn", "-b", "0.0.0.0:5000", "src.api:api"]
"""

@app.command()
def api(name: str):
  """ create a new api project """
  # Dockerfile
  # src/
  #   __init__.py
  #   api.py
  #   handlers.py
  # README.md
  os.mkdir(name)
  os.chdir(name)
  f = open('README.md', 'w+')
  f.close()
  f = open('Dockerfile', 'w+')
  f.write(dockerfileTemplate)
  f.close()
  os.mkdir('src')
  os.chdir('src')
  f = open('api.py', 'w+')
  f.write(apiTemplateV2)
  f.close()
  # f = open('handlers.py', 'w+')
  # f.write(handlersTemplate)
  # f.close()
  f = open('__init__.py', 'w+')
  f.close()
  print("You're all set!\nTo get started with development, run the following command:\n")
  print(f"cd {name} && solace run dev\n")
