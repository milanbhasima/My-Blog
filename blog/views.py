from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, Http404
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post,Profile,Comment
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import *
from django.contrib.auth import authenticate, login, logout
# from django.template.loader import render_to_string
# from django.forms import modelformset_factory
# Create your views here.
def post_list(request):
	post_list=Post.published.all().order_by('-id')
	query=request.GET.get('q')
	print(query)
	if query:
		post_list=Post.published.filter(
			Q(title__icontains=query)|
			Q(body__icontains=query)|
			Q(author__username=query)
			).distinct()
	paginator = Paginator(post_list, 4)
	page=request.GET.get('page')
	try:
		posts = paginator.page(page)
	except PageNotAnInteger:
		posts = paginator.page(1)
	except EmptyPage:
		posts = paginator.page(paginator.num_pages)

	context={
		'posts':posts,
	}
	return render(request,'blog/post_list.html',context)


def post_detail(request, id=None):
	post=get_object_or_404(Post, id=id)
	comments=Comment.objects.filter(post=post, reply=None).order_by('-id')
	is_liked=False
	# print(post.likes)
	# if post.likes.filter(id=request.user.id).exists():
	if request.user in post.likes.all():	
		is_liked=True

	form=CommentForm(request.POST or None)

	if form.is_valid():
		reply_id=request.POST.get('comment_id')
		comment_qs=None
		if reply_id:
			comment_qs=Comment.objects.get(id=reply_id)
		comment=form.save(commit=False)
		comment.post=post
		comment.reply=comment_qs
		comment.user=request.user
		comment.save()
		return redirect(post.get_absolute_url())
	context={
		'post':post,
		'is_liked':is_liked,
		'comments':comments,
		'form':form,
	}
	return render(request,'blog/post_detail.html',context)

def like_post(request):
	post=get_object_or_404(Post, id=request.POST.get('post_id'))
	if post.likes.filter(id=request.user.id).exists():
		post.likes.remove(request.user)
		is_liked=False
	else:
		post.likes.add(request.user)
		is_liked=True
	return redirect(post.get_absolute_url())


@login_required
def post_create(request):
	# ImageFormset=modelformset_factory(Images, fields=('image',), extra=4)
	form=PostCreateForm(request.POST or None, request.FILES or None)
	# formset=ImageFormset(request.POST or None, request.FILES or None)
	if form.is_valid():
		post=form.save(commit=False)
		post.author=request.user
		post.save()
		messages.success(request, 'Post has been successfully created.')
		
		# for f in formset:
		# 	try:
		# 		photo=Images(post=post,image=f.cleaned_data['image'])
		# 		photo.save()
				
		# 	except Exception as e:
		# 		break
		return redirect('blog:post-list')
	context={
		'form':form,
		# 'formset':formset,
	}
	return render(request, 'blog/post_create.html',context)


@login_required
def post_update(request, id):
	post=get_object_or_404(Post, id=id)
	# ImageFormset=modelformset_factory(Images, fields=('image',), extra=4)
	if post.author != request.user:
		raise Http404()
	form=PostEditForm(request.POST or None, request.FILES or None, instance=post)
	# formset=ImageFormset(request.POST or None, request.FILES or None)
	if form.is_valid():
		form.save()
		messages.info(request, 'Post has been Updated successfully.')
		return redirect(post.get_absolute_url())
	context={
		'form':form,
		'post':post,
		# 'formset':formset,
	}
	return render(request, 'blog/post_edit.html', context)

@login_required
def post_delete(request, id):
	post=get_object_or_404(Post, id=id )
	if post.author != request.user:
		raise Http404()
	if request.method=='POST':
		post.delete()
		messages.warning(request, 'Post has been deleted.')
		return redirect('blog:post-list')

	context={
		'object':post,
	}
	return render(request, 'blog/post_delete.html', context)

def user_login(request):
	form=UserLoginForm(request.POST or None)
	if form.is_valid():
		username=form.cleaned_data.get('username')
		password=form.cleaned_data.get('password')
		user=authenticate(username=username, password=password)
		if user:
			if user.is_active:
				login(request, user)
				return redirect('blog:post-list')
			else:
				return HttpResponse('user is not active')
		else:
			return HttpResponse('User is None')

	context={
		'form':form,
	}
	return render(request,'registration/login.html', context)

def user_logout(request):
	logout(request)
	return redirect('user-login')

def user_register(request):
	form=UserRegistrationForm(request.POST or None)
	if form.is_valid():
		user=form.save(commit=False)
		user.set_password(form.cleaned_data['password'])
		user.save()
		return redirect('blog:post-list')
	context={
		'form':form,
	}
	return render(request, 'registration/register.html',context)

@login_required
def user_profile(request):
	user=request.user
	u_form=UserUpdateForm(request.POST or None, instance=user)
	p_form=ProfileUpdateForm(request.POST or None, request.FILES or None, instance=user.profile)
	if u_form.is_valid() and p_form.is_valid():
		u_form.save()
		p_form.save()
		messages.success(request, 'your account has been Updated now.')
		return redirect('blog:post-list')
	context={
		'user':user,
		'u_form':u_form,
		'p_form':p_form,
	}
	return render(request, 'blog/profile.html', context)


def about(request):
	return render(request,'blog/about.html')