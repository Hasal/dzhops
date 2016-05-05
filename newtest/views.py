from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def testHtml(request):
    user = request.user.username
    return render(
        request,
        'test.html'
    )

@login_required
def testIndex(request):
    user = request.user.username
    return render(
        request,
        'anew/index.html'
    )