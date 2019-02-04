# Politico

A Platform for driving political change and engagement

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
    - export FLASK_APP=run.py
    - export FLASK_DEBUG=1
    - export FLASK_ENV=development

5. Running tests
      ```
         python -m pytest --cov=app/api
      ```
##Politico Endpoints

| Method | Endpoint          | Description                           |
| ------ | ----------------- | ------------------------------------- |
| `GET`  | `/api/v1/offices` | View All offices created by the ADMIN |



### Author: TevinThuku

### Credits: Andela
