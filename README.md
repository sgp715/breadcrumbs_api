# Breadcrumbs API

## Install
* Make sure you have python3
* Install the python requirements
```
$ pip3 install -r requirements.txt
```

## Getting Started
* move the sample_config.json file to config.json
```
$ mv sample_config.json config.json
```
* go into the config.json file and add the api key
* run the flask app
```
$ python3 app.py
```

## Example Calls
* The crumbs endpoint will return you the images corresponding to crumbs
```
$ http://127.0.0.1:5000/api/v1/crumbs?origin=chicago&destination=palo+alto
```
