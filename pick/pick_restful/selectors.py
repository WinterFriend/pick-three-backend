from pick_restful.models import User
from django.db.models.query import QuerySet
import datetime

def user_get_me(*, user: User) -> dict:
    return {
        'id': user.id,
        'name': user.name,
        'email': user.email
    }

def jwt_response_payload_handler(token: str, user=None, request=None) -> dict:
    return {
        'token': token,
        'me': user_get_me(user=user),
    }

def user_goal_info(
    queryset: QuerySet, 
    startDate: str,
    dateCount: str, 
    needColumn: list
) -> dict:
    if queryset == None:
        return None

    dictionary = {}
    dictionary['startDate'] = startDate
    dictionary['dateCount'] = dateCount
    dictionary['userGoalList'] = {}
    cur_date = datetime.datetime.strptime(startDate, "%Y-%m-%d")

    for _ in range(dateCount):
        cur_str = cur_date.strftime("%Y-%m-%d")
        dictionary['userGoalList'][cur_str] = []
        cur_date = cur_date + datetime.timedelta(days=1)

    for query in queryset:
        select_date_str = query['select_date'].strftime("%Y-%m-%d")
        dictionary['userGoalList'][select_date_str].append({})
        dictionary['userGoalList'][select_date_str][-1]['date'] = select_date_str
        dictionary['userGoalList'][select_date_str][-1]["goalId"] = query['goal']

        if 'success' in needColumn:
            dictionary['userGoalList'][select_date_str][-1]["success"] = query['success']
        if 'diary' in needColumn:
            dictionary['userGoalList'][select_date_str][-1]["diary"] = query['diary']
    return dictionary