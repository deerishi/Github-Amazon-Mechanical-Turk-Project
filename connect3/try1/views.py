from try1.models import Sentiment1,  UserProfile, AnnotatedSentences
from try1.serializers import Sentiment1Serializer, UserSerializer
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework import permissions
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from try1.forms import RegistrationForm
from django.contrib.auth import authenticate, login


ipaList=['Shows_Solidarity',' Shows_tension_release	','Agrees',' Gives_Suggestion',' Gives_opinion','Gives_orientation','Asks_for_orientation','    Asks_for_opinon','Asks_for_suggestion','Disagrees','Shows_Tension','Shows_Antagnism	']
emotions=['Thanks','Sorry','Calm','Nervous','Careless','Cautious','Agressive','Defensive','Happy','Angry'] 
class Sentiment1List(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, format=None):
        #print('request.sessions is ', request.session.keys())
        sentiments = Sentiment1.objects.all()
        serializer = Sentiment1Serializer(sentiments, many=True)
        return Response(serializer.data)

class UserList(APIView):
    
    def get(self, request, format=None):
        users=User.objects.all()
        serializer=UserSerializer(users, many=True)
        return Response(serializer.data)

@login_required
def main(request):
    user=request.user
    print('The user is ', user.email)
    
    return HttpResponse('hello world')

@login_required
def displayComment(request, comment_id):
    user=request.user
    numMarked=len(AnnotatedSentences.objects.filter(owner=user))
    if int(comment_id)<2:
        comment=get_object_or_404(Sentiment1, id=2)
        return render(request, 'try1/detail.html', {'comment':comment, 'ipaList':ipaList, 'emotions':emotions, 'user':user.email, 'prevComment':2, 'numMarked':numMarked})
    
    if int(comment_id)>5:
        return render(request, 'try1/finish.html',{'prevComment':int(comment_id-1)})  
    print('the user is ', user)
    up=get_object_or_404(UserProfile, email=user)
    print('comment_id is ', comment_id, ' and up.sentenceToMark is ', up.sentenceToMark)
    #assert int(up.sentenceToMark)==int(comment_id)
    comment=get_object_or_404(Sentiment1, id=comment_id)
    numMarked=len(AnnotatedSentences.objects.filter(owner=user))
    #body=comment.body
    #print('Comment is ', body)
    prevComment=int(comment_id)-1
    return render(request, 'try1/detail.html', {'comment':comment, 'ipaList':ipaList, 'emotions':emotions, 'user':user.email, 'prevComment':prevComment, 'numMarked':numMarked})

@login_required 
def dummy(request):
    user=request.user
    up=get_object_or_404(UserProfile, email=user)
    return HttpResponseRedirect(reverse('try1:dpc', args=(up.sentenceToMark,)))
    

    
@login_required
def processMarkedSentence(request, comment_id):
    print('In processMarkedSentence with comment_id', comment_id, ' and user is ', request.user)
    if request.method=='POST':
        user=request.user
        comment=request.POST['comment']
        print('The edited commment is ', comment)
        up=UserProfile.objects.get(email=user)
        up.sentenceToMark=int(comment_id) +1
        up.save()
        ipaCheckBoxes=request.POST.getlist('ipa')
        emotionsCheckBoxes=request.POST.getlist('emotion')
        ipaCheckBoxes=[int(x)-1 for x in ipaCheckBoxes]
        emotionsCheckBoxes=[int(x)-1 for x in emotionsCheckBoxes]
        ipaVals=[0]*12
        emotionsVal=[0]*10
        for i in ipaCheckBoxes:
            ipaVals[i]=1
        for i in emotionsCheckBoxes:
            emotionsVal[i]=1
        allCheckBoxes=ipaVals+emotionsVal
        #shows_solidarity =shows_tension_release =agrees =gives_suggestion =gives_opinion =gives_orientation =asks_for_orientation =asks_for_opinon =asks_for_suggestion =disagrees =shows_tension =shows_antagnism =thanks =sorry =calm =nervous =careless =cautious =agressive =defensive =happy =angry = 0
        shows_solidarity ,shows_tension_release ,agrees ,gives_suggestion ,gives_opinion ,gives_orientation ,asks_for_orientation ,asks_for_opinon ,asks_for_suggestion ,disagrees ,shows_tension ,shows_antagnism=tuple(ipaVals)
        thanks ,sorry ,calm ,nervous ,careless ,cautious ,agressive ,defensive ,happy ,angry =tuple(emotionsVal)
        print('tuple is ', allCheckBoxes)
        AnnotatedSentences.objects.filter(owner=user, comment_id=comment_id).delete()
        annotated=AnnotatedSentences.objects.create(comment_id=comment_id, owner=user, body=comment, shows_solidarity =shows_solidarity,shows_tension_release =shows_tension_release,agrees =agrees,gives_suggestion =gives_suggestion,gives_opinion =gives_opinion,gives_orientation=gives_orientation ,asks_for_orientation=asks_for_orientation,asks_for_opinon=asks_for_opinon,asks_for_suggestion =asks_for_suggestion,disagrees =disagrees,shows_tension=shows_tension ,shows_antagnism=shows_antagnism, thanks=thanks ,sorry=sorry ,calm=calm ,nervous=nervous ,careless=careless ,cautious=cautious ,agressive =agressive,defensive=defensive ,happy=happy ,angry=angry)
        annotated.save()
        return HttpResponseRedirect(reverse('try1:dpc', args=(up.sentenceToMark,)))
    else:
        return HttpResponseRedirect(reverse('try1:dpc', args=(comment_id,)))
        


def register(request):
    if request.user.is_authenticated():
        return  HttpResponseRedirect(reverse('try1:dummy'))
    elif request.method == 'POST':
        form = RegistrationForm(data=request.POST )
        print('The POST data is ', request.POST)
        print('form is ', form)
        if form.is_valid():
            print('The form is valid' )
            username=form.cleaned_data['username']
            print('The username is ',username)
            email=form.cleaned_data['email']
            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            password1=form.cleaned_data['password1']
            u=User.objects.create_user(username=username,email=email,  first_name=first_name, last_name=last_name, password=password1)
            UserProfile.objects.create(email=u, sentenceToMark=2)
            messages.info(request, "Thanks for registering. You are now logged in.")
            new_user = authenticate(username=username, email=email,password=password1)
            login(request, new_user)
            return HttpResponseRedirect(reverse('try1:dummy'))
        else:
            return render(request, 'try1/register.html',{'form':form})     
    else:
        form = RegistrationForm()
        return render(request, 'try1/register.html',{'form':form}) 

def homePage(request):
    if request.user.is_authenticated():
        return  HttpResponseRedirect(reverse('try1:dummy'))
    else:
        return render(request, 'try1/homePage.html') 
