here a simple makefile to run needed commands to install and go :

- make migrate  # to have our DB tables ready
- make createsuperuser  # to have our DB tables ready
- make run  # run dev compose
- make collectstatic

for production, just add '-prod' for same commands : like
- make migrate-prod 


# How the app is served

Base url on Dev: http://localhost:8008

Api base url : http://localhost:8008/api/

Base url on prod: http://localhost

