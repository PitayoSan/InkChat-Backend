# InkChat-Backend

## Virtualenv

### Create venv

In order for the server to be isolated from the rest of the computer, a Python virtualenv must be created.  
There, all the project's dependencies will be installed and the server can be tested safely in _development_ or _debug_ modes.

To create a virtualenv, you must create a _venv_ directory (already ignored by git):

`$ mkdir venv`

and assign the virtualenv to the created directory:

`$ python3 -m virtualenv venv`


### Activate venv

To activate the venv, do:

`$ . venv/bin/activate`

or

`$ source ./venv/bin/activate`

Now your terminal should look like this:

`(venv) $`

Now you can work safely from inside the virtual environment.
There you can install the necessary dependencies as well as run your flask app.


### Deactivate venv

To deactivate the venv, do:

`(venv) $ deactivate`

Now your terminal should look as always:

`$`


## Dependencies

In a virtualenv, dependencies are installed in the same way that in a normal environment:

`(venv) $ pip install Flask`

But, as mentioned earlier, the installed dependencies will only be available inside the venv. Just keep that in mind.


### Installing the project's dependencies

The dependencies that are currently being used throughout the project can be found in the `requirements.txt` file.  
To install them, do:

`(venv) $ pip install -r requirements.txt`


### Adding dependencies

When you add a dependency, in order for the `requirements.txt` file to be updated just do:

`(venv) $ pip freeze > requirements.txt`


## Exporting the necessary environment variables

Flask needs two environment variables in order to work.  
You can export them with:

`(venv) $ export FLASK_APP=run.py`
`(venv) $ export FLASK_ENV=development`

or store them in a `.env` file (already ignored by git).

Also, in order for the server endpoints to interact properly with Firebase, the following env var is needed:

`(venv) $ export FS_BUCKET=<project's bucket>`

which can also be exported or stored in a file.


## Run server

Finally, run the server with:

`(venv) $ flask run`
