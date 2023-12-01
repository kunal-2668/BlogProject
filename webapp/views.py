from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render,redirect, get_object_or_404
from django.core.mail import send_mail
from django.utils.safestring import SafeString
# Create your views here.

def home(request):
    data_list = Blog.objects.all()

    page = request.GET.get('page', 1)

    paginator = Paginator(data_list, 5)

    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)

    return render(request,'index.html',{'data':data})


def readMore(request,slug):
    data = Blog.objects.filter(blog_slug=slug).first()
    similartags = data.tags.all()
    datalist = []
    for i in similartags:
        for j in Blog.objects.filter(tags = i).exclude(blog_title = data.blog_title):
            if j in datalist:
                pass
            else:
                datalist.append(j)
    # datalist.remove({'blog_title':data.blog_title})

    print(datalist)
    return render (request,'readmore.html',{'data':data,'similar_posts':datalist})


def add_remove_blog_like(request,slug):
    post = get_object_or_404(Blog,blog_slug = slug)
 
    if post.likes.filter(id = request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    url = f"#{slug}"
    return redirect(f'/{url}')



def add_remove_comment_like(request,slug,id):
    comment = get_object_or_404(Comments,id = id)
 
    if comment.comment_likes.filter(id = request.user.id).exists():
        comment.comment_likes.remove(request.user)
    else:
        comment.comment_likes.add(request.user)

    url = "#Comments"
    return redirect(f'/readmore/{slug}{url}')


def signupView(request):
    if request.method == 'GET':
        return render(request,'signup.html')
    else:
        username,email,password,password1 = request.POST['username'],request.POST['email'],request.POST['password'],request.POST['password1']
        if password == password1:
            if User.objects.filter(username=username).exists():
                messages.warning(request,"Username Already Exists")
                return redirect('signup')
            elif User.objects.filter(email=email).exists():
                messages.warning(request,"Email Already Exists")
                return redirect('signup')
            else:
                User.objects.create_user(username=username,email=email,password=password)
                messages.info(request,"Account Created!!")
                return redirect('login')
        else:
            messages.warning(request,"Password mismatch")
            return redirect('signup')


def loginView(request):
    if request.method == 'GET':
        return render(request,'login.html')
    else:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username,password=password)

        if user:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'UserName/Password invalid, Try Again !!')
            return redirect('login')

    
def logoutView(request):
    logout(request)
    return redirect('login')


def addComment(request):
    if request.method == 'POST':
        comment = request.POST['comment']
        slug = request.POST['slug']
        user = request.user
        post = Blog.objects.filter(blog_slug=slug).first()

        Comments.objects.create(Post=post,Comment=comment,user=user)

        return redirect('readmore',slug=slug)


def deleteComment(request,slug,id):
    comment = Comments.objects.get(id=id)
    comment.delete()
    return redirect('readmore',slug=slug)


def Search(request):
    if request.method == 'POST':
        search = request.POST['search']
        tag = Tags.objects.filter(tagname__contains=search).first()
        data  = tag.blog_tags.all()

        return render(request,'search.html',{'data':data})
    
def shareblog(request):
    if request.method == 'POST':
        email = request.POST['email']
        body = request.POST['pagelink']
        slug = request.POST['slug']

        data = Blog.objects.get(blog_slug = slug)

        send_mail(
            "Chekout Blogs on ProBlogs",
            f"""Hey Check Out this Blog -- {body} -- copy paste this link in browser

               Blog title - {data.blog_title}
                Description - Continue Reading in above link
            """,
            "kunal00.kr@gmail.com",
            [f"{email}"],
            fail_silently=False,
        )
        url = f"{slug}"
        return redirect(f'/readmore/{url}')
    
    return redirect('home')