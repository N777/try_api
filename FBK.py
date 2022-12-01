import glob
import os
import re
import subprocess

for file in glob.glob('FBK/*.FBK'):
    name_without_datetime = re.sub(r'_\d{2}_\d{2}_\d{4}_\d{2}_\d{2}_\d{2}', '', file)
    command = f"gbak -c -user sysdba -password masterkey {file} {name_without_datetime[:-4]+'.FDB'}"
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    exit_code = p.wait()
    print("Конвертнул")
    if 'engine' in file.lower():
        os.rename(name_without_datetime[:-4] + '.FDB', "FBK/Engine.FDB")
        isql_exec = 'isql -u {user} -p {passwd} -ch WIN1251 -i {migration} {fb_server}:{layer_location}'.format(
            user='sysdba',
            passwd='masterkey',
            migration=os.path.abspath('engine_migrator.sql'),
            fb_server='127.0.0.1/3050',
            layer_location=os.path.abspath("FBK/Engine.FDB"))
        p = subprocess.Popen(isql_exec, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        (_, err) = p.communicate()
        exit_code = p.wait()
        print("Накатил миграцию")
    os.remove(file)
