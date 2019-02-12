[![Build Status](https://travis-ci.org/Tevinthuku/Politico.svg?branch=develop)](https://travis-ci.org/Tevinthuku/Politico)
[![Maintainability](https://api.codeclimate.com/v1/badges/65cb6a9e0fc4d16df8ce/maintainability)](https://codeclimate.com/github/Tevinthuku/Politico/maintainability)
[![Coverage Status](https://coveralls.io/repos/github/Tevinthuku/Politico/badge.svg?branch=develop)](https://coveralls.io/github/Tevinthuku/Politico?branch=develop)


![](https://img.shields.io/github/last-commit/Tevinthuku/Politico/develop.svg?style=for-the-badge)
![](https://img.shields.io/pypi/pyversions/flask.svg?style=for-the-badge)
# Politico

A Platform for driving political change and engagement

[Hosted on Heroku](https://tevpolitico.herokuapp.com/)

## Setup and installation

1. Set up virtualenv

   ```bash
        virtualenv venv
   ```

2. Activate virtualenv

   ```bash
        source venv/bin/activate
   ```

3. Install dependencies

   ```bash
        pip install -r requirements.txt
   ```

4. Setup env variables
    - $ export FLASK_APP=run.py
    - $ export FLASK_DEBUG=1
    - $ export FLASK_ENV=development
    - $ export SECRET_KEY=`<SECRET KEY>`
    - $ export DATABASE_URL=`<URI>`
    - $ export DATABASE_TEST_URL=`<URI>`


5. Running tests
      ```
         python -m pytest --cov=app/api
      ```
6. Start the server
      ```
         flask run
      ```

<details>
<summary>V1 Politico Endpoints</summary>


| Method   | Endpoint                             | Description                           |
| -------- | ------------------------------------ | ------------------------------------- |
| `GET`    | `/api/v1/offices`                    | View All offices created by the ADMIN |
| `POST`   | `/api/v1/offices`                    | Post a new office                     |
| `GET`    | `/api/v1/offices/<int:office_id>`    | Get a specific office                 |
| `GET`    | `/api/v1/parties`                    | View all parties created by ADMIN     |
| `POST`   | `/api/v1/parties`                    | Post a new party                      |
| `GET`    | `api/v1/parties/<int:party_id>`      | Get specific party Id                 |
| `PATCH`  | `api/v1/parties/<int:party_id>/name` | Update a party by name                |
| `DELETE` | `api/v1/parties/<int:party_id>`      | Delete a party by Id                  |
</details>

<details open>

<summary>V2 Politico Endpoints</summary>

| Method   | Endpoint                             | Description                           |
| -------- | ------------------------------------ | ------------------------------------- |
</details>


### Author: TevinThuku

### Credits: Andela
