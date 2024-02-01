import os
import requests
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aramgoproto.settings')
django.setup()

from matchhistory.models import Summoner, Match, Participant, MatchStats, Champion, Item
from django.utils import timezone

RIOT_API_KEY = 'RGAPI-584af21c-f54a-4dfc-807a-47cc336b8332'
REGION = 'na1'  # Example: 'na1' for North America


def fetch_summoner_info(summoner_name):
    url = f'https://{REGION}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}?api_key={RIOT_API_KEY}'
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching summoner info: Status code {response.status_code}, Response: {response.text}")
        return None


def fetch_aram_match_history(puuid):
    url = f'https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?queue=450&count=5&api_key={RIOT_API_KEY}'
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching ARAM match history: Status code {response.status_code}, Response: {response.text}")
        return None

def fetch_match_details(match_id):
    url = f'https://americas.api.riotgames.com/lol/match/v5/matches/{match_id}?api_key={RIOT_API_KEY}'
    response = requests.get(url)
    return response.json() if response.status_code == 200 else None





def populate_db(summoner_name):
    summoner_info = fetch_summoner_info(summoner_name)
    if not summoner_info:
        print(f"Error: Summoner '{summoner_name}' not found.")
        return

    

    summoner, _ = Summoner.objects.update_or_create(
        puuid=summoner_info["puuid"],
        defaults={
            "summoner_name": summoner_info["name"],
            "level": summoner_info["summonerLevel"],
            "profile_icon_id": summoner_info["profileIconId"],
            "icon_image_url": f"https://ddragon.leagueoflegends.com/cdn/13.5.1/img/profileicon/{summoner_info['profileIconId']}.png",
            
        }
    )

    match_history = fetch_aram_match_history(summoner_info["puuid"])
    if not match_history:
        print(f"Error: No ARAM match history found for summoner '{summoner_name}'.")
        return

    # LISTS OF A USERS MATCH ID
    for match_id in match_history:
        # Check if the match already exists in the database
        if Match.objects.filter(match_id=match_id).exists():
            print(f"Match {match_id} already exists in the database. Skipping.")
            continue

        match_details = fetch_match_details(match_id)

        #Creates match object for each match ID After fetching match detail
        match_obj, _ = Match.objects.get_or_create(
            match_id=match_details["metadata"]["matchId"],
            defaults={
                "timestamp": timezone.make_aware(timezone.datetime.fromtimestamp(match_details["info"]["gameCreation"] / 1000)),
                "queue_id": match_details["info"]["queueId"],
                "duration": match_details["info"]["gameDuration"],
                "version": match_details["info"]["gameVersion"],
                #ADD PATCH, ADD EPOCH UNIX TIMESTAMP FOR START
            }
        )
        
        #iterates over a list of particiapnts dictionary detials
        for participant_data in match_details["info"]["participants"]:
            stats = participant_data

            summoner, _ = Summoner.objects.update_or_create(
                puuid=participant_data["puuid"],
                defaults={
                    "summoner_name": participant_data["summonerName"],
                    "level": participant_data["summonerLevel"],
                    "profile_icon_id": participant_data["profileIcon"],
                    "icon_image_url": f"https://ddragon.leagueoflegends.com/cdn/13.5.1/img/profileicon/{participant_data['profileIcon']}.png",
                }
            )

            champion = Champion.objects.get(champion_id=participant_data["championId"])
            participant_obj, _ = Participant.objects.update_or_create(
                summoner=summoner,
                match=match_obj,
                defaults={
                    "team_id": participant_data["teamId"],
                    "champion": champion,
                }
            )

            
            match_stats_obj, _ = MatchStats.objects.update_or_create(
                participant=participant_obj,
                
                champion=champion,
                defaults={
                    "win": stats["win"],
                    "kills": stats["kills"],
                    "deaths": stats["deaths"],
                    "assists": stats["assists"],
                    "gold_earned": stats["goldEarned"],
                    "total_damage_dealt": stats["totalDamageDealt"],
                    "total_damage_taken": stats["totalDamageTaken"],
                    "creep_score": stats["totalMinionsKilled"],
                    }
                )
            
            

        for i in range(1, 7):
            item_id = stats.get(f"item{i - 1}", None)
            if item_id is not None:
                item_obj, created = Item.objects.get_or_create(item_id=item_id)
                match_stats_obj.items.add(item_obj)

        print(f"Processed match: {match_obj.match_id}")




