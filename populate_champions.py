import os
import requests
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aramgoproto.settings')

import django
django.setup()

from matchhistory.models import Champion

RIOT_API_KEY = 'RGAPI-28c9c5b1-5ec6-4d05-9c94-829504571fb3'

def fetch_champions_data():
    url = f"http://ddragon.leagueoflegends.com/cdn/13.7.1/data/en_US/champion.json" ##UPDATE THIS EVERY PATCH
    response = requests.get(url)
    data = response.json()
    print()
    return data['data']
    

def populate_champions():
    champions_data = fetch_champions_data()
    for champ_key, champ_data in champions_data.items():
        champion_id = champ_data['key']
        name = champ_data['name']
        title = champ_data['title']
        image_url = f"https://ddragon.leagueoflegends.com/cdn/13.5.1/img/champion/{champ_data['image']['full']}"
        tags = ', '.join(champ_data['tags'])
        
        champion, created = Champion.objects.update_or_create(
            champion_id=champion_id,
            defaults={
                'name': name,
                'title': title,
                'image_url': image_url,
                'tags': tags
            }
        )
        
        if created:
            print(f"Added {name} to the database.")
        else:
            print(f"Updated {name} in the database.")


if __name__ == '__main__':
    print("Starting champion population script...")
    populate_champions()
    
