from pick_restful.models import User

def user_get_me(*, user: User):
    return {
        'id': user.id,
        'name': user.name,
        'email': user.email
    }

def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'me': user_get_me(user=user),
    }

def user_goal_info(queryset, startData, dateCount, needColumn):
    if queryset == None:
        return None

    dictionary = {}
    dictionary['startData'] = startData
    dictionary['dateCount'] = dateCount
    dictionary['dateList'] = []
    for idx, query in enumerate(queryset):
        if idx%3==0:
            dictionary['dateList'].append({})
            print("query", query)
            dictionary['dateList'][-1]['date'] = query['select_date'].strftime("%Y-%m-%d")
            dictionary['dateList'][-1]['userGoalList'] = []
        dictionary['dateList'][-1]['userGoalList'].append({})
        dictionary['dateList'][-1]['userGoalList'][-1]["date"] = query['select_date'].strftime("%Y-%m-%d")
        dictionary['dateList'][-1]['userGoalList'][-1]["goalId"] = query['goal']
        if 'success' in needColumn: dictionary['dateList'][-1]['userGoalList'][-1]["success"] = query['success']
        if 'diary' in needColumn: dictionary['dateList'][-1]['userGoalList'][-1]["diary"] = query['diary']

    return dictionary