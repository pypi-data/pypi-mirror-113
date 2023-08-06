# Grimoire

Grimoire is a Python library to create interactive fiction.
What makes Grimoire unique is that it pre-renders all possible
choices and simply outputs linked HTML files.

## Installation

```
pip install grimoire-if
```

## Usage

Check out some [examples](examples/).

### Your story begins

Begin by instantiating a Grimoire app.

```
from grimoire import Grimoire


app = Grimoire()
```

Then create our stories initial page.

```
@app.page
def start(state):
    state['name'] = 'Grimoire'
    return f"Hello, {state['name']}!", state
```

You can render our (rather boring) story right now by calling the app's render method.

```
app.render()
```

Grimoire added all the html files (in this case only the index.html file) into the site/ directory.

You can optionally pass a state class when creating your app.

```
@datalass
class State:
    name: Optional[str] = None


app = Grimoire(state=State)

@app.start
def start(state):
    state.name = 'Grimoire'
    return f"Hello, {state.name}!", state
```

Grimoire uses [hype](https://github.com/scrussell24/hype-html) to render html and you can use it in your render functions.

```
from hype import *


@app.start
def start(state):
    state.name = 'Grimoire'
    return H1(f"Hello, {state.name}!"), state
```

### Choose your own destiny

Let's add some options.

```
@app.option(start, "Next")
def next(state):
    return P("We're really moving now!"), state
```

Try rendering again. If you reload the index.html file, you should now see a link (Next) that brings you to the next page.
