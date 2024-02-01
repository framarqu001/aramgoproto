from django.db import models

class Summoner(models.Model):
    puuid = models.CharField(max_length=255, primary_key=True, unique=True)
    summoner_name = models.CharField(max_length=255, unique=True)
    level = models.IntegerField()
    profile_icon_id = models.IntegerField()
    icon_image_url = models.URLField(null=True, blank=True)

class Match(models.Model):
    match_id = models.CharField(max_length=255, primary_key=True, unique=True)
    timestamp = models.DateTimeField()
    queue_id = models.IntegerField()
    duration = models.IntegerField()
    version = models.CharField(max_length=255)

class Champion(models.Model):
    champion_id = models.CharField(max_length=255, primary_key=True, unique=True)
    name = models.CharField(max_length=255, unique=True)
    title = models.CharField(max_length=255)
    image_url = models.URLField(null=True, blank=True)
    tags = models.CharField(max_length=255)

class Item(models.Model):
    item_id = models.CharField(max_length=255, primary_key=True, unique=True)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    cost = models.IntegerField(null=True)
    image_url = models.URLField(null=True, blank=True)

class Participant(models.Model):
    participant_id = models.AutoField(primary_key=True)
    summoner = models.ForeignKey(Summoner, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    team_id = models.IntegerField()
    champion = models.ForeignKey(Champion, on_delete=models.CASCADE)

class MatchStats(models.Model):
    participant = models.OneToOneField(Participant, on_delete=models.CASCADE, primary_key=True)
    win = models.BooleanField()
    kills = models.IntegerField()
    deaths = models.IntegerField()
    assists = models.IntegerField()
    gold_earned = models.IntegerField()
    total_damage_dealt = models.IntegerField()
    total_damage_taken = models.IntegerField()
    creep_score = models.IntegerField()
    items = models.ManyToManyField(Item)
    champion = models.ForeignKey(Champion, on_delete=models.CASCADE)

