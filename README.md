# media-majesty
A digital media marketplace


## Project Contributors

- _1458950_
_[Abbas Abbas](https://github.com/AbbasRabbani)_
[abbas.abbas@informatik.hs-fulda.de](mailto:abbas.abbas@informatik.hs-fulda.de)

- _1475728_
_[Achraf Boudabous](https://github.com/BoudabousAchraf)_
[achraf.boudabous@informatik.hs-fulda.de](mailto:achraf.boudabous@informatik.hs-fulda.de)

- _1377512_
_[Anwer Al-Dhify](https://github.com/AnwerHSFulda)_
[anwer-ahmed.al-dhify@informatik.hs-fulda.de](mailto:anwer-ahmed.al-dhify@informatik.hs-fulda.de)

- _1491148_
[Duru Yilmaz](https://github.com/dyilmaz03)
[duru.yilmaz@informatik.hs-fulda.de](mailto:duru.yilmaz@informatik.hs-fulda.de)

- _1458989_
[Shifali Kalra](https://github.com/shifalikalra)
[shifali.shifali@informatik.hs-fulda.de](mailto:shifali.shifali@informatik.hs-fulda.de)

- _1457966_
_[Shinu Donney](https://github.com/7ze)_
[shinu.donney@informatik.hs-fulda.de](mailto:shinu.donney@informatik.hs-fulda.de)


## How to set up the project for development in your local environment

### Prerequisites


You need to have these things set up

- `mysql` installed (ideally with a user other than root who has access to an empty database)
- `ssh` key set up with github


### Steps to reproduce

1. Clone the repository to your local directory of choice

    ```bash
    git clone git@github.com:Hochschule-Fulda-AI/media-majesty.git
    ```

> **Note**:
> Since the project is still in the development phase, use the branch `olympus`
> to get the latest approved changes and then start a new branch from there.

2. Create and activate the virtual environment for local python development

    ```python
    cd media-majesty

    python3 -m venv .venv           # creating virtual environment 

    # now activate the virtual environment;
    source .venv/bin/activate       # on unix systems
    source .venv/Scripts/activate   # on Windows (I mean why do you even use Windows really?)

    
    # remember to activate your virtual environment
    # every time you open the IDE if it doesn't do it
    # for you automatically.

    # to check if you have activated the virtual environment, 
    # you could run 
    which pip # it should point to the directory that you are in
    ```

3. Install all python dependencies needed for the project

    ```bash
    pip install -r development_requirements.txt 
    ```

4. Create the necessary environment file to run the project

    ```bash
    touch .env # creates an environment file
    ```

    Add all of these variables to this `.env` file. Make sure that
    the names are the same as given below:

    ```python
    DATABASE_NAME="<database name>"
    DATABASE_USER="<database user>"
    DATABASE_PASSWORD="<database password>"
    DATABASE_HOST="<localhost or remote host domain if you are hosting one>"
    DATABASE_PORT="<since we are using mysql, it is generally 3306>"
    ```

> **Note**:
> Make sure you have access to the database with the user and the password
> is correctly given. I recommend using a user other than 'root' for security
> reasons and building good practices.

5. Migrate the database and Run the project

    ```bash
    # if you are in the root directory first make sure to 
    # go to the directory that holds manage.py 
    cd mediamajesty

    # run the SQL migrations
    python manage.py migrate 

    # run the development server
    python manage.py runserver
    ```

And _Voila!_ Hopefully everything must have went well and you should see the 
development server running.
