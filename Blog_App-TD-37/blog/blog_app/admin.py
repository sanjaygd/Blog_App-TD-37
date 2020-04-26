from django.contrib import admin
from .models import Post

#django model admin options is referece for more details.
class PostModelAdmin(admin.ModelAdmin):
    list_display = ["title","timestamp","content", "updated"] #To display fields in admin panel
    list_display_links = ['updated'] # use to display as link
    list_filter = ['content','timestamp'] #used for side filter
    search_fields = ['content'] #We can search information in particular or in multiple fields
    list_editable = ['title'] # To edit the field
    class Meta:
        model = Post


admin.site.register(Post,PostModelAdmin)
