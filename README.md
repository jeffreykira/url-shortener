# url-shortener

## Environment Dependency
- python3
- pip install -r requirements.txt


## Quick Start
1. run API server
```
project_path > python3 run.py
```
2. open Swagger API document on the browser
```
http://localhost:5604/api/v1/
```


## Run Unit Test
- test all files
```
project_path > python -m unittest discover -v url_shortener/test
```

- test specific file
```
project_path > python -m unittest -v url_shortener/test/{test_file_name}
```