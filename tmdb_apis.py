import requests
import pandas as pd
import json

api_key="3d790715684442ccd60d3bd18e76fc9b"
api_base_url = "https://api.themoviedb.org/3"


def get_search_results(search_query):
    endpoint_path = f"/search/movie"
    endpoint = f"{api_base_url}{endpoint_path}?api_key={api_key}&query={search_query}"
    r = requests.get(endpoint)
    results = r.json()
    if r.status_code != 200:
        raise Exception("get_search_results failed: {}".format(results["status_message"]))
    return results['results']


def get_movie_detail(movie_id):
    endpoint_path = f"/movie/{movie_id}"
    endpoint = f"{api_base_url}{endpoint_path}?api_key={api_key}"
    r = requests.get(endpoint)
    results = r.json()
    if r.status_code != 200:
        raise Exception("get_search_results failed: {}".format(results["status_message"]))
    return results


def get_movie_reviews(movie_id):
    endpoint_path = f"/movie/{movie_id}/reviews"
    endpoint = f"{api_base_url}{endpoint_path}?api_key={api_key}"
    r = requests.get(endpoint)
    results = r.json()
    if r.status_code != 200:
        raise Exception("get_search_results failed: {}".format(results["status_message"]))
    return results['results']

# print(get_movie_reviews(577922)[0])

# movie_id = "movie_id"
# api_key = "3d790715684442ccd60d3bd18e76fc9b"
# api_base_url = "https://api.themoviedb.org/3"
# endpoint_path = f"/movie/{movie_id}/reviews"
# endpoint = f"{api_base_url}{endpoint_path}?api_key={api_key}"
# r = requests.get(endpoint)
# print(r.text)
# pprint.pprint(r.json()
# print(get_movie_detail(577922))



# "original_title"
# "poster_path"



"genres"
"homepage"
"popularity"
"release_date"
"revenue"
"status"
"vote_average"
"vote_count"


# "overview"



# """
# Endpoint
# /movie/{movie_id}
# https://api.themoviedb.org/3/movie/550?api_key=3d790715684442ccd60d3bd18e76fc9b
# api_key=3d790715684442ccd60d3bd18e76fc9b"
# """

#movie_id = 550


# endpoint_path = f"/search/movie"
# search_query = "Interstellar"
# endpoint = f"{api_base_url}{endpoint_path}?api_key={api_key}&query={search_query}"
# # print(endpoint)
# r = requests.get(endpoint)
# # print(r.status_code)
# # print(r.text)
# # pprint.pprint(r.json())
# if r.status_code in range(200,299):
#     data = r.json()
#     results = data['results']
#     if len(results) > 0:
#         #print(results[0].keys())
#         movie_ids = set()
#         for result in results:
#             _id = result['id']
#             print(result['title'],_id)
#             movie_ids.add(_id)
#         print(list(movie_ids))
#     output = 'movie.csv'
#     movie_data = []
    # for movie_id in movie_ids:
    #     api_base_url = "https://api.themoviedb.org/3"
    #     endpoint_path = f"/movie/{movie_id}"
    #     endpoint = f"{api_base_url}{endpoint_path}?api_key={api_key}&query={search_query}"
    #     r = requests.get(endpoint)
    #     if r.status_code in range(200, 299):
    #         data = r.json()
    #         movie_data.append(data)

#     # df = pd.DataFrame(movie_data)
#     # print(df.head())
#     # df.to_csv(output,index=False)