from django.shortcuts import render
from . import game
# from django.views.decorators.csrf import csrf_exempt
# from django.http import HttpResponse
# from django.http import JsonResponse
# import json


def index(request):
    return render(request, 'index.html')

def test(request):
    return render(request, 'test.html')

def gen_grid(request):
    row = int(request.POST["row-input"])
    col = int(request.POST["col-input"])
    bomb = int(request.POST["bomb-input"])
    # maybe have some user validation
    args = {
        "row": row,
        "row_len": range(row),
        "col": col,
        "col_len": range(col),
        "bomb": bomb,
    }
    # maybe return a grid idk or return some type of redirect 
    return render(request, "grid.html", args)


# cool way of getting req.params from js dont delete may use for later
# @csrf_exempt 
# def gen_grid(request):
#     var = json.loads(request.body.decode("utf-8"))
#     return JsonResponse(var)
    # return render(request, 'index.html',args )