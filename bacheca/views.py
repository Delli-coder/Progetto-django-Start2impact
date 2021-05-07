from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from .models import UserProfile
from .models import Post
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from django.contrib import messages


def ip_address(request):
    x_forward = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forward:
        ip = x_forward.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


def registration(request):
    ip = ip_address(request)
    form = RegisterForm(request.POST)
    if form.is_valid():
        user = form.save()
        new_user = UserProfile()
        new_user.user = user
        new_user.ipAddress = ip
        new_user.username = user.username
        new_user.save()
        return redirect('/homepage')
    else:
        form = RegisterForm()
        return render(request, 'registration.html', {'form': form})


@login_required
def home_page(request):
    this_ip = ip_address(request)
    user = request.user
    if not user.is_superuser:
        prof_user = user.username
        x = UserProfile.objects.filter(username=prof_user).values('ipAddress')
        s = x[0]
        if this_ip != s['ipAddress']:
            messages.info(request, 'Attenzione! indirizzo IP differente!')
            UserProfile.objects.filter(username=prof_user).update(ipAddress=this_ip)
    if request.method == 'POST':
        messaggio = request.POST
        if 'hack' in messaggio['msg'] or 'Hack' in messaggio['msg']:
            return HttpResponse("<h1>Nei post non si puo' inserire la parola hack</h1>")
        else:
            new_post = Post(user=request.user, content=messaggio['msg'])
            new_post.set_date()
            new_post.save()
            response = []
            posts = Post.objects.filter().order_by('-published_date')
            for post in posts:
                response.append({
                    'content': post.content,
                    'author': f"{post.user}",
                    'published_date': post.published_date
                })
            return render(request, 'home_page.html', {'post': response})
    else:
        response = []
        posts = Post.objects.filter().order_by('-published_date')
        for post in posts:
            response.append({
                'content': post.content,
                'author': f"{post.user}",
                'published_date': post.published_date
            })
        return render(request, 'home_page.html', {'post': response})


def id_user(request, pk):
    user = User.objects.filter(id=pk).values()
    return render(request, 'id_user.html', {'user': user})


def number_post(request):
    user_list = User.objects.filter(is_superuser=False)
    total_post = {}
    for user in user_list:
        cont = 0
        posts = Post.objects.filter(user=user).values()
        for post in posts:
            cont += 1
        total_post[user.username] = cont

    return render(request, 'number_post.html', {'total_post': total_post})


def hour_post(request):
    h_post = []
    now = timezone.now()
    posts = Post.objects.filter().order_by('-published_date')
    for post in posts:
        if now - post.published_date <= timedelta(0, 3599):
            h_post.append(
                {
                    'author': f"{post.user}",
                    'content': post.content,
                    'published_date': post.published_date
                }
            )
    return JsonResponse(h_post, safe=False)


def get_word(request):
    word = request.GET.get('', 'start2impact')
    posts = Post.objects.filter()
    count = 0
    x = str(word)
    for post in posts:
        if x in post.content:
            count += 1
    return HttpResponse(f'La parola {x} è stata scritta {count} volte nei post')


# Create your views here.
