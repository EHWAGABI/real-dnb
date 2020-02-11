from django.shortcuts import render, get_object_or_404, redirect
from .models import Culture, Comment
from bookmap.models import BookStore
from .forms import CommentForm, CultureForm
from el_pagination.views import AjaxListView
from django.db.models import Q
import os
import simplejson
# Create your views here.

def board(request):
    cultures = Culture.objects.order_by('-write_date')
    result = 'total'

    bookstores = BookStore.objects.all()
    insta = []
    for a in bookstores:
        if a.insta != 'nan':
            insta.append(a.insta)
        else: pass
    instalist = simplejson.dumps(insta)
    return render(request, 'board.html', {'cultures':cultures, 'result':result,'instalist':instalist,'stores':bookstores,})

def entry_index(request, template='others/board.html'):
    context = {
        'cultures' : Culture.objects.all().order_by('-write_date'),
    }
    return render(request, template, context)

def detail(request, culture_id):
    culture_detail = get_object_or_404(Culture, pk=culture_id)
    comments = culture_detail.comment_set.all().order_by('-created_at')
    if request.user.is_authenticated:
        form = CommentForm()
        return render(request, 'culturedetail.html', {'comments':comments,'culture':culture_detail, 'form':form})
    else:
        return render(request,'culturedetail.html', {'comments':comments,'culture' : culture_detail})
    

def guide(request):
    return render(request,'guide.html')

def commentcreate(request, culture_id):
    culture = get_object_or_404(Culture, pk=culture_id)
    if request.method=='POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.culture = culture
            comment.user = request.user
            comment.save()
            return redirect('culturedetail', culture_id=culture.pk)
        else:
            redirect('board')
    else:
        pass
    
def commentdelete(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    comment.delete()
    return redirect('culturedetail', culture_id=comment.culture.pk)

def new(request):
    return render(request, 'boardnew.html')

def boardcreate(request):
    if request.method=='POST':
        form = CultureForm(request.POST, request.FILES)
        storename = request.POST['storename']
        bookstore = BookStore.objects.get(name=storename)
        if form.is_valid(): 
            post = form.save(commit=False)
            post.store = bookstore
            post.save()
            return redirect('culturedetail', culture_id=post.pk)
        else:
            return redirect('board')
    else:
        form = CultureForm()
        storename = BookStore.objects.get(boss=request.user)
        return render(request, 'boardnew.html', {'form':form, 'storename':storename})


def boardsearch(request):
    cultures = Culture.objects.order_by('-write_date')  
    query = request.GET.get('query','')
    if query:
        result = request.GET.get('searchtype','')
        if result == 'title':
            cultures = Culture.objects.filter(title__contains=query).order_by('-write_date')
        elif result == 'store':
            stores = BookStore.objects.filter(name__contains=query)
            q = Q()
            for i in stores:
                q.add(Q(store=i), q.OR)
            cultures = Culture.objects.filter(q).order_by('-write_date')
    result = 'total'
    return render(request, 'board.html', {'cultures':cultures, 'result':result})

def boardclass(request):
    result = request.GET.get('class','')
    cultures = Culture.objects.order_by('-write_date')
    if result == 'total':
        cultures = Culture.objects.order_by('-write_date')
    elif result == 'concert':
        cultures = Culture.objects.filter(group='CO').order_by('-write_date')
    elif result == 'oneday':
        cultures = Culture.objects.filter(group='ON').order_by('-write_date')
    elif result == 'club':
        cultures = Culture.objects.filter(group='CL').order_by('-write_date')
    elif result == 'movie':
        cultures = Culture.objects.filter(group='MO').order_by('-write_date')
    elif result == 'etc':
        cultures = Culture.objects.filter(group='ET').order_by('-write_date')
    return render(request, 'board.html', {'cultures':cultures, 'result':result})


def boardupdate(request, culture_id):
    culture = get_object_or_404(Culture, pk = culture_id)
    if culture.picture:
        pic=culture.picture.path
    else:
        pic=None
    if request.method == 'POST':
        form = CultureForm(request.POST, request.FILES, instance=culture)
        if request.FILES and pic:
            os.remove(pic)
        storename = request.POST['storename']
        bookstore = BookStore.objects.get(name=storename)
        if form.is_valid(): 
            post = form.save(commit=False)
            post.store = bookstore
            post.save()
            return redirect('culturedetail', culture_id=post.pk)
    else:
        form = CultureForm(instance=culture)
        storename = BookStore.objects.get(boss=request.user)

        return render(request, 'boardnew.html', {'form':form, 'storename':storename})

def boarddelete(request, culture_id):
    post = get_object_or_404(Culture, pk = culture_id)
    if post.picture:
        os.remove(post.picture.path)
    post.delete()
    return redirect('board')