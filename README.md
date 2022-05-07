### This repo has several micro-services
1. Users
   1. /user/<user_id> - GET
   2. /users - GET
2. Accounting
   1. /accounts - GET
   2. /accounts/user/<user_id> - GET
   3. /account/charge - POST
3. Products
   1. /product/<product_id> - GET
   2. /product/order - POST
   3. /products - GET
4. Ordering
   1. /order/<order_id> - GET
   2. /order - POST
   3. /orders - GET

### Tools and libraries used
1. [Flask](https://flask.palletsprojects.com/en/2.1.x/) - Lightweight web framework
2. [SQLAlchemy](https://docs.sqlalchemy.org/en/14/orm/tutorial.html) -  Abstracting db operations
3. [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/) - Creating of db and tables quickly
4. [Requests](https://docs.python-requests.org/en/latest/) -  Making http calls between microservices
5. [Locust](https://docs.locust.io/en/stable/installation.html) - Load testing
6. [Docker](https://docs.docker.com/engine/install/) - Containerising applications
7. [Docker-Compose](https://docs.docker.com/compose/) - Running multiple applications in containers
8. SQLite database - to persist our data


### Dev set up
1. Install Docker from links in the tools sections above
2. Run 
```shell
docker-compose up --build
```