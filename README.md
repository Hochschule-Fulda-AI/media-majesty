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
- `poetry` installed, check the [documentation](https://python-poetry.org/docs/)

Optionally, it would be nice if you have
- `make`build tool, makes our life easier. check [documentation](https://www.gnu.org/software/make/#download)

```sh
# On mac, you can install it with brew if you don't have it already

brew install make
```

### Steps to reproduce

1. Clone the repository to your local directory of choice

    ```bash
    git clone git@github.com:Hochschule-Fulda-AI/media-majesty.git
    ```

> **Note**:
> Since the project is still in the development phase, use the branch `olympus`
> to get the latest approved changes and then start a new branch from there.

2. Create and activate the virtual environment for local python development

    ##### Creating virtual environment

    ```python
    cd media-majesty

    python3 -m venv .venv           # creating virtual environment
    ```

3. Install all python dependencies needed for the project using poetry

    ##### Installing dependencies
    Poetry automatically installs and builds a lock file specific to your platform

    ```bash
    poetry install # installs all the dependencies into the virtual environment

    # or alternatively, if you have make
    make install
    ```

    ##### Activating virtual environment

    ```bash
    poetry shell # activates the virtual environment
    ```

4. Create the necessary environment file to run the project

    ```bash
    touch .env # creates an environment file
    ```

    Add all of these variables to this `.env` file. Make sure that
    the names are the same as given below:

    ```python
    SECRET_KEY="<secret key>"
    DEBUG="<True or False depending on if you are in development or production>"
    DATABASE_ENGINE="django.db.backends.mysql"
    DATABASE_NAME="<database name>"
    DATABASE_USER="<database user>"
    DATABASE_PASSWORD="<database password>"
    DATABASE_HOST="<localhost or remote host domain if you are hosting one>"
    DATABASE_PORT="<since we are using mysql, it is generally 3306>"
    DEFAULT_FILE_STORAGE="storages.backends.azure_storage.AzureStorage"
    AZURE_MEDIA_CONTAINER="<azure media container name>"
    AZURE_THUMBNAIL_CONTAINER="<azure thumbnail container name>"
    ```

> **Note**:
> Make sure you have access to the database with the user and the password
> is correctly given. I recommend using a user other than 'root' for security
> reasons and building good practices.

5. Migrate the database and Run the project

    ##### Database migrations with django ORM

    ```bash
    # if you are in the root directory first make sure to
    # go to the directory that holds manage.py
    cd mediamajesty

    # run the SQL migrations
    python manage.py makemigrations
    python manage.py migrate

    # or alternatively,
    make migrations
    make migrate

    # run the development server
    python manage.py runserver

    # or alternatively,
    make run
    ```


    And _Voila!_ Hopefully everything must have went well and you should see the
    development server running.

> **Note**:
> These `manage.py` commands will only work if you are inside poetry's virtual
> environment which you should have activated from the previous step hopefully.

> **Pro Tip**:
> You can check out the Makefile and try other commands

```bash
# For eg, make start will install the dependencies, run migrations and run
# the development server automatically

make start
```

6. One final note, install pre-commit:

    Before you make changes and do your commit for the first time after you clone
    this repository, make sure to install pre-commit into your git hooks so it can
    run automatically and make checks when you do a commit.

    ```bash
    # this installs pre-commit to your git hooks
    pre-commit install
    ```

    Also, if you make any additional changes to the pre-commit configuration
    file `.pre-commit-config.yaml`, then you should run ths file again to make
    sure the new version is installed.

---

> **Note**
> Please always make sure the [virtual environment is
> activated](#activating-virtual-environment) before you start working on the
> project. Use `poetry` to manage and install dependencies.

> Also, make sure that in case of breaking changes that require additional
> dependencies or database updates, you [install the new
> dependencies](#installing-dependencies) and [migrate the
> database](#database-migrations-with-django-orm) if needed.
