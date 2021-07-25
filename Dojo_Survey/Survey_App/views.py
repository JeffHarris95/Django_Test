from django.shortcuts import redirect, render

def index(request):
    return render(request,'index.html')

def create(request):
    print(request.POST)
    request.session['name'] = request.POST["name"]
    request.session['location'] = request.POST["location"]
    request.session['language'] = request.POST["language"]
    request.session['comments'] = request.POST["comments"]
    return redirect('/results')

def results(request):
    return render(request,'results.html')