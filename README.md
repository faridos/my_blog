here a simple makefile to run needed commands to install and go :

- make migrate  # to have our DB tables ready
- make createsuperuser  # to have our DB tables ready
- make run-dev  # run dev compose
- make run-prod # run the production setup

# How the app is served

Base url on Dev: http://localhost:8008

Api base url : http://localhost:8008/api/

Base url on prod: http://localhost


Documenting the api : localhost:8008/redoc/

docker, settings and requirements are seperated for prod and dev
# URLS:
   - Datapoint: pull from MS and create/update data Api:
   
           POST api/datapoint/<str:plant_id>/<str:from_date>/<str:to_date>

   - Datapoint Check and fetch result in case pull/reorganize/save processing did not finish:
     
           GET api/datapoint/check/<int:task_id>

   - Datapoint Report generation api :
   
           GET datapoint/monthly/report/<int:last_x_months>
           
           
# Documentation of the Apis:
  accessible via http://localhost:8008/redoc/