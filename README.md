# ExcelPlay Kryptos
Follow the steps below to start the API server:
  - Primary requirements (These need to be preinstalled)
    - pip
    - virtualenv
  - Create a virtual environment and activate it
    ```sh
    $ virtualenv -p python3.6 server
    $ source server/bin/activate
    ```
  - Install the requirements
    ```sh
    $ pip install -r requirements.txt
    ```
  - Set up Mysql Database
    ```sh
    $ mysql -u root -p
    '''
    '''sh
    mysql> CREATE DATABASE kryptos CHARACTER SET UTF8;
    mysql> CREATE USER excel@localhost IDENTIFIED BY 'password';
    mysql> GRANT ALL PRIVILEGES ON kryptos.* TO excel@localhost;
    mysql> exit
    '''
    '''sh
    $ mysql -u excel -p kryptos < kryptos.sql
    '''

  - Run the dev server
    ```sh
    $ python manage.py makemigrations
    $ python manage.py migrate
    $ python manage.py createsuperuser
    $ python manage.py runserver
    ```
