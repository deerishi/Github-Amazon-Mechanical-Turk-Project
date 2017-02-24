from __future__ import unicode_literals
from django.contrib.auth.models import User

from django.db import models

class Sentiment1(models.Model):
    id = models.BigIntegerField(primary_key=True)
    pull_request_id = models.BigIntegerField(blank=True, null=True)
    user_id = models.BigIntegerField(blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    github_comment_id = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'sentiments'

        

class UserProfile(models.Model):
    email=models.ForeignKey(User)
    sentenceToMark=models.IntegerField(default=2)
    
    @property
    def email_username(self):
        return self.email.username

class AnnotatedSentences(models.Model):
    comment_id=models.IntegerField(null=True, blank=True)
    owner=models.ForeignKey(User)
    body=models.TextField(blank=True, null=True)
    shows_solidarity = models.BigIntegerField(db_column='Shows_Solidarity', blank=True, null=True)  # Field name made lowercase.
    shows_tension_release = models.BigIntegerField(db_column='Shows_tension_release', blank=True, null=True)  # Field name made lowercase.
    agrees = models.BigIntegerField(db_column='Agrees', blank=True, null=True)  # Field name made lowercase.
    gives_suggestion = models.BigIntegerField(db_column='Gives_Suggestion', blank=True, null=True)  # Field name made lowercase.
    gives_opinion = models.BigIntegerField(db_column='Gives_opinion', blank=True, null=True)  # Field name made lowercase.
    gives_orientation = models.BigIntegerField(db_column='Gives_orientation', blank=True, null=True)  # Field name made lowercase.
    asks_for_orientation = models.BigIntegerField(db_column='Asks_for_orientation', blank=True, null=True)  # Field name made lowercase.
    asks_for_opinon = models.BigIntegerField(db_column='Asks_for_opinon', blank=True, null=True)  # Field name made lowercase.
    asks_for_suggestion = models.BigIntegerField(db_column='Asks_for_suggestion', blank=True, null=True)  # Field name made lowercase.
    disagrees = models.BigIntegerField(db_column='Disagrees', blank=True, null=True)  # Field name made lowercase.
    shows_tension = models.BigIntegerField(db_column='Shows_Tension', blank=True, null=True)  # Field name made lowercase.
    shows_antagnism = models.BigIntegerField(db_column='Shows_Antagnism', blank=True, null=True)  # Field name made lowercase.
    thanks = models.BigIntegerField(db_column='Thanks', blank=True, null=True)  # Field name made lowercase.
    sorry = models.BigIntegerField(db_column='Sorry', blank=True, null=True)  # Field name made lowercase.
    calm = models.BigIntegerField(db_column='Calm', blank=True, null=True)  # Field name made lowercase.
    nervous = models.BigIntegerField(db_column='Nervous', blank=True, null=True)  # Field name made lowercase.
    careless = models.BigIntegerField(db_column='Careless', blank=True, null=True)  # Field name made lowercase.
    cautious = models.BigIntegerField(db_column='Cautious', blank=True, null=True)  # Field name made lowercase.
    agressive = models.BigIntegerField(db_column='Agressive', blank=True, null=True)  # Field name made lowercase.
    defensive = models.BigIntegerField(db_column='Defensive', blank=True, null=True)  # Field name made lowercase.
    happy = models.BigIntegerField(db_column='Happy', blank=True, null=True)  # Field name made lowercase.
    angry = models.BigIntegerField(db_column='Angry', blank=True, null=True)  # Field name made lowercase.

class DisplayTableOfMarkedComments(models.Model):
    Person=models.ForeignKey(User)
    Comment=models.TextField()
    Marked=models.TextField()
    CommentId=models.IntegerField(default=0)
    

class HITTable(models.Model):
    person=models.ForeignKey(User)
    hitCode=models.BigIntegerField()
