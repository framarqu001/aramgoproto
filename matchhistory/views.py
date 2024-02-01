from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Summoner, Match, Participant
from django.http import JsonResponse
from django.forms.models import model_to_dict
import json
from .populate_db import populate_db

# Create your views here.

def say_hello(request):
    return render(request, 'hello.html')





def display_match_history(request, summoner_name):
    populate_db(summoner_name)

    summoner = Summoner.objects.get(summoner_name=summoner_name)
    main_participant = (Participant.objects.filter(summoner=summoner)
                    .select_related('match', 'champion', 'matchstats')
                    .order_by('-match__timestamp')[:10])
    match_ids = [participant.match.match_id for participant in main_participant]
    all_participants = (Participant.objects.filter(match__match_id__in=match_ids)
                        .select_related('summoner', 'champion', 'matchstats'))

    context = {'summoner': summoner, 'main_participant': main_participant, 'all_participants': all_participants}
    return render(request, 'match_history.html', context)

def search_summoner(request):
    if request.method == 'POST':
        summoner_name = request.POST['summoner_name']
        return redirect('display_match_history', summoner_name=summoner_name)
    return render(request, 'search_summoner.html')


