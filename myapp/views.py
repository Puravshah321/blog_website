from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import *
from django.shortcuts import HttpResponseRedirect

from .models import Comment,Post
# Create your views here.
def index(request):
    return render(request,"index.html",{
        'posts':Post.objects.filter(user_id=request.user.id).order_by("id").reverse(),
        'top_posts':Post.objects.all().order_by("-likes"),
        'recent_posts':Post.objects.all().order_by("-id"),
        'user':request.user,
        'media_url':settings.MEDIA_URL
    })


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        first_name = request.POST['first_name']  # Get first name
        last_name = request.POST['last_name']    # Get last name
        date_of_birth = request.POST['date_of_birth']
        
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,"Username already Exists")
                return redirect('signup')
            if User.objects.filter(email=email).exists():
                messages.info(request,"Email already Exists")
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.first_name = first_name  # Save first name
                user.last_name = last_name    # Save last name
                user.date_of_birth = date_of_birth
                user.save()
                return redirect('signin')
        else:
            messages.info(request,"Password should match")
            return redirect('signup')
            
    return render(request,"signup.html")
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        first_name = request.POST['first_name']  # Get first name
        last_name = request.POST['last_name']    # Get last name
        
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,"Username already Exists")
                return redirect('signup')
            if User.objects.filter(email=email).exists():
                messages.info(request,"Email already Exists")
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.first_name = first_name  # Save first name
                user.last_name = last_name    # Save last name
                user.save()
                return redirect('signin')
        else:
            messages.info(request,"Password should match")
            return redirect('signup')
            
    return render(request,"signup.html")

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,"Username already Exists")
                return redirect('signup')
            if User.objects.filter(email=email).exists():
                messages.info(request,"Email already Exists")
                return redirect('signup')
            else:
                User.objects.create_user(username=username,email=email,password=password).save()
                return redirect('signin')
        else:
            messages.info(request,"Password should match")
            return redirect('signup')
            
    return render(request,"signup.html")

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect("index")
        else:
            messages.info(request,'Username or Password is incorrect')
            return redirect("signin")
            
    return render(request,"signin.html")

def logout(request):
    auth.logout(request)
    return redirect('index')

def blog(request):
    selected_categories = request.GET.getlist('categories')
    posts = Post.objects.filter(category__in=selected_categories).order_by("-id")
    return render(request,"blog.html",{
            'posts':Post.objects.filter(user_id=request.user.id).order_by("id").reverse(),
            'top_posts':Post.objects.all().order_by("-likes"),
            'recent_posts':Post.objects.all().order_by("-id"),
            'user':request.user,
            'media_url':settings.MEDIA_URL
        })
    
def create(request):
    if request.method == 'POST':
        try:
            postname = request.POST['postname']
            content = request.POST['content']
            category = request.POST['category']
            image = request.FILES['image']
            Post(postname=postname,content=content,category=category,image=image,user=request.user).save()
        except:
            print("Error")
        return redirect('index')
    else:
        return render(request,"create.html")
    
def profile(request,id):
    
    return render(request,'profile.html',{
        'user':User.objects.get(id=id),
        'posts':Post.objects.all(),
        'media_url':settings.MEDIA_URL,
    })
    
    
def profileedit(request, id):
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
    
        user = User.objects.get(id=id)
        user.first_name = firstname
        user.last_name = lastname
        user.email = email
        user.save()
        return redirect('profile', id=id)  # Redirect to the profile page after saving the changes

    return render(request, "profileedit.html", {
        'user': User.objects.get(id=id),
    })

    
@login_required
def increaselikes(request, id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=id)
        if request.user in post.liked_by.all():
            post.liked_by.remove(request.user)
            post.likes -= 1
        else:
            post.liked_by.add(request.user)
            post.likes += 1
        post.save()
    return redirect("index")

@login_required
def increaselike(request, id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=id)
        if request.user in post.liked_by.all():
            post.liked_by.remove(request.user)
            post.likes -= 1
        else:
            post.liked_by.add(request.user)
            post.likes += 1
        post.save()
    return redirect("blog")


def post(request,id):
    post = Post.objects.get(id=id)
    
    return render(request,"post-details.html",{
        "user":request.user,
        'post':Post.objects.get(id=id),
        'recent_posts':Post.objects.all().order_by("-id"),
        'media_url':settings.MEDIA_URL,
        'comments':Comment.objects.filter(post_id = post.id),
        'total_comments': len(Comment.objects.filter(post_id = post.id))
    })
    
def savecomment(request,id):
    post = get_object_or_404(Post, id=id)
    if request.method == "POST":
        message = request.POST.get('message')
        parent_id = request.POST.get('parent_id')  # Get the parent ID if it's a reply

        # If a parent ID is provided, create a reply
        if parent_id:
            parent_comment = get_object_or_404(Comment, id=parent_id)
            comment = Comment(user=request.user, post=post, content=message, parent=parent_comment)
        else:
            # If no parent ID, create a normal top-level comment
            comment = Comment(user=request.user, post=post, content=message)

        comment.save()
        return redirect('post', id=id)  # Redirect back to the post page

    #return HttpResponseForbidden("Invalid request")
    
def deletecomment(request,id):
    comment = Comment.objects.get(id=id)
    postid = comment.post.id
    comment.delete()
    return post(request,postid)
    
def editpost(request,id):
    post = Post.objects.get(id=id)
    if request.method == 'POST':
        try:
            postname = request.POST['postname']
            content = request.POST['content']
            category = request.POST['category']
            
            post.postname = postname
            post.content = content
            post.category = category
            post.save()
        except:
            print("Error")
        return profile(request,request.user.id)
    
    return render(request,"postedit.html",{
        'post':post
    })
    
def deletepost(request,id):
    Post.objects.get(id=id).delete()
    return profile(request,request.user.id)


def contact_us(request):
    context={}
    if request.method == 'POST':
        name=request.POST.get('name')    
        email=request.POST.get('email')  
        subject=request.POST.get('subject')  
        message=request.POST.get('message')  

        obj = Contact(name=name,email=email,subject=subject,message=message)
        obj.save()
        context['message']=f"Dear {name}, Thanks for your time!"

    return render(request,"contact.html")

def blog_view(request):
    # Retrieve selected categories from the GET request
    selected_categories = request.GET.getlist('categories')
    
    # Filter posts based on selected categories or show all if no filter is applied
    if selected_categories:
        posts = Post.objects.filter(category__in=selected_categories)
    else:
        posts = Post.objects.all()

    context = {
        'recent_posts': posts,
        'selected_categories': selected_categories,  # Pass selected categories for retaining filter state
    }
    return render(request, 'blog.html', context)
