[![Build Status](https://travis-ci.org/Tevinthuku/Politico.svg?branch=develop)](https://travis-ci.org/Tevinthuku/Politico)
[![Maintainability](https://api.codeclimate.com/v1/badges/65cb6a9e0fc4d16df8ce/maintainability)](https://codeclimate.com/github/Tevinthuku/Politico/maintainability)
[![Coverage Status](https://coveralls.io/repos/github/Tevinthuku/Politico/badge.svg?branch=develop)](https://coveralls.io/github/Tevinthuku/Politico?branch=develop)

![](https://img.shields.io/github/last-commit/Tevinthuku/Politico/develop.svg?style=for-the-badge)
![](https://img.shields.io/pypi/pyversions/flask.svg?style=for-the-badge)

# Politico

A Platform for driving political change and engagement

[Hosted on Heroku](https://tevpolitico.herokuapp.com/)

[Documentation on APIARY](https://tevzpolitico.docs.apiary.io/#)

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

4. SET up envs
   Follow the format provided in the `.env.sample` file to create your own local `.env` file
   Once your `.env` is ready run.

   **NB**

   - You will need a sendgrid account so that you can paste your API key in the SENDGRID env variable

```

source ./.env

```

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

| Method   | Endpoint                              | Description                           |
| -------- | ------------------------------------- | ------------------------------------- |
| `GET`    | `/api/v1/offices`                     | View All offices created by the ADMIN |
| `POST`   | `/api/v1/offices`                     | Post a new office                     |
| `GET`    | `/api/v1/offices/<int:office_id>`     | Get a specific office                 |
| `GET`    | `/api/v1/parties`                     | View all parties created by ADMIN     |
| `POST`   | `/api/v1/parties`                     | Post a new party                      |
| `GET`    | `/api/v1/parties/<int:party_id>`      | Get specific party Id                 |
| `PATCH`  | `/api/v1/parties/<int:party_id>/name` | Update a party by name                |
| `DELETE` | `/api/v1/parties/<int:party_id>`      | Delete a party by Id                  |

</details>

<details open>

<summary>V2 Politico Endpoints</summary>

| Method   | Endpoint                                     | Description                                                                                                      |
| -------- | -------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| `POST`   | `/api/v2/auth/signup`                        | Create a new user                                                                                                |
| `POST`   | `/api/v2/auth/signin`                        | User can login                                                                                                   |
| `POST`   | `/api/v2/auth/reset`                         | User can reset password                                                                                          |
| `GET`    | `/api/v2/parties`                            | Fetch all parties                                                                                                |
| `POST`   | `/api/v2/parties`                            | Admin can post a party                                                                                           |
| `GET`    | `/api/v2/parties/<int:party_id>`             | Get specific party details                                                                                       |
| `PATCH`  | `/api/v2/parties/<int:party_id>/name`        | Admin can Update a party by its name                                                                             |
| `DELETE` | `/api/v2/parties/<int:party_id>`             | An Admin can delete a party                                                                                      |
| `POST`   | `/api/v2/offices`                            | An Admin can create an office                                                                                    |
| `GET`    | `/api/v2/offices`                            | Get all offices created in the DB                                                                                |
| `GET`    | `/api/v2/offices/<int:office_id>`            | Get a specific office from the DB                                                                                |
| `POST`   | `/api/v2/offices/<int:office_id>/register`   | A admin can register a candidate to an office                                                                    |
| `POST`   | `/api/v2/votes`                              | A registered user can vote                                                                                       |
| `GET`    | `/api/v2/offices/<int:office_id>/result`     | A user can view the results of a particular office                                                               |
| `GET`    | `/api/v2/users`                              | Should be able to get a list of all users                                                                        |
| `POST`   | `/api/v2/authorize/<int:user_id>`            | An admin can make other users admins                                                                             |
| `GET`    | `/api/v2/offices/<int:office_id>/candidates` | This view shows a list of all the candidates in a particular office                                              |
| `GET`    | `/api/v2/offices/metainfo`                   | This view returns results info on an office, candidates vying and also the results after voting for all offices  |
| `POST`   | `/api/v2/votes/activity`                     | This request returns all offices with infomation as to whether a user has voted or not in that particular office |
| `POST`   | `api/v2/auth/newpassword`                    | This endpoint updates the password of an existing user                                                           |

</details>

### Author: TevinThuku

### Credits: Andela
