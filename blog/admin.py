from django.contrib import admin
from .models import Post, Profile,Comment
# Register your models here.
class PostAdmin(admin.ModelAdmin):
	list_display=('title', 'slug', 'body', 'author', 'status')
	list_filter=('status', 'created', 'updated')
	search_fields=('author__username', 'title')
	prepopulated_fields={'slug':('title',)}
	list_editable=('status',)
	date_hierarchy=('created')
	class Meta:
		model=Post


admin.site.register(Post, PostAdmin)

class ProfileAdmin(admin.ModelAdmin):
	list_display=('user', 'dob', 'photo')


admin.site.register(Profile, ProfileAdmin)

# class ImageAdmin(admin.ModelAdmin):
# 	list_display=('post', 'image')

# admin.site.register(Images, ImageAdmin)


class CommentAdmin(admin.ModelAdmin):
	list_display=['__str__','content']

admin.site.register(Comment, CommentAdmin)