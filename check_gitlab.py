import requests
import datetime

gitlab_token = "Bearer glpat-T7jMoBNBiVFF8Dg2Wa7x"
yt_token = 'Bearer perm:0JLQsNC00LjQvF/QldCz0L7RgNC+0LI=.NDQtOQ==.yhRzlybjMDg39ejEwQpYkB66fH99Qq'
gitlab_base_url = 'https://gitlab.litebox.ru/api/v4/projects/53'
yt_base_url = 'https://yt.litebox.ru/api'
gitlab_datetime_format = '%Y-%m-%dT%H-%M-%SZ'

def get_agiles():
    response = requests.get(f'{yt_base_url}/issues/LB-26178?fields=id,summary,customFields(id,name,value(avatarUrl,buildLink,color(id),fullName,id,isResolved,localizedName,login,minutes,name,presentation,text))',
                            headers={"Authorization": yt_token})
    return response.json()['customFields'][8]['name']

def get_merge_requests(updated_before):
    updated_after = updated_before - datetime.timedelta(weeks=2)
    response = requests.get(f'{gitlab_base_url}/merge_requests',
                            params={'updated_after': updated_after.strftime(gitlab_datetime_format),
                                    'updated_before': updated_before.strftime(gitlab_datetime_format),
                                    'state': 'merged',
                                    'target_branch': 'develop'},
                            headers={"Authorization": gitlab_token})
    return response.json()


mrs = get_merge_requests(datetime.datetime.now())
get_agiles()
mrs_filtered = [mr for mr in mrs if 'feature' in mr['source_branch']]
temp = ''
for mr in mrs_filtered:
    temp += f'<div><a href="{mr["web_url"]}">{mr["title"]}</a><p>{mr["description"]}</p></div><hr>'
print(temp)
