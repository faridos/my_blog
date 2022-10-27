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


# Documentation of the Apis:
  accessible via dev  http://localhost:8008/redoc/
  
  accessible via prod  http://localhost/redoc/
  
  
docker, settings and requirements are seperated for prod and dev
    inside ./coreapp/settings/ 

# Config and URL endpoints:
   - Datapoint: pull from MS and create/update data Api:
   
           POST api/datapoint/<str:plant_id>/<str:from_date>/<str:to_date>

   - Datapoint Check and fetch result in case pull/reorganize/save processing did not finish:
     
           GET api/datapoint/check/<int:task_id>

   - Datapoint Report generation api :
   
           GET datapoint/monthly/report/<int:last_x_months>
           
           
  - Periodic tasks are configured in settings via the key: CELERY_BEAT_SCHEDULE
            

  
  
  
  
#Take aways
- i did not finish testing
- i did not finish report generation, 
  to make less headackes on server:
  i just went with method of computing and saving all calculations needed in a seperate DB tables
  then with needed specs , call an api , i use pandas/numpy/matplotlib to generate real pdf/images reports and download
  them
  
