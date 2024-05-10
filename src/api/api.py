from ninja import NinjaAPI

api = NinjaAPI()





@api.get("/get_user_total_score")
def get_user_total_score(request):
    return "Hello world"