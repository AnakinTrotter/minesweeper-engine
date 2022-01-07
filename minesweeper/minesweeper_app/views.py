from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.http import JsonResponse
# Notes for KAM: response to browser

def index(request):
    return render(request, 'index.html')

def test(request):
    return render(request, 'test.html')

@csrf_exempt 
def gen_grid(request):
    print(request)
    print("hihi")
    args = {"test_stuff": "hellotest"}
    return JsonResponse(args)
    # return render(request, 'index.html',args )