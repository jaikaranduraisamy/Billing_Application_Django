Operating System: Ubuntu

Required software:
########################################################################
doucker
docker-compose

How to Run Docker:
########################################################################
1) Open a terminal where docker-compose.yml file is located.
2) Run a command - sudo docker-compose up --build (or) sudo docker compose up --build
3) Make sure any already docker container with same name. To check docker container - Sudo docker ps

Steps for database Migration in Django:
########################################################################
1) Update the changes in the Django Models i.e: models.py
2) Enter into the DB shell using command - sudo docker exec -it billing_application_backend_1 /bin/bash
3) command - python3 manage.py makemigrations web_app
4) command - python3 manage.py migrate

Steps to create admin user for Django:
########################################################################
1) command - python manage.py createsuperuser
2) command - admin
3) command - <email>
4) command - admin

Add required row for the table product
########################################################################
1) Open web browser
2) Use Domain - http://localhost:8000/admin
3) Enter username and password we created above
4) Add row for the tblProduct

To use the billing application
########################################################################
1) Open web browser
2) Use Domain - http://localhost:3000
3) Enter all the fileld. Make sure all the fields are entered.
4) Click on "Generate Bill" button.
5) A pdf is generated and downloaded with A4 potrait page.


To view all the records in the table. Use this api call
########################################################################
1) To view tblCustomer, Use Domain - http://localhost:8000/api/allCustomer
2) To view tblProduct, Use Domain - http://localhost:8000/api/allProduct
3) To view tblOrder, Use Domain - http://localhost:8000/api/allOrder
