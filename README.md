# GraphQL
An example project showing integration of Graphene, Flask and SQLAlchemy. This is based on the [Example Flask+SQLAlchemy Project](https://github.com/graphql-python/graphene-sqlalchemy/tree/master/examples/flask_sqlalchemy). 

I have included GraphQl mutations and have used graphene.relay for pagination. See example queries below.


# Set up Guide

Clone the whole repository:
```
git clone https://github.com/AryaDevops/GraphQL.git

```

Create a virtual environment (advisable but not required) in which the dependencies will be installed

```
virtualenv env
source env/bin/activate

```

Now, install all dependencies,

```
pip install -r requirements.txt

```

Now run the following command to set up the database and start the server

```
python ./app.py

```

Go to http://127.0.0.1.5000/graphql to go to query the server.
