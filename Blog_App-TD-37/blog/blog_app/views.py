from urllib.parse import quote_plus
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseRedirect,Http404
from django.shortcuts import render,get_object_or_404,redirect
from django.utils import timezone


from .models import Post
from .forms import PostForm

def post_list(request):
    # the below line is alternative for model Manager but not suitable at every time
    # queryset = Post.objects.filter(draft=False).filter(publish__lte=timezone.now()) #all().order_by('-id') #.order_by('-timestamp')
    today = timezone.now()
    queryset = Post.objects.active() # added in ch-36
    if request.user.is_staff or request.user.is_superuser: # added in ch-36
        queryset = Post.objects.all() # added in ch-36

    query = request.GET.get('q')
    if query:
        queryset = Post.objects.filter(
            Q(title__icontains=query)|
            Q(content__icontains=query)|
            Q(user__first_name__icontains=query)|
            Q(user__last_name__icontains=query)).filter(draft=False).distinct()

    paginator = Paginator(queryset, 5) # Show 5 contents per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'object_list' : page_obj,
        'page_obj': page_obj,
        'today':today
    }
    return render(request,'blog_app/post_list.html',context)


def post_details(request,slug = None, pk=None):
    # instance = get_object_or_404(Post,pk=pk)
    instance = get_object_or_404(Post,slug=slug)
    if instance.draft or instance.publish > timezone.now():
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404
    share_string = quote_plus(instance.content)
    context = {
        'obj_details':instance,
        'share_string':share_string
    }
    return render(request,'blog_app/post_details.html',context)


def post_create(request):
    # if not request.user.is_staff or not request.user.is_supperuser:
        # raise Http404

    if not request.user.is_authenticated:
        raise Http404

    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        messages.success(request,'Succesfuly created')
        return HttpResponseRedirect(instance.get_absolute_url())
    # else:
    #     messages.error(request,'Not succesfully created')    
    context = {
        'form':form
    }
    return render(request, 'blog_app/post_create.html',context)



def post_update(request, id=None):
    # if not request.user.is_staff or not request.user.is_supperuser:
    #     raise Http404

    if not request.user.is_authenticated:
        raise Http404
    
    instance = get_object_or_404(Post,id=id) #This instance should pass through form to update
    form = PostForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        messages.success(request,'<a href="">Item</a> Succesfuly changed',extra_tags='html_safe') #extra tag is used to create different classes in html
        return HttpResponseRedirect(instance.get_absolute_url()) #redirecting the url is must and should once after saved the form
    # else:
    #     messages.error(request,'Not succesfully changed')

    context = {
        'form':form
    }
    return render(request, 'blog_app/post_create.html',context)


def post_delete(request,id=None):
    if not request.user.is_staff or not request.user.is_supperuser:
        raise Http404
    instance = get_object_or_404(Post,id=id)
    instance.delete()
    messages.success(request, "Succesfully deleted")
    return redirect('blog_app:post_list')



