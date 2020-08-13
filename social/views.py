from django.http import HttpResponse,HttpResponseNotFound
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages

from . import models

def messages_view(request):
    """Private Page Only an Authorized User Can View, renders messages page
       Displays all posts and friends, also allows user to make new posts and like posts
    Parameters
    ---------
      request: (HttpRequest) - should contain an authorized user
    Returns
    --------
      out: (HttpResponse) - if user is authenticated, will render private.djhtml
    """
    if request.user.is_authenticated:
        user_info = models.UserInfo.objects.get(user=request.user)
        # TODO Objective 9: query for posts (HINT only return posts needed to be displayed)
        allPosts=models.Post.objects.all()
        allPosts=list(allPosts.order_by('timestamp'))
        allPosts=allPosts[::-1]
        #print(allPosts)
        posts = []
        for i in allPosts:
            posts+=[i]
        posts=posts[0:request.session.get('postCounter')]
        # TODO Objective 10: check if user has like post, attach as a new attribute to each post
        totalPosts=models.Post.objects.all()
        likePosts=models.Post.objects.filter(likes=user_info)
      #  print(likePosts)
        context = { 'user_info' : user_info
                  , 'posts' : posts, 'likePosts' : likePosts}
        return render(request,'messages.djhtml',context)

    request.session['failed'] = True
    return redirect('login:login_view')

def account_view(request):
    """Private Page Only an Authorized User Can View, allows user to update
       their account information (i.e UserInfo fields), including changing
       their password
    Parameters
    ---------
      request: (HttpRequest) should be either a GET or POST
    Returns
    --------
      out: (HttpResponse)
                 GET - if user is authenticated, will render account.djhtml
                 POST - handle form submissions for changing password, or User Info
                        (if handled in this view)
    """
    #if request.user.is_authenticated:
    if not request.user.is_authenticated:
        return redirect('login:login_view')

    if request.user.is_authenticated:
         user_info = models.UserInfo.objects.get(user=request.user)
         if request.method == 'POST':
            form = PasswordChangeForm(user_info.user, request.POST)
            if form.is_valid():
                user= form.save()
                update_session_auth_hash(request, user)
                return redirect('login:login_view')

            newInterest = request.POST.get('interest')
            if newInterest:
             if newInterest:
                userInterest = models.Interest(label=newInterest)
                userInterest.save()
                user_info.interests.add(userInterest)
                user_info.save()
                return redirect('social:account_view')

            else:
             user_info.birthday=request.POST.get('birthday',user_info.birthday)
             user_info.location=request.POST.get('location', user_info.location)
             user_info.employment=request.POST.get('employment', user_info.employment)

            user_info.save()
            return redirect('social:account_view')

         else:
            form = PasswordChangeForm(request.user)
    user_info = models.UserInfo.objects.get(user=request.user)
    context = { 'user_info' : user_info, 'form' : form}
    return render(request,'account.djhtml',context)

    request.session['failed'] = True
    return redirect('login:login_view')

def people_view(request):
    """Private Page Only an Authorized User Can View, renders people page
       Displays all users who are not friends of the current user and friend requests
    Parameters
    ---------
      request: (HttpRequest) - should contain an authorized user
    Returns
    --------
      out: (HttpResponse) - if user is authenticated, will render people.djhtml
    """
    if request.user.is_authenticated:
        user_info = models.UserInfo.objects.get(user=request.user)
        # TODO Objective 4: create a list of all users who aren't friends to the current user (and limit size)
        fList=user_info.friends.all()
        accounts=models.UserInfo.objects.exclude(user=request.user)
        all_people = []
        for i in accounts:
            if i not in fList:
                  all_people+=[i]
                 # print(i)
        #request.session['displayCounter']=1
        # TODO Objective 5: create a list of all friend requests to current user
        x=list(models.FriendRequest.objects.filter(to_user=user_info))
        friend_requests = []
        for i in x:
            if i not in friend_requests:
                 friend_requests+=[i.from_user.user.username]
        b=list(models.FriendRequest.objects.filter(from_user=user_info))
        sent_requests = []
        for a in b:
            if a not in sent_requests:
                 sent_requests+=[a.to_user.user.username]
        #print(sent_requests)
        all_people=all_people[0:request.session.get('displayCounter')]
        context = { 'user_info' : user_info,
                    'all_people' : all_people,
                    'friend_requests' : friend_requests,
                     'sent_requests' : sent_requests }
        #return redirect('social:people_view')
        return render(request,'people.djhtml',context)

    request.session['failed'] = True
    return redirect('login:login_view')

def like_view(request):
    '''Handles POST Request recieved from clicking Like button in messages.djhtml,
       sent by messages.js, by updating the corrresponding entry in the Post Model
       by adding user to its likes field
    Parameters
	----------
	  request : (HttpRequest) - should contain json data with attribute postID,
                                a string of format post-n where n is an id in the
                                Post model
	Returns
	-------
   	  out : (HttpResponse) - queries the Post model for the corresponding postID, and
                             adds the current user to the likes attribute, then returns
                             an empty HttpResponse, 404 if any error occurs
    '''
    postIDReq = request.POST.get('postID')
    #print("postIDReq")
    if postIDReq is not None:
        # remove 'post-' from postID and convert to int
        # TODO Objective 10: parse post id from postIDReq
        postID=int(postIDReq[5:])
        #print(postID)
        #postID = 0
        x=list(models.Post.objects.all())
        lenX=len(x)-1
        postO=x[lenX-postID]
        #print(postO.content)

        if request.user.is_authenticated:
            # TODO Objective 10: update Post model entry to add user to likes field
            user_info = models.UserInfo.objects.get(user=request.user)
            postO.likes.add(user_info)
            # return status='success'
            return HttpResponse()
        else:
            return redirect('login:login_view')

    return HttpResponseNotFound('like_view called without postID in POST')

def post_submit_view(request):
    '''Handles POST Request recieved from submitting a post in messages.djhtml by adding an entry
       to the Post Model
    Parameters
	----------
	  request : (HttpRequest) - should contain json data with attribute postContent, a string of content
	Returns
	-------
   	  out : (HttpResponse) - after adding a new entry to the POST model, returns an empty HttpResponse,
                             or 404 if any error occurs
    '''
    postContent = request.POST.get('postContent')
    #print(postContent)
    if postContent is not None:
        if request.user.is_authenticated:
            user_info = models.UserInfo.objects.get(user=request.user)
            # TODO Objective 8: Add a new entry to the Post model
            apost= models.Post(owner=user_info)
            apost.save()
            apost.content=postContent
            apost.save()
            # return status='success'
         #   redirect('social:messages_view')
            return HttpResponse()
        else:
            return redirect('login:login_view')

    return HttpResponseNotFound('post_submit_view called without postContent in POST')

def more_post_view(request):
    '''Handles POST Request requesting to increase the amount of Post's displayed in messages.djhtml
    Parameters
	----------
	  request : (HttpRequest) - should be an empty POST
	Returns
	-------
   	  out : (HttpResponse) - should return an empty HttpResponse after updating hte num_posts sessions variable
    '''
    if request.user.is_authenticated:
        # update the # of posts dispalyed
        uList = models.Post.objects.all()
        i = int(request.session.get('postCounter',0))

        if len(uList)>=i:
              request.session['postCounter']=i+2
        # TODO Objective 9: update how many posts are displayed/returned by messages_view

        # return status='success'
        return HttpResponse()

    return redirect('login:login_view')

def more_ppl_view(request):
    '''Handles POST Request requesting to increase the amount of People displayed in people.djhtml
    Parameters
	----------
	  request : (HttpRequest) - should be an empty POST
	Returns
	-------
   	  out : (HttpResponse) - should return an empty HttpResponse after updating the num ppl sessions variable
    '''
    if request.user.is_authenticated:
        # update the # of people dispalyed
        uList = models.UserInfo.objects.exclude(user=request.user)
        i = int(request.session.get('displayCounter',0))
        # TODO Objective 4: increment session variable for keeping track of num ppl displayed
        if len(uList)>=request.session.get('displayCounter',0):
              request.session['displayCounter']=i+1
       # print(
        # return status='success'
        return HttpResponse()

    return redirect('login:login_view')

def friend_request_view(request):
    '''Handles POST Request recieved from clicking Friend Request button in people.djhtml,
       sent by people.js, by adding an entry to the FriendRequest Model
    Parameters
	----------
	  request : (HttpRequest) - should contain json data with attribute frID,
                                a string of format fr-name where name is a valid username
	Returns
	-------
   	  out : (HttpResponse) - adds an etnry to the FriendRequest Model, then returns
                             an empty HttpResponse, 404 if POST data doesn't contain frID
    '''
    frID = request.POST.get('frID')
   # print(frID)
    if frID is not None:
        # remove 'fr-' from frID
        username = frID[3:]
        if request.user.is_authenticated:
            x=models.UserInfo.objects.get(user_id=username)
            user= models.UserInfo.objects.get(user=request.user)
            newEntry= models.FriendRequest(to_user=x,from_user=user)
           # print(models.FriendRequest.objects.all())
            newEntry.save()
            # TODO Objective 5: add new entry to FriendRequest
            # return status='success'
            return HttpResponse()
        else:
            return redirect('login:login_view')

    return HttpResponseNotFound('friend_request_view called without frID in POST')

def accept_decline_view(request):
    '''Handles POST Request recieved from accepting or declining a friend request in people.djhtml,
       sent by people.js, deletes corresponding FriendRequest entry and adds to users friends relation
       if accepted
    Parameters
	----------
	  request : (HttpRequest) - should contain json data with attribute decision,
                                a string of format A-name or D-name where name is
                                a valid username (the user who sent the request)
	Returns
	-------
   	  out : (HttpResponse) - deletes entry to FriendRequest table, appends friends in UserInfo Models,
                             then returns an empty HttpResponse, 404 if POST data doesn't contain decision
    '''
    data = request.POST.get('decision')
    #print(data)
    if data is not None:
        # TODO Objective 6: parse decision from data
        d=data[0:1]
        username=data[2:]

        if request.user.is_authenticated:
            x=models.UserInfo.objects.get(user__username=username)
            user_info = models.UserInfo.objects.get(user=request.user)
            if d=='A':
                user_info.friends.add(x)
                accept= models.FriendRequest.objects.get(to_user=user_info,from_user=x)
                accept.delete()
                people_view(request)
            elif d=='D':
                 decline= models.FriendRequest.objects.get(to_user=user_info,from_user=x)
                 decline.delete()
            # TODO Objective 6: delete FriendRequest entry and update friends in both Users

            # return status='success'

            return HttpResponse()
        else:
            return redirect('login:login_view')
    return HttpResponseNotFound('accept-decline-view called without decision in POST')
