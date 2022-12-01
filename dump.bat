set db=billing_staging
dropdb -f -U postgres %db%
psql -U postgres -c "create database %db%"
psql -d %db% -U postgres -f "C:\PythonProjects\try_api\postgre\billing_staging_2022111851032_52783.tar"
pause