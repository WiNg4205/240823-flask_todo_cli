import json
from flask import Flask, render_template
import click

app = Flask(__name__)

DATA_FILE = 'data.json'

def load_data():
    try:
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_data(data):
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file)

data = load_data()

@app.route('/')
def hello():
    return render_template("index.html", tasks=data)

@app.cli.command("greet")
@click.argument("name", nargs=-1)
def greet(name):
    """Greet the user by name."""
    name = ' '.join(name)
    print(f"Hello, {name}!")

# Create
@app.cli.command("add")
@click.argument("task", nargs=-1)
def add(task):
    task = ' '.join(task)
    data.append(task)
    save_data(data)

# Read
@app.cli.command("read")
def read():
    for index, task in enumerate(data):
        print(index, task)
    
# Update
@app.cli.command("update")
@click.argument("index", type=int)
@click.argument("updated_task")
def update(index, updated_task):
    data[index] = updated_task
    save_data(data)

# Delete
@app.cli.command("delete")
@click.argument("index", type=int)
def delete(index):
    data.pop(index)
    save_data(data)

@app.cli.command("pop")
def pop():
    data.pop()
    save_data(data)

if __name__ == "__main__":
    app.run(debug=True)