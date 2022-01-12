from django.shortcuts import render
from . import game
from django.views.decorators.csrf import csrf_exempt
# from django.http import HttpResponse
from django.http import JsonResponse
import json


def index(request):
    return render(request, 'index.html')

def test(request):
    return render(request, 'test.html')

def gen_grid(request):
    row = int(request.POST["row-input"])
    col = int(request.POST["col-input"])
    bomb = int(request.POST["bomb-input"])
    # maybe have some user validation
    game.set_row(row)
    game.set_col(col)
    game.set_bomb(bomb)
    game.set_tiles_revealed(0)
    game.generate_grid(row, col, bomb)
    user_map = game.get_user_map()
    args = {
        "row": row,
        "col": col,
        "bomb": bomb,
        "user_map": user_map
    }
    
    return render(request, "grid.html", args)
    
@csrf_exempt 
def add_point(request):
    var = json.loads(request.body.decode("utf-8"))
    row = int(var.get("row"))
    col = int(var.get("col"))
    game_over = not game.check_guess(row, col)
    # first check to see if its the first point clicked, if so you would generate the grid until you get a good one
    if game.get_tiles_revealed() == 0:
        while game_over:
            game.generate_grid(game.get_row(), game.get_col(), game.get_bomb())
            game_over = not game.check_guess(row, col)
    win = False
    if not game_over:
        game_over = game.check_win()
        if game_over:
            win = True
    args = {
        "user_map": game.get_user_map().tolist(),
        "game_over": game_over,
        "win": win
    }
    # return render(request, "grid.html", args)
    return JsonResponse(args)


# cool way of getting req.params from js dont delete may use for later

# def gen_grid(request):
#     var = json.loads(request.body.decode("utf-8"))
#     return JsonResponse(var)
    # return render(request, 'index.html',args )