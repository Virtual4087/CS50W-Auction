**An auction website created using django that uses sqlite as database.**

**Live Demo** - https://youtu.be/OHSdf_ca4uE?si=TTCPDLox2hbjA-DS

# Setup Guide
- Download the source code
- Install Django
- Install Sqlite3
- Run python manage.py makemigrations auctions
- Run python manage.py migrate
- Run python manage.py runserver

**Note:- There are no categories at the start so if you want to add any categories do it through Sqlite shell or django admin for easier access.**
# To setup Django admin interface
- Run python manage.py createsuperuser
- Setup the username, email and passowrd
- Visit /admin and make direct changes to the database
