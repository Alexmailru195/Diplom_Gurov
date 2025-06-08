from django.shortcuts import render


def profile_view(request):
    return render(request, 'user_profile/user_profile.html')
