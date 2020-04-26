from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save
from django.shortcuts import reverse
from django.utils import timezone
from django.utils.text import slugify


class PostManager(models.Manager):
    def active(self, *args, **kwargs):
        return super(PostManager,self).filter(draft=False).filter(publish__lte=timezone.now())

def upload_location(instance,filename):
    return "%s/%s" %(instance.id, filename)

class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    content = models.TextField()
    image = models.ImageField(upload_to=upload_location, null=True, blank=True, height_field='height_field', width_field='width_field')
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    slug = models.SlugField(unique=True)
    draft = models.BooleanField(default=False) #added in ch-35
    publish = models.DateTimeField() #added in ch-35

    objects = PostManager()


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('posts:post_details', kwargs={'slug':self.slug}) #changed from pk to slug for slug field
        # return "post/details/%s/" %(self.pk)

    
    # class Meta:
    #     ordering = ['-timestamp', '-updated']


def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    print(slug)
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug=slug).order_by("-id")
    # print('test1- ',qs.first().id)
    exists = qs.exists()
    if exists:
        print('2nd - ',slug)
        new_slug = "%s-%s" %(slug, qs.last().id)
        return create_slug(instance,new_slug=new_slug)
    return slug



def pre_save_post_reciever(sender,instance,*args,**kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


pre_save.connect(pre_save_post_reciever,sender=Post)