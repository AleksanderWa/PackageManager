# PackageManager
Made with **Python 3.10** and **Django 4.0**

Admin application for online furniture distribution.

### Key features:
- 2 admin views:
  - 1: showing all orders with necessary data like (date created, customer name, country, order status, delivery company, furniture weight, number of packages and packages weight)
  - 2: showing all order items with custom highlights. Order items with more than 3 packages will have violet border. Order items within Benelux countries and furniture weight > 200 kg are going to have red background.
- 1st view allows to select orders and set them status to "Ready to send" allowing user to select delivery company.

## Installation (for developers):
1. git clone repository
2. create virtual env with Python 3.10
3. pip install -r requirements.txt
4. create postgres database and set edit settings.py accordingly to your db
5. python manage.py migrate
6. python manage.py seed_db -> this will create test fixtures
7. use admin user to log in
   8. login:admin
   9. password:password



