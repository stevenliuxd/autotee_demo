# autotee

This web service enables auto-registration for golf course tee times via POST APIs, eliminiating the need to manually book.
* URL: https://www.somesamplegolfcourse.com

## Backend Requirements

* [Docker](https://www.docker.com/)
* [Python 3](https://www.python.org/downloads/)

## Dev Testing

* Swagger UI: http://localhost:8000/docs
* Run service (python only):
```bash
(venv) PS C:\Users\Shnau\Code\autotee> cd app >> python main.py
```

## Docker Commands

* Build docker image: 
```bash
docker build -t python-autotee .
```

* Run docker image (docker host): 
```bash
docker run -p 8000:8000 python-autotee 
```

* Remove all docker containers: 
```bash
docker rm -f $(docker ps -a -q)
```

## Virtual Environment

* Export dependencies into text file:
```bash
(venv) PS C:\Users\Shnau\Code\autotee> pip freeze > requirements.txt (install into venv first)
```

* Create virtual env:
```bash
python3 -m venv venv
```

* Install requirements into virtual env:
```bash
pip install -r requirements.txt
```

* Activate virtual env:
```bash
venv/Scripts/activate (May need Admin Powershell: Set-ExecutionPolicy RemoteSigned)
```

* Deactivate virtual env:
```bash
deactivate
```
