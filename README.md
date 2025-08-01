



# εiko

**εiko** stands for "**ε**iko : **i**nterop **k**nowledge **o**perations". 
 **εiko** is aims to be a standardized solution for deploying and operationalizing data science tools with advanced DevOps practices.

## About the project

### What's Included

**🏃 Development Environment**
- Everything for continuous delivery : Makefile, README, Docker, requirements.txt, classes for data manipulation and computation (cutsom and/or Pydantic)

**🚀 Production Backend**
- FastAPI (Swagger UI) with pagination and OAuth authentication (local JSON file, Github accounts, Keycloak private service) using JWT and encryption
- Pytest testing suite
- CLI interface via Click framework

**🌍 Analysis operators**
- Data analysis and data science toolkit featuring raster manipulation, model computations, and more. All operations are accessible via REST API or the built-in Swagger interface for authenticated users.
- Dataflow automation for more complexe analysis and data delivery. 
This tool enables you to create automated data pipelines that can download datasets, cross-reference information, apply numerical models, filter data series, and generate visualizations. Operations can be chained together and executed automatically on a scheduled basis. The *scenarios* come with a JSON file.

### Multi-Perspective Solution
As a **Key Benefit**, **εiko**  focus on data science while ensuring enterprise-grade deployment standards :

- **For Developers:** A framework and top layer for manipulating data libraries within a built-in environment. Or just a project template or a code skeleton, if *you wanna do a proper job*.

- **For Users:** A data and service provider accessible through APIs.

- **For Project Leaders:** A platform that ensures delivery and practice quality.

### Business Focus: Environmental Value

εiko specializes in complex spatial data operations, enabling:
- Cross-referencing of administrative and ecological scientific data
- Output generation: data visualizations, statistical analyses, and sophisticated models
- Satellite image processing and automated model rendering via PRISME library integration


### Core concept: smart integration (*the simpler is the better*)

εiko doesn't aim to be a code provider—it's intelligent *glue* between powerful existing data tools (Pandas, Scikit-Learn, Seaborn, PyTorch, Pydantic...). Unlike typical projects where tool selection is driven by habits, εiko prioritizes resource consumption, maintainability, low-cost performance and cost-effectiveness.

Built on principles of **sovereignty**, **ease-of-use**, and **maintainability** with a focus on **sobriety**. We prioritize the lightest and simplest solutions.

Fork it, copy it, use parts or all functionalities. The main objective is providing data users and developers a common foundation to initiate projects and start creating value as early as possible. That's doesn't mean using the "lowest-level" or "the most powerfull" code, just testing and using the lightest and more reliable one, for the job to be done.



### Achievements
Go and check the [achievements file](https://github.com/AlexLyko/eiko/blob/main/README_KPI.md).


## 101 : how to use it

### Install
Create a virtual Python3 environment and activate it.
Go through the requirements file.

#### Option #1 : run εiko on your current environment
##### On MS Windows platform :
```ps1
python -m venv ./venv
/.venv/Scripts/activate.bat
```
Or just use [Ctrl] + [Shift] + [P] for VSCode users.

Then :
```ps1
python -m pip install -r requirements.txt
```

##### On UNIX systems :
```bash
python -m venv ./venv
source venv/bin/activate
pip install -r requirements.txt
```

### Test
##### On both systems :
Everything :

```bash
pytest tests
```
#### Option #2 : using a Docker container
##### On UNIX systems :
```bash
 docker compose up
```
The "assets" folder is shared. 

Only a part :

```bash
# Will test only : GisSerie
pytest tests/test_gisserie.py 
# Will test only : Grid
pytest tests/test_grid.py 
# Will test only : Reference
pytest tests/test_reference.py 
# Will test only : ModelOutput
pytest tests/test_modeloutput.py 
# Will test only : Weighter
pytest tests/test_weighter.py 
# Will test only : AlphanumSerie
pytest tests/test_anserie.py
```
### Configure

Barely all configuration can be done using the [utils/.env](https://github.com/AlexLyko/eiko/blob/main/utils/.env) file.

#### .env parameters

These parameters are mostly related to the FastAPI service and Swagger UI, such as OAuth mode.
|  Parameter | Description  | Available values|
|---|---|---|
|OAUTH_MODE |  OAuth connection mode, integrated in Swagger UI (*Authorize* button) | "github", "keycloak", "local_db"|
|SECRET_KEY |  Choose your secret key. This one is provided as an example (from tiangolo's demo on FastAPI official doc). | Random phrase|
|GITHUB_* |  Secret and id given by the App OAuth on Github dec tools. Only used if OAUTH_MODE set to  "github".| Phrase from your Github settings|
|KEYCLOAK_* |  Keycloak configuration (especialy, URLs). Only used if OAUTH_MODE set to  "keycloak".| Phrase from your Keycloak settings|
|APP_* |  Relative to your FastAPI / Swagger UI app. Think about the final URL AS {APP_PROTOCOL}{APP_DNS}:{APP_PORT}|  By default, your app streams at http://127.0.0.1:8000|
|USER_LOCALDB_PATH|When the OAUTH_MODE is set to  "local_db", users data are stored in this JSON file. |  By default, the json file is at [assets/fake_users_db.json](https://github.com/AlexLyko/eiko/blob/main/assets/fake_users_db.json)|

When you update .env file in dev mode, uvicorn reload feature doesn't work. You'll have to manually reboot the server.

#### JSON local users database
FIle path is given by USER_LOCALDB_PATH parameter.You can modify or change this file, but you will have to keep the schema.

The default user is "johndoe" with the "secret" password : it is obviously recommanded to delete this user is this file as soon as possible after the installation.

Stored passwords are encypted : the workflow is quite "manual" here. The API *GeneratePwd* accessible through SwaggerUI allows passphrase encryption. Users can generate their own encrypted phrase and transmit it to the admin... Cause 
for now, εiko won't manage users and keep that database just to filter visitors who will be able to use the API.

#### Github access precisions
Quite hacky.
- get there : https://github.com/settings/developers
- Go to OAuth Apps, create a new app
- Configure this app with *Homepage URL = http://127.0.0.1:8000* and *Authorization callback URL = http://127.0.0.1:8000/docs/oauth2-redirect* (or your updated value with APP_* prameters, changing http://127.0.0.1:8000). Do not use "localhost".

### Launch FastAPI / Swagger UI service

##### On both systems :
Production:

```bash
python main.py eikofastapi
```
Development (with uvicorn --reload option :

```bash
pytest efastapi.py
```


### For MAKE users
Do not forget to use a virtual Python environment: 
```bash
python -m venv ./venv
source venv/bin/activate
```
εiko comes with a MakeFile.

Installation:

```bash
make install
```

Full test:
```bash
make test
```

Launch docker:
```bash
make docker
```
Launch εiko service in **production** mode:
```bash
make start_server
```
Launch εiko service in **development** mode (more verbose, uvicornreload mode):
```bash
make start_devserver
```

### Using the library
For now, examples are given in the [analysis notebook](https://github.com/AlexLyko/eiko/blob/main/demo.ipynb).

### Using the FastAPI / Swagger UI service
 API UI is accessible at [http:127.0.0.1:8000/docs](http:127.0.0.1:8000/docs), or the APP_* parameters if you updated them.
