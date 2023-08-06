# python-module-resources

Import non-python files in a project directory as python namedtuple objects.

If you've ever worked in node, you might be familiar with a language feature which allows you to pull in a json file as an imported module.

```node
import { dataStuff } from 'myProjectResources/jsonFiles'

dataStuff.contents === "A rich javascript object"
```

With `module_resources`, you can achieve something similar in python.

```py
from my_project_resources.json_files import data_stuff

data_stuff.contents == 'A python namedtuple instance'
```
## Caveats

There are some caveats to be aware of.

#### Valid vs. invalid namedtuple field names

```py
>>> from module_resources.examples.json import logging_config
>>> logging_config.loggers.__main__
```
```
git checkout master
git pull origin master
# examples of preparing a new tag for release
make tag-patch # also accepts: tag-minor, tag-major
git push origin --tags
```