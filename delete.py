import os
import requests
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aramgoproto.settings')
django.setup()

from matchhistory.models import Summoner, Match, Participant, MatchStats, Champion, Item
from django.utils import timezone

def delete_all_data():
    MatchStats.objects.all().delete()
    Participant.objects.all().delete()
    Item.objects.all().delete()
    Champion.objects.all().delete()
    Match.objects.all().delete()
    Summoner.objects.all().delete()

if __name__ == "__main__":
    delete_all_data()