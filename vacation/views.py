import json
import random
from datetime import datetime

from django.core import serializers
from django.http import HttpResponse, JsonResponse
from vacation.models import CityFeature, UserCity, UserFeature

from scipy.spatial import distance
import numpy as np
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier

# from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def storeData(request):
    if request.method == "POST":
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ipaddress = x_forwarded_for.split(',')[-1].strip()
        else:
            ipaddress = request.META.get('REMOTE_ADDR')

        user = UserFeature()
        user.user_ip = ipaddress
        json_data = json.loads(request.body)
        who = json_data['who']
        # print('who:', who)

        if len(who) != 0:
            if 'Solo' in who:
                user.solo =  1
            if 'Couple' in who:
                user.couple =  1
            if 'Family' in who:
                user.family =  1
            if 'Friends' in who:
                user.friends =  1
        else:
            user.solo = None
            user.couple = None
            user.family = None
            user.friends = None



        number = json_data['number']
        if len(number) != 0:
            number = number[0]
        if number == 1:
            user.one_passengers = 1
        if number == 2:
            user.two_passengers = 1
        if number == 3:
            user.three_passengers = 1
        if number == 4:
            user.four_passengers = 1
        if number == 5:
            user.five_passengers = 1
        if number == 6:
            user.six_passengers = 1

        theme = json_data['theme']
        # print('theme:', theme)
        if len(theme)!=0:
            if 'City Life' in theme:
                user.city_life = 1
            if 'Beach' in theme:
                user.beach = 1
            if 'Nature' in theme:
                user.nature = 1
            if 'Surprise me' in theme:
                user.surprise = 1
            if 'Country side' in theme:
                user.countryside = 1
        else:
            user.city_life = None
            user.beach = None
            user.nature = None
            user.surprise = None
            user.countryside = None

        howlong = json_data['howlong']
        # print(howlong)
        if len(howlong) != 0:
            user.weekend = 1 if 'Weekend' in howlong else 0
            user.long_weekend = 1 if 'Long Weekend' in howlong else 0
            user.mid_week = 1 if 'Midweek' in howlong else 0
            user.weekish = 1 if 'Weekish' in howlong else 0
            user.three_weeks = 1 if '3 Weeks' in howlong else 0
            user.four_weeks = 1 if '4 Weeks' in howlong else 0
            user.two_weeks = 1 if '2 Weeks' in howlong else 0
        else:
            user.weekend = None
            user.long_weekend = None
            user.mid_week = None
            user.weekish = None
            user.three_weeks = None
            user.four_weeks = None
            user.two_weeks = None

        user.save()

        print("useriD=================" + str(user.user_id))

        return HttpResponse(str(user.user_id))


def updateData(request):
    if request.method == "POST":
        json_data = json.loads(request.body)
        userId = json_data['userId']
        budget = json_data['budget']
        months = json_data['months']
        who = json_data['who']
        howlong = json_data['howlong']
        theme = json_data['themes']
        number = json_data['number']
        traveler = json_data['traveler']

        user = UserFeature.objects.get(user_id=userId)
        user.delete()

        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

        if x_forwarded_for:
            ipaddress = x_forwarded_for.split(',')[-1].strip()
        else:
            ipaddress = request.META.get('REMOTE_ADDR')

        user = UserFeature()
        user.user_id = userId
        user.user_ip = ipaddress

        if len(who) != 0:
            if 'Solo' in who:
                user.solo =  1
            if 'Couple' in who:
                user.couple =  1
            if 'Family' in who:
                user.family =  1
            if 'Friends' in who:
                user.friends =  1
        else:
            user.solo = None
            user.couple = None
            user.family = None
            user.friends = None

        for i in range(0, len(number)):
            if number[i] == 1:
                user.one_passengers = 1
            if number[i] == 2:
                user.two_passengers = 1
            if number[i] == 3:
                user.three_passengers = 1
            if number[i] == 4:
                user.four_passengers = 1
            if number[i] == 5:
                user.five_passengers = 1
            if number[i] == 6:
                user.six_passengers = 1

        if len(howlong) != 0:
            user.weekend = 1 if 'Weekend' in howlong else 0
            user.long_weekend = 1 if 'Long Weekend' in howlong else 0
            user.mid_week = 1 if 'Midweek' in howlong else 0
            user.weekish = 1 if 'Weekish' in howlong else 0
            user.three_weeks = 1 if '3 Weeks' in howlong else 0
            user.four_weeks = 1 if '4 Weeks' in howlong else 0
            user.two_weeks = 1 if '2 Weeks' in howlong else 0
        else:
            user.weekend = None
            user.long_weekend = None
            user.mid_week = None
            user.weekish = None
            user.three_weeks = None
            user.four_weeks = None
            user.two_weeks = None


        # print(budget)
        if len(budget) != 0:
            user.budget_low = 1 if 'low' in budget else 0
            user.budget_normal = 1 if 'normal' in budget else 0
            user.budget_high = 1 if 'high' in budget else 0


        # print(traveler)
        if len(traveler) != 0:
            user.comp_allboys = 1 if 'boys' in traveler else 0
            user.comp_allgirls = 1 if 'girls' in traveler else 0
            user.comp_elderly = 1 if 'elderly' in traveler else 0
            user.comp_kids_babies = 1 if 'kids' in traveler else 0

        # print(theme)

        if len(theme) != 0:
            user.city_life = 1 if 'City Life' in theme else 0
            user.romantic = 1 if 'Romantic' in theme else 0
            user.shopping = 1 if 'Shopping' in theme else 0
            user.beach = 1 if 'Beach' in theme else 0
            user.honeymoon = 1 if 'Honeymoon' in theme else 0
            user.camping = 1 if 'Camping' in theme else 0
            user.adventures = 1 if 'Adventures' in theme else 0
            user.ski = 1 if 'Ski' in theme else 0
            user.remote = 1 if 'Remote' in theme else 0
            user.wildlife = 1 if 'Wildlife' in theme else 0
            user.hiking = 1 if 'Hiking' in theme else 0
            user.road_trip = 1 if 'Road Trip' in theme else 0
            user.festivals = 1 if 'Festivals' in theme else 0
            user.nightlife = 1 if 'Nightlife' in theme else 0
            user.holidays = 1 if 'Holidays' in theme else 0
            user.vivid = 1 if 'Vivid' in theme else 0
            user.cultural_experience = 1 if 'Cultural Experience' in theme else 0
            user.surfing = 1 if 'Surfing' in theme else 0
            user.scuba_diving = 1 if 'Scuba Diving' in theme else 0
            user.nature = 1 if 'Nature' in theme else 0
            user.countryside = 1 if 'Countryside' in theme else 0
            user.surprise = 1 if 'Surprise' in theme else 0
            user.other = 1 if 'Other' in theme else 0


        # setting months
        # print(months)
        if 1 in months:
            user.january = months[0]
            user.february = months[1]
            user.march = months[2]
            user.april = months[3]
            user.may = months[4]
            user.june = months[5]
            user.july = months[6]
            user.august = months[7]
            user.september = months[8]
            user.october = months[9]
            user.november = months[10]
            user.december = months[11]

        user.save()
        return HttpResponse("Successfully Updated")


def getCityInfo(request):
    # json_data = json.loads(request.body)
    # print(json_data)
    cities = CityFeature.objects.all().order_by('?').values()
    user = UserFeature.objects.latest('time_stamp')

    user_fields = [field.name for field in user._meta.get_fields()]

    # for i in ['user_id','user_ip','time_stamp']:
    #     user_fields.remove(i)

    user_features = {}
    for field in user_fields:
        user_features[field] = getattr(user, field)


    # print('user_features::::::::::::;;;\n', user_features)
    nanFeatures = []
    for feature in user_features.keys():
        if user_features[feature] is None:
            nanFeatures.append(feature)
    passengers_features = ['one_passengers', 'two_passengers', 'three_passengers', 'four_passengers', 'five_passengers', 'six_passengers']
    df_cities = pd.DataFrame(cities).fillna(0).drop(
        ['city_id', 'short_description', 'sites', 'picture', 'country'] + nanFeatures + passengers_features , axis=1)

    df_user = pd.DataFrame(user_features, index=[0]).drop(['user_id','user_ip','time_stamp']+nanFeatures + passengers_features, axis=1)
    # print('df_cities:\n', df_cities.drop(['city_name'], axis=1))
    df_user = df_user*1
    # df_user.to_csv('df_user.csv')
    # df_cities.to_csv('df_cities.csv')
    # print('df_user:\n', df_user)
    # print('df_cities:\n', df_cities)

    columns_user = list(df_user.columns)
    columns_cities = list(df_cities.columns)
    # print('columns_user:\n', columns_user)
    # print('columns_cities:\n', columns_cities)


    X = df_cities.drop(['city_name'], axis=1)
    y = df_cities['city_name']

    important_features = ['romantic','shopping','honeymoon','camping',
                          'adventures','ski','remote','wildlife','hiking','road_trip','festivals',
                          'nightlife','holidays','vivid','cultural_experience','surfing','scuba_diving']

    super_features = ['city_life', 'beach','nature','countryside','ski']
    # print('important_features\n', important_features)
    weights = weight_func(columns_user,important_features, super_features)
    weights = np.array(weights)
    # print('weights:\n', weights.shape)

    # neigh = KNeighborsClassifier(n_neighbors=4,metric_params={'w':weights})
    # neigh.fit(X, y)
    # distAndPred = neigh.kneighbors(X=df_user, return_distance=True)
    # pred = distAndPred[1]
    # print(y[pred[0]])
    # cities_names= list(y[pred[0]])

    cities_features = []

    cities_matrix = df_cities.drop(['city_name'], axis=1).to_numpy()

    UserFeaturesVector = df_user.to_numpy()


    # for cityList in listOfLists_cities:
    #     # print('jaccard::::::::::',distance.jaccard(cityList[1:], listOfUserFeatures, weights))
    #     cityList.append(distance.jaccard(cityList[1:], listOfUserFeatures, weights))
    # print('listoflists::::',listOfLists_cities)
    #
    # # df_cities = pd.DataFrame(listOfLists_cities).sort_values(by =35 )
    # cities_list = pd.DataFrame(listOfLists_cities).sort_values(35, ascending=True)[0].values.tolist()
    # print(df_cities)
    # print('cities:\n', cities_matrix)

    UserFeaturesVector = UserFeaturesVector*weights
    cities_dot_user = cities_matrix.dot(np.transpose(UserFeaturesVector))
    cities_matrix_with_names = df_cities.to_numpy()
    c = np.c_[cities_matrix_with_names, cities_dot_user]
    c_df = pd.DataFrame(c)#,columns=df_cities.columns+['score'])
    c_df = c_df.sort_values(c_df.columns[-1], ascending=False)
    # print('c_df\n', c_df)
    cities_names = c_df[0]

    for cname in cities_names:
        cities_features.append(CityFeature.objects.filter(city_name=cname).values()[0])

    return JsonResponse(cities_features,safe=False)
    # cities_list = list(cities)
    # print(cities_list)
    # return JsonResponse(cities_list,safe=False)


def addRatingMatching(request):
    json_data = json.loads(request.body)

    try:
        userCity = UserCity.objects.get(user_id=json_data['userId'], city_name=json_data['city_name'])
    except:
        userCity = UserCity()
    userCity.city_name = json_data['city_name']
    userCity.user_id = json_data['userId']
    userCity.users_rating = json_data['users_rating']
    userCity.matching_score = random.randint(0, 100)

    userCity.save()

    return HttpResponse("Success save into user_matching_table")


def weight_func(columns_user, important_features, super_features):

    important_that_exists = []
    super_that_exists = []
    for col in columns_user:
        if col in important_features:
            important_that_exists.append(col)
        elif col in super_features:
            super_that_exists.append(col)



    weights = [1] * len(columns_user)

    for feature in important_that_exists:
        important_index = columns_user.index(feature)
        weights[important_index] = 3
    for feature in super_that_exists:
        super_index = columns_user.index(feature)
        weights[super_index] = 15
    # print(columns_user)
    # print(weights)
    return weights