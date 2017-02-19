from rest_framework import serializers
from try1.models import Sentiment1,  AnnotatedSentences
from django.contrib.auth.models import User

class Sentiment1Serializer(serializers.ModelSerializer):
    class Meta:
        model = Sentiment1
        fields = ('id', 'body')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('id', 'email', 'first_name', 'last_name')
        

class AnnotatedSentencesSerilzer(serializers.ModelSerializer):
    class Meta:
        model=AnnotatedSentences
        fields = ('id', 'body','markerid' ,'shows_solidarity', 'shows_tension_release', 'agrees', 'gives_suggestion', 'gives_opinion', 'gives_orientation', 'asks_for_orientation', 'asks_for_opinon', 'asks_for_suggestion', 'disagrees', 'shows_tension', 'shows_antagnism', 'thanks', 'sorry', 'calm', 'nervous', 'careless', 'cautious', 'agressive', 'defensive', 'happy', 'angry')
