

# Create your views here.

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, get_object_or_404, render_to_response
from django.urls import reverse
from django.views import generic
from django.utils import timezone
import datetime
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views.decorators.cache import cache_page
from django.template import RequestContext
from django.template.loader import get_template
from django.middleware.csrf import _get_new_csrf_token, rotate_token, _get_new_csrf_string, get_token
import base64

from .models import *


def integer_to_string_encode(integer):
    return str(base64.a85encode(bytearray((str(integer)).encode(encoding='utf-16'))))

def integer_to_string_decode(string):
    return int(str(base64.a85decode(bytearray(string)).decode(encoding='utf-16')))

def create_group_code(group):
    code_begin = "b'"
    code_end = "'"
    code_middle = str(group.id * 7919)
    group.group_code = code_begin + code_middle + code_end
    group.save()

def delete_all_characters():
    Ziener.objects.all().delete()
    Heks.objects.all().delete()
    LeerlingZiener.objects.all().delete()
    Magier.objects.all().delete()
    AuraZiener.objects.all().delete()
    Bodyguard.objects.all().delete()
    Jager.objects.all().delete()
    Martelares.objects.all().delete()
    Medium.objects.all().delete()
    Priester.objects.all().delete()
    Prins.objects.all().delete()
    StoereKerel.objects.all().delete()
    Zieke.objects.all().delete()
    Onruststoker.objects.all().delete()
    Vrijmetselaar.objects.all().delete()
    Dorpeling.objects.all().delete()
    Bezweerder.objects.all().delete()
    OudWijf.objects.all().delete()
    Looier.objects.all().delete()
    Sekteleider.objects.all().delete()
    OudeMan.objects.all().delete()
    Schurk.objects.all().delete()
    Wolfmens.objects.all().delete()
    Dubbelganger.objects.all().delete()
    Cupido.objects.all().delete()
    Tovenares.objects.all().delete()
    Dronkaard.objects.all().delete()
    Vervloekte.objects.all().delete()
    EenzameWolf.objects.all().delete()
    Volgeling.objects.all().delete()
    Weerwolf.objects.all().delete()
    Welp.objects.all().delete()
    Vampier.objects.all().delete()


def find_character(model_name):
    if model_name == 'Ziener':
        return Ziener()
    elif model_name == 'Heks':
        return Heks()
    elif model_name == 'LeerlingZiener' or model_name == 'Leerling ziener':
        return LeerlingZiener()
    elif model_name == 'Magier':
        return Magier()
    elif model_name == 'AuraZiener' or model_name == 'Aura ziener':
        return AuraZiener()
    elif model_name == 'Bodyguard':
        return Bodyguard()
    elif model_name == 'Jager':
        return Jager()
    elif model_name == 'Martelares':
        return Martelares()
    elif model_name == 'Medium':
        return Medium()
    elif model_name == 'Priester':
        return Priester()
    elif model_name == 'Prins':
        return Prins()
    elif model_name == 'StoereKerel' or model_name == 'Stoere kerel':
        return StoereKerel()
    elif model_name == 'Zieke':
        return Zieke()
    elif model_name == 'Onruststoker':
        return Onruststoker()
    elif model_name == 'Vrijmetselaar':
        return Vrijmetselaar()
    elif model_name == 'Dorpeling':
        return Dorpeling()
    elif model_name == 'Bezweerder':
        return Bezweerder()
    elif model_name == 'OudWijf' or model_name == 'Oud wijf':
        return OudWijf()
    elif model_name == 'Looier':
        return Looier()
    elif model_name == 'Sekteleider':
        return Sekteleider()
    elif model_name == 'OudeMan' or model_name == 'Oude man':
        return OudeMan()
    elif model_name == 'Schurk':
        return Schurk()
    elif model_name == 'Wolfmens':
        return Wolfmens()
    elif model_name == 'Dubbelganger':
        return Dubbelganger()
    elif model_name == 'Cupido':
        return Cupido()
    elif model_name == 'Tovenares':
        return Tovenares()
    elif model_name == 'Dronkaard':
        return Dronkaard()
    elif model_name == 'Vervloekte':
        return Vervloekte()
    elif model_name == 'EenzameWolf' or model_name == 'Eenzame wolf':
        return EenzameWolf()
    elif model_name == 'Volgeling':
        return Volgeling()
    elif model_name == 'Weerwolf':
        return Weerwolf()
    elif model_name == 'Welp':
        return Welp()
    elif model_name == 'Vampier':
        return Vampier()
    else:
        return None


def find_influence(model_name):
    role = find_character(model_name=model_name)
    role.save()
    i = role.balance_effect
    role.delete()
    return i


def calculate_average_balance_diff(x1, goal_balance, influences, amount, extra_cards):
    import numpy as np
    all_cards = []
    for indexi, x in enumerate(x1):
        for i in range(0, x):
            all_cards.append(influences[indexi])

    all_cards = np.array(all_cards)
    sums = sum(all_cards)
    average_balance = sums * amount / (amount + extra_cards)
    return np.absolute(goal_balance - average_balance)


def balance_village(goal_balance, amount, influences, maxis, minis, ones, dorpeling_loc, extra_cards):
    import numpy as np

    x = ones[:]
    residu = extra_cards + amount - np.dot(ones,x)
    x[dorpeling_loc] += residu
    continueBool = True
    diff = calculate_average_balance_diff(x1=x, goal_balance=goal_balance, influences=influences, amount=amount, extra_cards=extra_cards)
    actions = []
    itera = 0

    for index1,influence1 in enumerate(influences):
        for index2,influence2 in enumerate(influences):
            if index1 != index2 and influence1 != influence2:
                actions.append((index1,index2)) #remove 1 add 2

    while diff !=0 and continueBool and itera < 10000:
        itera += 1
        continueBool = False
        for action in actions:
            x_new = x[:]
            x_new[action[0]] -= 1
            x_new[action[1]] += 1
            if maxis[action[1]] == -1:
                if x[action[0]]-1 > minis[action[0]]:
                    diff_new = calculate_average_balance_diff(x1=x_new, goal_balance=goal_balance, influences=influences, amount=amount, extra_cards=extra_cards)
                    if diff_new < diff:
                        x = x_new[:]
                        diff = diff_new
                        continueBool = True
            else:
                if x[action[0]]-1 > minis[action[0]] and maxis[action[1]] > x[action[1]]+1:
                    diff_new = calculate_average_balance_diff(x1=x_new, goal_balance=goal_balance, influences=influences, amount=amount, extra_cards=extra_cards)
                    if diff_new < diff:
                        x = x_new[:]
                        diff = diff_new
                        continueBool = True

    return x


def genereer_dorpsnamen_method():
    Village.objects.all().delete()

    import numpy as np
    dorpsnamen = ['Bloetebeke', 'Horrorheide', 'Schaapstad', 'Wolfrijk', 'Roedelgem', 'Denderwolf', 'Extra1', 'Extra2', 'Extra3', 'Extra4', 'Extra5', 'Extra6', 'Extra7', 'Extra8', 'Extra9', 'Extra10']
    participants_amount = len(Participant.objects.all())

    if participants_amount < 30:
        if participants_amount < 24:
            villages_amount = 1
        else:
            villages_amount = 2
    else:
        villages_amount = np.floor(participants_amount / 15)

    for x in range(0,int(villages_amount)):
        Village(village_name=dorpsnamen[x], village_ID=x, start_inhabitants = 0).save()


@login_required(login_url='/admin/login/')
def setup(request):
    return render(request, 'Autospelleider/setup.html')


@login_required(login_url='/admin/login/')
def village(request, village_name):
    village = get_object_or_404(Village, village_name=village_name)
    return render(request, 'Autospelleider/village.html', {
        'village': village,
    })


@login_required(login_url='/admin/login/')
def villages(request):
    villages_list = Village.objects.all()
    return render(request, 'Autospelleider/villages.html', {
        'villages_list': villages_list,
    })


@login_required(login_url='/admin/login/')
def participants(request):
    participants_list = Participant.objects.all()
    dateBool = datetime.datetime.now().date != datetime.date(2017, 3, 4)
    return render(request, 'Autospelleider/participants.html', {
        'participants_list': participants_list,
        'dateBool': dateBool,
    })

@login_required(login_url='/admin/login/')
def inschrijvingen(request):
    inschrijvingen_list = Subscription.objects.all()
    return render(request, 'Autospelleider/inschrijvingen.html', {
        'inschrijvingen_list': inschrijvingen_list,
    })


@login_required(login_url='/admin/login/')
def verdeel_deelnemers(request):

    import numpy as np

    genereer_dorpsnamen_method()

    itlim = 3000
    groups_list = Group.objects.all()
    villages_list = Village.objects.all()
    groups_amount = len(groups_list)
    villages_amount = len(villages_list)

    #Everyone in same group knows eachother
    for group in groups_list:
        for group2 in Group.objects.exclude(group_ID=group.group_ID):
            for reservation in group.included_reservations():
                if reservation in group2.included_reservations():
                    group.add_familiar_group(group2)

    counter = 1
    for group in groups_list:
        group.move_to(Village.objects.get(village_ID=np.remainder(counter, villages_amount)))
        group.save()
        counter += 1

    it = 0

    #Checking condition 1
    CBool = False
    C1Bool = False

    counteri = 1
    while counteri <= villages_amount and not CBool:
        village_groups_list = Village.objects.get(village_ID=counteri-1).group_set.all()
        for group in village_groups_list:
            familiar_groups_list = group.familiar_groups.all()
            groups_in_same_village = village_groups_list.exclude(group_ID=group.group_ID)
            for group2 in familiar_groups_list:
                if group2 in groups_in_same_village:
                    #move group2 to another village
                    potential_villages_list = Village.objects.all()
                    familiar_inhabitant_amount = 10000 #lazy programming
                    for village in potential_villages_list:
                        familiar_inhabitant_amount_new = village.count_groupmembers_familiar_if_group_in_this_village(group2)
                        if familiar_inhabitant_amount_new <= familiar_inhabitant_amount:
                            familiar_inhabitant_amount = familiar_inhabitant_amount_new
                            preferred_village = village
                            break

                    if preferred_village == group2.village.village_name:
                        C1Bool = True
                    group2.move_to(preferred_village) #nope it really can't be not assigned
                    group2.save()
                    CBool = True
                    break

        counteri += 1


    while C1Bool and it<itlim:
        CBool = False
        C1Bool = False

        counteri = 1
        while counteri <= villages_amount and not CBool:
            village_groups_list = Village.objects.get(village_ID=counteri).group_set.all()
            for group in village_groups_list:
                familiar_groups_list = group.familiar_groups.all()
                groups_in_same_village = village_groups_list.objects.exclude(group_ID=group.group_ID)
                for group2 in familiar_groups_list:
                    if group2 in groups_in_same_village:
                        #move group2 to another village
                        potential_villages_list = Village.objects.all()
                        familiar_inhabitant_amount = 10000 #lazy programming
                        for village in potential_villages_list:
                            familiar_inhabitant_amount_new = village.count_groupmembers_familiar_if_group_in_this_village(group2)
                            if familiar_inhabitant_amount_new <= familiar_inhabitant_amount:
                                familiar_inhabitant_amount = familiar_inhabitant_amount_new
                                preferred_village = village
                                break

                        if preferred_village == group2.village.village_name:
                            C1Bool = True
                        group2.move_to(preferred_village) #nope it really can't be not assigned
                        group2.save()
                        CBool = True
                        break

            counteri += 1
        it += 1

    # End of checking condition 1

    # Checking condition 2
    C2Bool = False
    continueBool = True
    counteri = 1

    while counteri <= villages_amount-1 and continueBool:
        counterj = counteri + 1
        village_i = Village.objects.get(village_ID=counteri-1)
        village_i_sum_group_sizes = village_i.start_inhabitants
        while counterj <= villages_amount and continueBool:
            village_j = Village.objects.get(village_ID=counterj-1)
            village_j_sum_group_sizes = village_j.start_inhabitants
            size_difference = np.absolute(village_i_sum_group_sizes-village_j_sum_group_sizes)
            if size_difference != 0:
                # Zoek twee groepen in dezelfde partitie van familiar_groups
                groups_i = village_i.group_set.all()
                groups_j = village_j.group_set.all()
                for groupi in groups_i:
                    for groupj in groupi.familiar_groups.all():
                        if groupj in groups_j:
                            size_difference_new = np.absolute(village_i_sum_group_sizes - groupi.group_size() + groupj.group_size() - (village_j_sum_group_sizes - groupj.group_size() + groupi.group_size()))
                            if size_difference_new < size_difference:
                                # switch groups
                                C2Bool = True
                                continueBool = False
                                #groupi.village = village_j
                                groupi.move_to(village_j)
                                groupi.save()
                                groupj.move_to(village_i)
                                groupj.save()
                                break
                    if not continueBool:
                        break
            counterj += 1
        counteri += 1

    while C2Bool and it<itlim:
        C2Bool = False
        continueBool = True
        counteri = 1

        while counteri <= villages_amount-1 and continueBool:
            counterj = counteri + 1
            village_i = Village.objects.get(village_ID=counteri-1)
            village_i_sum_group_sizes = village_i.start_inhabitants
            while counterj <= villages_amount and continueBool:
                village_j = Village.objects.get(village_ID=counterj-1)
                village_j_sum_group_sizes = village_j.start_inhabitants
                size_difference = np.absolute(village_i_sum_group_sizes-village_j_sum_group_sizes)
                if size_difference != 0:
                    # Zoek twee groepen in dezelfde partitie van familiar_groups
                    groups_i = village_i.group_set.all()
                    groups_j = village_j.group_set.all()
                    for groupi in groups_i:
                        for groupj in groupi.familiar_groups.all():
                            if groupj in groups_j:
                                size_difference_new = np.absolute(village_i_sum_group_sizes - groupi.group_size() + groupj.group_size() - (village_j_sum_group_sizes - groupj.group_size() + groupi.group_size()))
                                if size_difference_new < size_difference:
                                    # switch groups
                                    C2Bool = True
                                    continueBool = False
                                    groupi.move_to(village_j)
                                    groupi.save()
                                    groupj.move_to(village_i)
                                    groupj.save()
                                    break
                        if not continueBool:
                            break
                counterj += 1
            counteri += 1
        it += 1

    # End of condition 2

    # Checking condition 3:
    # Kijken of er groepen zijn die we kunnen wisselen zonder familiarity toe te voegen,
    # die inwonersaantalverschil doen afnemen

    C3Bool = False
    continueBool = True
    counteri = 1

    while counteri <= villages_amount-1 and continueBool:
        counterj = counteri + 1
        village_i = Village.objects.get(village_ID=counteri-1)
        village_i_sum_group_sizes = village_i.start_inhabitants
        while counterj <= villages_amount and continueBool:
            village_j = Village.objects.get(village_ID=counterj-1)
            village_j_sum_group_sizes = village_j.start_inhabitants
            size_difference = np.absolute(village_i_sum_group_sizes-village_j_sum_group_sizes)
            if size_difference != 0:
                # Zoek twee groepen in dezelfde partitie van familiar_groups
                groups_i = village_i.group_set.all()
                groups_j = village_j.group_set.all()
                for groupi in groups_i:
                    # Tel of groupi in village_j steken familiars doet toenemen
                    newFamiliarityBool = village_j.count_groupmembers_familiar_if_group_in_this_village(groupi) == groupi.group_size()
                    if newFamiliarityBool:
                        # controleer of er verbetering is door simpelweg groupi in village_j te steken
                        size_difference_new = np.absolute(village_i_sum_group_sizes - groupi.group_size() - (village_j_sum_group_sizes + groupi.group_size()))
                        if size_difference_new < size_difference:
                            groupi.move_to(village_j)
                            groupi.save()
                            continueBool = False
                            C3Bool = True
                            break
                        else:
                            # vind groupj die niet familiar is met village_i
                            for groupj in groups_j:
                                newFamiliarityBool2 = village_i.count_groupmembers_familiar_if_group_in_this_village(groupj) == groupj.group_size()
                                if newFamiliarityBool2:
                                    size_difference_new = np.absolute(village_j_sum_group_sizes - groupj.group_size() - (village_i_sum_group_sizes + groupj.group_size()))
                                    if size_difference_new < size_difference:
                                        groupj.move_to(village_i)
                                        groupj.save()
                                        continueBool = False
                                        C3Bool = True
                                        break
                                    else:
                                        size_difference_new = np.absolute(village_i_sum_group_sizes - groupi.group_size() + groupj.group_size() - (village_j_sum_group_sizes - groupj.group_size() + groupi.group_size()))
                                        if size_difference_new < size_difference:
                                            C3Bool = True
                                            continueBool = False
                                            groupi.move_to(village_j)
                                            groupi.save()
                                            groupj.move_to(village_i)
                                            groupj.save()
                                            break
                    if not continueBool:
                        break

            counterj += 1
        counteri += 1

    while C3Bool and it<itlim:
        C3Bool = False
        continueBool = True
        counteri = 1
        while counteri <= villages_amount-1 and continueBool:
            counterj = counteri + 1
            village_i = Village.objects.get(village_ID=counteri-1)
            while counterj <= villages_amount and continueBool:
                village_j = Village.objects.get(village_ID=counterj-1)
                village_j_sum_group_sizes = village_j.start_inhabitants
                size_difference = np.absolute(village_i_sum_group_sizes-village_j_sum_group_sizes)
                if size_difference != 0:
                    # Zoek twee groepen in dezelfde partitie van familiar_groups
                    groups_i = village_i.group_set.all()
                    groups_j = village_j.group_set.all()
                    for groupi in groups_i:
                        # Tel of groupi in village_j steken familiars doet toenemen
                        newFamiliarityBool = village_j.count_groupmembers_familiar_if_group_in_this_village(groupi) == groupi.group_size()
                        if newFamiliarityBool:
                            # controleer of er verbetering is door simpelweg groupi in village_j te steken
                            size_difference_new = np.absolute(village_i_sum_group_sizes - groupi.group_size() - (village_j_sum_group_sizes + groupi.group_size()))
                            if size_difference_new < size_difference:
                                groupi.move_to(village_j)
                                groupi.save()
                                continueBool = False
                                C3Bool = True
                                break
                            else:
                                # vind groupj die niet familiar is met village_i
                                for groupj in groups_j:
                                    newFamiliarityBool2 = village_i.count_groupmembers_familiar_if_group_in_this_village(groupj) == groupj.group_size()
                                    if newFamiliarityBool2:
                                        village_i_sum_group_sizes = village_i.start_inhabitants
                                        village_j_sum_group_sizes = village_j.start_inhabitants
                                        size_difference_new = np.absolute(village_j_sum_group_sizes - groupj.group_size() - (village_i_sum_group_sizes + groupj.group_size()))
                                        if size_difference_new < size_difference:
                                            groupj.move_to(village_i)
                                            groupj.save()
                                            continueBool = False
                                            C3Bool = True
                                            break
                                        else:
                                            village_i_sum_group_sizes = village_i.start_inhabitants
                                            village_j_sum_group_sizes = village_j.start_inhabitants
                                            size_difference_new = np.absolute(village_i_sum_group_sizes - groupi.group_size() + groupj.group_size() - (village_j_sum_group_sizes - groupj.group_size() + groupi.group_size()))
                                            if size_difference_new < size_difference:
                                                C3Bool = True
                                                continueBool = False
                                                groupi.move_to(village_j)
                                                groupi.save()
                                                groupj.move_to(village_i)
                                                groupj.save()
                                                break
                        if not continueBool:
                            break

                counterj += 1
            counteri += 1

    for village in villages_list:
        village.start_inhabitants = village.sum_group_sizes()
        village.save()

    return HttpResponseRedirect(reverse('Autospelleider:villages'))


@login_required(login_url='/admin/login/')
def genereer_inschrijvingen(request):

    Group.objects.all().delete()
    Participant.objects.all().delete()
    Villager.objects.all().delete()

    import numpy as np

    amount = request.POST['amount']
    if amount:
        amount = int(amount)
    else:
        amount = 72

    subGroupLimit = 5
    n = 1
    reservation_ID = 0
    group_counter = 1

    while n < amount:
        reservation_ID += 1
        r = 0
        while r == 0:
            r = np.random.poisson(3)

        q = max(min(amount-n, r), 1)
        ps = {}
        for x in range(n, n+q+1):
            key = 'p' + str(x)
            if x==n:
                main_subscriber = True
            else:
                main_subscriber = False

            group_ID = np.remainder(x, np.ceil(q / subGroupLimit)) + group_counter

            if not Group.objects.filter(group_ID=group_ID):
                group = Group(group_ID=group_ID)
                group.save()
            else:
                group = Group.objects.get(group_ID=group_ID)

            value = Participant(first_name='Jonathan' + str(x), last_name='Corvers', participant_ID=x, reservation_ID=reservation_ID, group=group, main_subscriber=main_subscriber)
            value.save()
            ps[key] = value

        group_counter += np.ceil(q / subGroupLimit)
        n += q+1

    return HttpResponseRedirect(reverse('Autospelleider:participants'))


@login_required(login_url='/admin/login/')
def genereer_dorpsnamen(request):

    genereer_dorpsnamen_method()

    return HttpResponseRedirect(reverse('Autospelleider:villages'))


@login_required(login_url='/admin/login/')
def maak_inwoners(request):

    Villager.objects.all().delete()

    for village_i in Village.objects.all():
        for group in village_i.group_set.all():
            vs = {}
            for participant in group.participant_set.all():
                key = str(participant.participant_ID)
                value = Villager(participant=participant, village=village_i)
                vs[key] = value
                vs[key].save()

            for participant in group.participant_set.all():
                for participant2 in group.participant_set.all():
                    participant.villager.add_familiar(participant2.villager)

    for village_i in Village.objects.all():
        for group in village_i.group_set.all():
            for group2 in group.familiar_groups.all():
                for participant in group.participant_set.all():
                    for participant2 in group2.participant_set.all():
                        if participant.participant_ID != participant2.participant_ID:
                            participant.villager.add_familiar(participant2.villager)
                            participant.villager.save()
                            participant2.villager.save()

    return HttpResponseRedirect(reverse('Autospelleider:villages'))


@login_required(login_url='/admin/login/')
def villagers(request, village_name):
    village = get_object_or_404(Village, village_name=village_name)
    return render(request, 'Autospelleider/villagers.html', {
        'village': village,
    })


@login_required(login_url='/admin/login/')
def spelleider_interface(request, village_name, participant_ID=-1):
    import numpy as np
    villages_list = Village.objects.exclude(village_name=village_name)
    village2 = get_object_or_404(Village, village_name=village_name)
    villagers_amount = len(village2.villager_set.all())
    if village2.timer:
        timerOnBool = village2.timer.stop_time - datetime.datetime.now() > datetime.timedelta(0)
        time_left = village2.timer.stop_time - datetime.datetime.now()
        start_rotation = -np.remainder(time_left.seconds*6 + 90,360)
        milliseconds_left = time_left.seconds*1000
        minutes_left = np.floor(time_left.seconds/60)*60*1000
    else:
        timerOnBool = False
        time_left = 0
        start_rotation = 0
        minutes_left = 0
        milliseconds_left = 0

    degrees = []
    if participant_ID != -1:
        participant = get_object_or_404(Participant, participant_ID=participant_ID)
        villager = participant.villager
    else:
        villager = False

    villagers_list = village2.villager_set.all()
    seat = villagers_list[0].seat
    if seat != -1:
        villagers_list = village2.villager_set.all().order_by('seat')
    else:
        villagers_list = village2.villager_set.all()

    for x in range(0, villagers_amount):
        degrees.append(x * (360.0/villagers_amount))
    return render(request, 'Autospelleider/spelleider_interface_materialize.html', {
        'village': village2,
        'villagers_list': villagers_list,
        'villages_list': villages_list,
        'degrees': degrees,
        'villager': villager,
        'timerOnBool': timerOnBool,
        'time_left': time_left,
        'milliseconds_left': milliseconds_left,
        'minutes_left': minutes_left,
        'start_rotation': start_rotation,
        'neg_start_rotation': -start_rotation,
    })


@login_required(login_url='/admin/login/')
def set_timer(request, village_name):

    minutes = request.POST['timerMinutes']
    if minutes:
        minutes = int(minutes)
    else:
        minutes = 3

    village = get_object_or_404(Village, village_name=village_name)
    if village.timer:
        village.timer = None
    else:
        pass

    start_time=datetime.datetime.now()
    stop_time=start_time+datetime.timedelta(minutes=minutes)
    timer = Timer(start_time=start_time, stop_time=stop_time)
    timer.save()
    village.timer = timer
    village.save()

    return HttpResponseRedirect(reverse('Autospelleider:spelleiderInterface', kwargs={'village_name': village_name}))


@login_required(login_url='/admin/login/')
def select_characters(request):
    sub_classes = Character.__subclasses__()
    characters = []
    for character in sub_classes:
        char_name = character.__name__.replace(" object","")
        previous = True
        name = ''
        for c in char_name:
            if c.isupper() and not previous:
                name = name + ' ' + c.lower()
            else:
                name = name + c

            previous = c.isupper()

        characters.append(name)

    characters.sort()

    return render(request, 'Autospelleider/selectCharacters.html', {
        'character_sub_classes': characters,
        'sub_classes': sub_classes,
    })


@login_required(login_url='/admin/login/')
def balance_villages(request):
    delete_all_characters()

    goal_balance = request.POST.get('goal_balance')
    extra_cards = request.POST.get('extra_cards')
    if extra_cards:
        extra_cards = int(extra_cards)
    else:
        extra_cards = 0
    goal_balance = int(goal_balance)
    characters = request.POST.getlist('checks')
    influences = []
    ones = []
    maxis = []
    minis = []
    i = -1
    for iter,character in enumerate(characters):
        role = find_character(model_name=character)
        role.save()
        if role.character_name == 'Dorpeling':
            i = len(influences)
        influences.append(role.balance_effect)
        ones.append(1)
        maxis.append(role.maxi)
        minis.append(0)

        role.delete()

    if i == -1:
        characters.append('Dorpeling')
        influences.append(1)
        ones.append(1)
        maxis.append(-1)
        minis.append(0)
        i = len(characters)-1

    villages = Village.objects.all()
    for testindex,village in enumerate(villages):
        amount = village.sum_group_sizes()
        result = balance_village(goal_balance=goal_balance, amount=amount, influences=influences, maxis=maxis, minis=minis, ones=ones, dorpeling_loc=i, extra_cards=extra_cards)
        for index,character in enumerate(characters):
            cs = {}
            for counter in range(0,result[index]):
                value = find_character(character)
                key = character + str(index)
                cs[key] = value
                cs[key].village = village
                cs[key].save()

        x = influences

        village.set_influences(x=x)
        village.save()
        x = []

        y = characters
        village.set_start_characters(x=y)
        village.save()
        y = []

        z = result
        village.set_start_characters_amounts(x=z)
        village.save()
        z = []

    return render(request, 'Autospelleider/villages.html', {
        'villages_list': villages,
    })


@login_required(login_url='/admin/login/')
def spelleider_interface_auto(request, village_name, auto_boodschap, participant_ID=-1, nieuwe_inwoner_name=None):
    import numpy as np
    villages_list = Village.objects.exclude(village_name=village_name)
    village2 = get_object_or_404(Village, village_name=village_name)
    villagers_amount = len(village2.villager_set.exclude(seat=None))
    if village2.timer:
        timerOnBool = village2.timer.stop_time - datetime.datetime.now() > datetime.timedelta(0)
        time_left = village2.timer.stop_time - datetime.datetime.now()
        start_rotation = -np.remainder(time_left.seconds*6 + 90,360)
        milliseconds_left = time_left.seconds*1000
        minutes_left = time_left.seconds/60
    else:
        timerOnBool = False
        time_left = 0
        start_rotation = 0
        milliseconds_left = 0
        minutes_left = 0
        start_rotation = -np.remainder(90,360)

    if not timerOnBool:
        time_left = 0
        start_rotation = 0
        milliseconds_left = 0
        minutes_left = 0
        start_rotation = -np.remainder(90,360)

    notifications = village2.notification_set.all()
    degrees = []

    if participant_ID != -1:
        participant = get_object_or_404(Participant, participant_ID=participant_ID)
        villager = participant.villager
    else:
        villager = False

    villagers_list = village2.villager_set.all()

    seat = True
    for villager in villagers_list:
        seat = seat and not villager.seat is None

    if seat:
        villagers_list = village2.villager_set.order_by('seat')
    else:
        villagers_list = village2.villager_set.exclude(seat=None)

    if auto_boodschap == 'namenrondje':
        villagers_list = village2.villager_set.all()
        villagers_amount = len(village2.villager_set.all())

    for x in range(0, villagers_amount):
        degrees.append(x * (360.0/villagers_amount))


    return render(request, 'Autospelleider/auto_boodschappen/' + auto_boodschap + '.html', {
        'village': village2,
        'villagers_list': villagers_list,
        'villages_list': villages_list,
        'degrees': degrees,
        'villager': villager,
        'nieuwe_inwoner_name': nieuwe_inwoner_name,
        'timerOnBool': timerOnBool,
        'time_left': time_left,
        'milliseconds_left': milliseconds_left,
        'minutes_left': minutes_left,
        'start_rotation': start_rotation,
        'neg_start_rotation': -start_rotation,
        'villagers_amount': villagers_amount,
        'notifications': notifications,
        'seat': seat,
    })


@login_required(login_url='/admin/login/')
def spelleider_interface_auto(request, village_name, auto_boodschap, participant_ID=-1, nieuwe_inwoner_name=None, villager_name=None):
    import numpy as np
    villages_list = Village.objects.exclude(village_name=village_name)
    village2 = get_object_or_404(Village, village_name=village_name)
    villagers_amount = len(village2.villager_set.exclude(seat=None))
    if village2.timer:
        timerOnBool = village2.timer.stop_time - datetime.datetime.now() > datetime.timedelta(0)
        time_left = village2.timer.stop_time - datetime.datetime.now()
        start_rotation = -np.remainder(time_left.seconds*6 + 90,360)
        milliseconds_left = time_left.seconds*1000
        minutes_left = time_left.seconds/60
    else:
        timerOnBool = False
        time_left = 0
        start_rotation = 0
        milliseconds_left = 0
        minutes_left = 0
        start_rotation = -np.remainder(90,360)

    if not timerOnBool:
        time_left = 0
        start_rotation = 0
        milliseconds_left = 0
        minutes_left = 0
        start_rotation = -np.remainder(90,360)

    notifications = village2.notification_set.all()
    degrees = []

    if participant_ID != -1:
        participant = get_object_or_404(Participant, participant_ID=participant_ID)
        villager = participant.villager
    else:
        villager = False

    villagers_list = village2.villager_set.all()

    seat = True
    for villager in villagers_list:
        seat = seat and not villager.seat is None

    if seat:
        villagers_list = village2.villager_set.order_by('seat')
    else:
        villagers_list = village2.villager_set.exclude(seat=None)

    if auto_boodschap == 'namenrondje':
        villagers_list = village2.villager_set.all()
        villagers_amount = len(village2.villager_set.all())

    for x in range(0, villagers_amount):
        degrees.append(x * (360.0/villagers_amount))


    return render(request, 'Autospelleider/auto_boodschappen/' + auto_boodschap + '.html', {
        'village': village2,
        'villagers_list': villagers_list,
        'villages_list': villages_list,
        'degrees': degrees,
        'villager': villager,
        'nieuwe_inwoner_name': nieuwe_inwoner_name,
        'timerOnBool': timerOnBool,
        'time_left': time_left,
        'milliseconds_left': milliseconds_left,
        'minutes_left': minutes_left,
        'start_rotation': start_rotation,
        'neg_start_rotation': -start_rotation,
        'villagers_amount': villagers_amount,
        'notifications': notifications,
        'seat': seat,
        'villager_name': villager_name,
    })


@login_required(login_url='/admin/login/')
def spelleider_interface_auto_namenrondje(request, village_name, auto_boodschap=None, participant_ID=-1, overlayBool=False):
    import numpy as np
    village2 = get_object_or_404(Village, village_name=village_name)
    villagers_amount = len(village2.villager_set.all())
    if village2.timer:
        timerOnBool = village2.timer.stop_time - datetime.datetime.now() > datetime.timedelta(0)
        time_left = village2.timer.stop_time - datetime.datetime.now()
        start_rotation = -np.remainder(time_left.seconds*6 + 90,360)
        milliseconds_left = time_left.seconds*1000
        minutes_left = time_left.seconds/60
    else:
        timerOnBool = False
        time_left = 0
        milliseconds_left = 0
        minutes_left = 0
        start_rotation = -np.remainder(90,360)

    if not timerOnBool:
        time_left = 0
        milliseconds_left = 0
        minutes_left = 0
        start_rotation = -np.remainder(90,360)

    degrees = []
    seat = -1
    if participant_ID != -1:
        participant = get_object_or_404(Participant, participant_ID=participant_ID)
        villager = participant.villager
        seat = max(participant.villager.seat, seat)
    else:
        villager = False

    if seat != -1:
        villagers_list = village2.villager_set.order_by('seat')
    else:
        villagers_list = village2.villager_set.all()

    villagers_list = village2.villager_set.all() #namenrondje mag nog niet naar plaatsen kijken
    for x in range(0, villagers_amount):
        degrees.append(x * (360.0/villagers_amount))
    return render(request, 'Autospelleider/auto_boodschappen/namenrondje.html', {
        'village': village,
        'villagers_list': villagers_list,
        'degrees': degrees,
        'overlayBool': overlayBool,
        'villager': villager,
        'timerOnBool': timerOnBool,
        'time_left': time_left,
        'milliseconds_left': milliseconds_left,
        'minutes_left': minutes_left,
        'start_rotation': start_rotation,
        'neg_start_rotation': -start_rotation,
        'villagers_amount': villagers_amount,
    })


@login_required(login_url='/admin/login/')
def order_seats(request, village_name):
    village2 = get_object_or_404(Village, village_name=village_name)
    seats = request.POST.getlist('checks')
    if len(seats) == len(village2.villager_set.all()):
        for seat in seats:
            place = seat[0:2]
            villager_name = seat[2:]
            participant = get_object_or_404(Participant, first_name=villager_name)
            villager = participant.villager
            villager.seat = place
            villager.save()

        return HttpResponseRedirect(reverse('Autospelleider:spelleiderInterfaceAuto', kwargs={'village_name': village_name, 'auto_boodschap': 'voorbeeld'}))

    else:
        return HttpResponseRedirect(reverse('Autospelleider:namenrondje', kwargs={'village_name': village_name}))


def index(request):
    background_cover = 'static/Autospelleider/images/bg_bos.jpg'
    background_person = 'static/Autospelleider/images/Sarah.png'
    '''import random
    n1 = random.randint(0,1)
    n2 = random.randint(0,1)

    if n1 is 0:
        background_cover = 'static/Autospelleider/images/bg_bos.jpg'
        if n2 is 0:
            background_person = 'static/Autospelleider/images/Sarah.png'
        else:
            background_person = 'static/Autospelleider/images/Wolf.png'
    else:
        background_cover = 'static/Autospelleider/images/bg_dorp.jpg'
        if n2 is 0:
            background_person = 'static/Autospelleider/images/Wouter.png'
        else:
            background_person = 'static/Autospelleider/images/Jonathan.png'''''

    return render(request, 'Autospelleider/index.html', {
        'background_cover': background_cover,
        'background_person': background_person,
    })

def view_reservation(request, reservation_code):
    reservation = get_object_or_404(ReservationSubscription, id=str(int(float(int(reservation_code)/7919))))
    subscriptions = reservation.subscription_set.all()
    group_code_list = []
    for index in range(len(subscriptions)):
        group_code_list.append(subscriptions[index].group.group_code[2:-1])

    zipped = zip(subscriptions, group_code_list)
    return render(request,'Autospelleider/inschrijving_bekijken.html', {
        'reservation': reservation,
        'zipped': zipped,
        'reservation_code': reservation_code,
        'subscriptions': subscriptions,
    })

def change_reservation(request, reservation_code):
    import urllib

    reservation = ReservationSubscription.objects.get(id=str(int(int(reservation_code)/7919)))
    issues = []

    path = str(request.POST['mydata'])
    path = urllib.parse.unquote_plus(path)

    endpoint = path.find("&")
    endpoints = [endpoint]
    it = 0
    rest = path
    while (not (endpoint == -1)) and (it <= len(path)):
        old_endpoint = endpoint
        rest = rest[old_endpoint+1:]
        if rest.find("groepscode") == 0:
            begin_code = rest.find("b'")
            if not begin_code == -1:
                restrest = rest[begin_code+2:]
                end_code = restrest.find("'")
                endpoint = begin_code + 2 + end_code + 1
        else:
            endpoint = rest.find("&")

        if not endpoint == -1:
            endpoints.append(endpoint)

        it += 1

    key_value_pairs = []
    rest = path
    for index in endpoints:
        key_value_pairs.append(rest[0:index])
        rest = rest[index + 1:]

    key_value_pairs.append(rest)

    form_data = {}
    for pair in key_value_pairs:
        key_end = pair.find("[]=")
        if not key_end == -1:
            key = pair[0:key_end]
            value = pair[key_end+3:]
            form_data[key] = value

    subs_amount = form_data['subs_amount']

    subscribers = reservation.subscription_set.all()

    for index, subscriber in enumerate(subscribers):
        group = form_data['custom-selected' + str(index + 1)]
        if not group[0] == 'n':
            group_code = form_data['groepscode' + str(index + 1)]
            group_by_code = GroupSubscription.objects.get(group_code=group_code)
            if not group_by_code.group_subscriptions_size() > 3:
                subscriber.group = group_by_code
                subscriber.save()
            else:
                issues.append('Groep ' + group_code[2:-1] + ' was al vol.')

    group_code_list = []
    for index in range(int(subs_amount)):
        group_code_list.append(subscribers[index].group.group_code[2:-1])

    zipped = zip(subscribers, group_code_list)

    return render(request,'Autospelleider/form_step_change_reservation.html', {
        'zipped': zipped,
        'reservation': reservation,
        'issues': issues,
    })

def subscription_with_code(request, group_code):
    background_cover = 'Autospelleider/images/bg_bos.jpg'
    background_person = 'Autospelleider/images/Sarah.png'
    full = False
    try:
        group = GroupSubscription.objects.get(group_code="b'" + group_code + "'")
        exists = True
        if group.group_subscriptions_size() > 3:
            full = True
    except:
        exists = False
    '''import random
    n1 = random.randint(0,1)
    n2 = random.randint(0,1)

    if n1 is 0:
        background_cover = 'static/Autospelleider/images/bg_bos.jpg'
        if n2 is 0:
            background_person = 'static/Autospelleider/images/Sarah.png'
        else:
            background_person = 'static/Autospelleider/images/Wolf.png'
    else:
        background_cover = 'static/Autospelleider/images/bg_dorp.jpg'
        if n2 is 0:
            background_person = 'static/Autospelleider/images/Wouter.png'
        else:
            background_person = 'static/Autospelleider/images/Jonathan.png'''''

    return render(request, 'Autospelleider/inschrijving_groepcode.html', {
        'background_cover': background_cover,
        'background_person': background_person,
        'group_code': group_code,
        'exists': exists,
        'full': full,
    })

def create_reservation(request):
    import urllib

    issues = []

    path = str(request.POST['mydata'])
    path = urllib.parse.unquote_plus(path)

    endpoint = path.find("&")
    endpoints = [endpoint]
    it = 0
    rest = path
    while (not (endpoint == -1)) and (it <= len(path)):
        old_endpoint = endpoint
        rest = rest[old_endpoint+1:]
        if rest.find("groepscode") == 0:
            begin_code = rest.find("b'")
            restrest = rest[begin_code+2:]
            end_code = restrest.find("'")
            endpoint = begin_code + 2 + end_code + 1
        else:
            endpoint = rest.find("&")

        if not endpoint == -1:
            endpoints.append(endpoint)

        it += 1

    key_value_pairs = []
    rest = path
    for index in endpoints:
        key_value_pairs.append(rest[0:index])
        rest = rest[index + 1:]

    key_value_pairs.append(rest)

    form_data = {}
    for pair in key_value_pairs:
        key_end = pair.find("[]=")
        if not key_end == -1:
            key = pair[0:key_end]
            value = pair[key_end+3:]
            form_data[key] = value

    reservation = ReservationSubscription()
    reservation.save()

    subs_amount = form_data['subs_amount']
    groups = []
    custom = []
    subscribers = []

    for index in range(int(subs_amount)):
        first_name = form_data['first_name' + str(index)]
        last_name = form_data['last_name' + str(index)]
        age = form_data['leeftijd' + str(index)]
        email = form_data['email' + str(index)]
        group = form_data['custom-selected' + str(index)]
        if group[0] == 'n':
            groups.append(str(group[9]))
            custom.append(False)
        else:
            groups.append(form_data['groepscode' + str(index)])
            custom.append(True)

        main_subscriber = False
        if index == 0:
            main_subscriber = True

        subscriber = Subscription(first_name=first_name,
                                  last_name=last_name,
                                  age=int(age),
                                  email=email,
                                  main_subscriber=main_subscriber,
                                  reservation=reservation)
        subscriber.save()
        subscribers.append(subscriber)

    noncustom_groups = []
    for i in range(len(custom)):
        if custom[i] == False:
            noncustom_groups.append(int(groups[i]))

    group_instances = subscribers[:]
    noncustom_groups = set(noncustom_groups)
    possible_groups = []
    for ncg in noncustom_groups:
        group_instance = GroupSubscription()
        group_instance.save()
        create_group_code(group_instance)
        group_instances[ncg-1] = (group_instance)
        possible_groups.append(group_instance)

    groupless_subscribers = []
    for index in range(int(subs_amount)):
        if custom[index] == False:
            ind = int(groups[index]) - 1
            subscribers[index].group = group_instances[ind]
        else:
            try:
                group_by_code = GroupSubscription.objects.get(group_code=groups[index])
                if group_by_code.group_subscriptions_size() < 4 :
                    subscribers[index].group = group_by_code
                else:
                    full_group = groups[index]
                    issues.append('Er zaten al 4 personen in groep ' + full_group[2:-1] + '.')
                    issues.append(subscribers[index].first_name + ' ' + subscribers[index].last_name + ' is ingedeeld in een andere groep.')
                    issues.append('Dit kan je nog aanpassen via een link in de e-mail die je zal ontvangen.')
                    groupless_subscribers.append(subscribers[index])
            except:
                groupless_subscribers.append(subscribers[index])
                non_existent_group = groups[index]
                issues.append('Groep ' + non_existent_group[2:-1] + ' bestaatniet.')
                issues.append(subscribers[index].first_name + ' ' + subscribers[index].last_name + ' is ingedeeld in een andere groep.')
                issues.append('Je kan via de link in de mail die je zal ontvangen deze persoon nog in een andere groep zetten.')

        subscribers[index].save()

    for index in range(len(groupless_subscribers)):
        if len(possible_groups) > 0:
            for indexg, possible_group in enumerate(possible_groups):
                if possible_group.group_subscriptions_size() < 4 and (not subscribers[index].group):
                    subscribers[index].group = possible_group
                elif indexg == len(possible_groups) - 1:
                    new_possible_group = GroupSubscription()
                    new_possible_group.save()
                    create_group_code(new_possible_group)
                    subscribers[index].group = new_possible_group
                    subscribers[index].save()
                    possible_groups.append(new_possible_group)
        else:
            new_possible_group = GroupSubscription()
            new_possible_group.save()
            create_group_code(new_possible_group)
            subscribers[index].group = new_possible_group
            subscribers[index].save()
            possible_groups.append(new_possible_group)

    group_code_list = []
    for index in range(int(subs_amount)):
        group_code_list.append(subscribers[index].group.group_code[2:-1])

    zipped = zip(subscribers, group_code_list)
    group_list = list(set(group_code_list))

    from django.core.mail import send_mail

    html_message = loader.render_to_string(
                                            'Autospelleider/bevestiging_inschrijving_email.html',
                                            {
                                                'main_subscriber': subscribers[0],
                                                'zipped': zipped,
                                                'reservation': reservation,
                                                'amount_due': reservation.amount_due(),
                                                'subscribers': subscribers,
                                                'reservation_code': reservation.id * 7919,
                                                'group_code_list': group_code_list,
                                                'group_list': group_list,
                                            })
    text_message = loader.render_to_string(
                                            'Autospelleider/bevestiging_inschrijving_email.txt',
                                            {
                                                'main_subscriber': subscribers[0],
                                                'zipped': zipped,
                                                'reservation': reservation,
                                                'amount_due': reservation.amount_due(),
                                                'subscribers': subscribers,
                                                'reservation_code': reservation.id * 7919,
                                                'group_code_list': group_code_list,
                                                'group_list': group_list,
                                            })
    send_mail(
        'Bevestiging inschrijving',
        text_message,
        'limburgsewolven@gmail.com',
        [subscribers[0].email],
        fail_silently=False,
        html_message=html_message,
    )

    return render(request,'Autospelleider/form_step.html', {
        'zipped': zipped,
        'reservation': reservation,
        'issues': issues,
    })

def create_reservation_code(request):
    import urllib

    issues = []

    path = str(request.POST['mydata'])
    path = urllib.parse.unquote_plus(path)

    endpoint = path.find("&")
    endpoints = [endpoint]
    it = 0
    rest = path
    while (not (endpoint == -1)) and (it <= len(path)):
        old_endpoint = endpoint
        rest = rest[old_endpoint+1:]
        if rest.find("groepscode") == 0:
            begin_code = rest.find("b'")
            restrest = rest[begin_code+2:]
            end_code = restrest.find("'")
            endpoint = begin_code + 2 + end_code + 1
        else:
            endpoint = rest.find("&")

        if not endpoint == -1:
            endpoints.append(endpoint)

        it += 1

    key_value_pairs = []
    rest = path
    for index in endpoints:
        key_value_pairs.append(rest[0:index])
        rest = rest[index + 1:]

    key_value_pairs.append(rest)

    form_data = {}
    for pair in key_value_pairs:
        key_end = pair.find("[]=")
        if not key_end == -1:
            key = pair[0:key_end]
            value = pair[key_end+3:]
            form_data[key] = value

    reservation = ReservationSubscription()
    reservation.save()

    subs_amount = form_data['subs_amount']
    groups = []
    custom = []
    subscribers = []

    first_name = form_data['first_name0']
    last_name = form_data['last_name0']
    age = form_data['leeftijd0']
    email = form_data['email0']
    group = form_data['custom-selected0']
    if group[0] == 'n':
        groups.append(str(group[9]))
        custom.append(False)
    else:
        groups.append(form_data['groepscode0'])
        custom.append(True)

    main_subscriber = True

    subscriber = Subscription(first_name=first_name,
                              last_name=last_name,
                              age=int(age),
                              email=email,
                              main_subscriber=main_subscriber,
                              reservation=reservation)
    subscriber.save()
    subscribers.append(subscriber)

    noncustom_groups = []
    for i in range(len(custom)):
        if custom[i] == False:
            noncustom_groups.append(int(groups[i]))

    group_instances = subscribers[:]
    noncustom_groups = set(noncustom_groups)
    possible_groups = []
    for ncg in noncustom_groups:
        group_instance = GroupSubscription()
        group_instance.save()
        create_group_code(group_instance)
        group_instances[ncg-1] = (group_instance)
        possible_groups.append(group_instance)

    groupless_subscribers = []
    for index in range(int(subs_amount)):
        if custom[index] == False:
            ind = int(groups[index]) - 1
            subscribers[index].group = group_instances[ind]
        else:
            try:
                group_by_code = GroupSubscription.objects.get(group_code=groups[index])
                if group_by_code.group_subscriptions_size() < 4 :
                    subscribers[index].group = group_by_code
                else:
                    full_group = groups[index]
                    issues.append('Er zaten al 4 personen in groep ' + full_group[2:-1] + '.')
                    issues.append(subscribers[index].first_name + ' ' + subscribers[index].last_name + ' is ingedeeld in een andere groep.')
                    issues.append('Dit kan je nog aanpassen via een link in de e-mail die je zal ontvangen.')
                    groupless_subscribers.append(subscribers[index])
            except:
                groupless_subscribers.append(subscribers[index])
                non_existent_group = groups[index]
                issues.append('Groep ' + non_existent_group[2:-1] + ' bestaatniet.')
                issues.append(subscribers[index].first_name + ' ' + subscribers[index].last_name + ' is ingedeeld in een andere groep.')
                issues.append('Je kan via de link in de mail die je zal ontvangen deze persoon nog in een andere groep zetten.')

        subscribers[index].save()

    for index in range(len(groupless_subscribers)):
        if len(possible_groups) > 0:
            for indexg, possible_group in enumerate(possible_groups):
                if possible_group.group_subscriptions_size() < 4 and (not subscribers[index].group):
                    subscribers[index].group = possible_group
                elif indexg == len(possible_groups) - 1:
                    new_possible_group = GroupSubscription()
                    new_possible_group.save()
                    create_group_code(new_possible_group)
                    subscribers[index].group = new_possible_group
                    subscribers[index].save()
                    possible_groups.append(new_possible_group)
        else:
            new_possible_group = GroupSubscription()
            new_possible_group.save()
            create_group_code(new_possible_group)
            subscribers[index].group = new_possible_group
            subscribers[index].save()
            possible_groups.append(new_possible_group)

    group_code_list = []
    for index in range(int(subs_amount)):
        group_code_list.append(subscribers[index].group.group_code[2:-1])

    zipped = zip(subscribers, group_code_list)

    from django.core.mail import send_mail

    html_message = loader.render_to_string(
                                            'Autospelleider/bevestiging_inschrijving_email.html',
                                            {
                                                'main_subscriber': subscribers[0],
                                                'zipped': zipped,
                                                'reservation': reservation,
                                                'amount_due': reservation.amount_due(),
                                                'subscribers': subscribers,
                                            })
    text_message = loader.render_to_string(
                                            'Autospelleider/bevestiging_inschrijving_email.txt',
                                            {
                                                'main_subscriber': subscribers[0],
                                                'zipped': zipped,
                                                'reservation': reservation,
                                                'amount_due': reservation.amount_due(),
                                                'subscribers': subscribers,
                                            })
    send_mail(
        'Bevestiging inschrijving',
        text_message,
        'limburgsewolven@gmail.com',
        [subscribers[0].email],
        fail_silently=False,
        html_message=html_message,
    )

    return render(request,'Autospelleider/form_step.html', {
        'zipped': zipped,
        'reservation': reservation,
        'issues': issues,
    })

def contact_mail(request):
    import urllib

    path = str(request.POST['mydata'])
    path = urllib.parse.unquote_plus(path)

    endpoint = path.find("&")
    endpoints = [endpoint]
    it = 0
    rest = path
    while (not (endpoint == -1)) and (it <= len(path)):
        old_endpoint = endpoint
        rest = rest[old_endpoint+1:]
        if rest.find("groepscode") == 0:
            begin_code = rest.find("b'")
            restrest = rest[begin_code+2:]
            end_code = restrest.find("'")
            endpoint = begin_code + 2 + end_code + 1
        else:
            endpoint = rest.find("&")

        if not endpoint == -1:
            endpoints.append(endpoint)

        it += 1

    key_value_pairs = []
    rest = path
    for index in endpoints:
        key_value_pairs.append(rest[0:index])
        rest = rest[index + 1:]

    key_value_pairs.append(rest)

    form_data = {}
    for pair in key_value_pairs:
        key_end = pair.find("[]=")
        if not key_end == -1:
            key = pair[0:key_end]
            value = pair[key_end+3:]
            form_data[key] = value

    from django.core.mail import send_mail

    html_message = loader.render_to_string(
                                            'Autospelleider/contact_email.html',
                                            form_data,
                                            )
    text_message = loader.render_to_string(
                                            'Autospelleider/contact_email.txt',
                                            form_data,
                                            )
    send_mail(
        'Contactformulier: '+ form_data['subject'],
        text_message,
        'limburgsewolven@gmail.com',
        ['limburgsewolven@gmail.com'],
        fail_silently=False,
    )

    send_mail(
        'Contactformulier: '+ form_data['subject'],
        text_message,
        'limburgsewolven@gmail.com',
        [form_data['email']],
        fail_silently=False,
        html_message=html_message,
    )

    return render(request,'Autospelleider/contact_form_sent.html', {
    })


@login_required(login_url='/admin/login/')
def leave_village(request, village_name, new_village_name, seat):

    village2 = get_object_or_404(Village, village_name=village_name)
    new_village = get_object_or_404(Village, village_name=new_village_name)
    villager = get_object_or_404(Villager, village=village2, seat=seat)
    villager.village = new_village
    villager.seat = None
    villager.save()
    textinfo = villager.participant.first_name + ' komt jouw dorp binnen!'
    notification = Notification(village=new_village, type='Verhuis', textinfo=textinfo)
    notification.action = villager.participant.first_name
    notification.save()

    linkurl = '/village/'+ village_name + '/spelleiderInterface/voorbeeld/'
    return HttpResponseRedirect(linkurl)


@login_required(login_url='/admin/login/')
def enter_village(request, village_name, villager_name, villager_name_left):

    village2 = get_object_or_404(Village, village_name=village_name)
    villagers = village2.villager_set.all()
    for villagerin in villagers:
        if villagerin.participant.first_name == villager_name:
            villager = villagerin
        elif villagerin.participant.first_name == villager_name_left:
            villager_left = villagerin

    seat_left = villager_left.seat

    seat_counter = seat_left + 1
    continueBool = True
    for villagerin in villagers.exclude(seat=None).order_by('seat'):
        if villagerin.seat > seat_left and villagerin.seat > seat_counter and continueBool:
            villager.seat = seat_counter
            villager.save()
            continueBool = False
        elif villagerin.seat > seat_left and villager.seat is None:
            seat_counter += 1
            villager.seat = villagerin.seat
            villager.save()
            villagerin.seat = seat_counter
            villagerin.save()
        elif villager.seat:
            seat_counter += 1
            villagerin.seat = seat_counter
            villagerin.save()

    if villager.seat is None:
        villager.seat = seat_counter
        villager.save()

    seat_counter = 0
    for villagerin in villagers.exclude(seat=None).order_by('seat'):
        villagerin.seat = seat_counter
        villagerin.save()
        seat_counter += 1

    textinfo = villager.participant.first_name + ' komt jouw dorp binnen!'
    notification = get_object_or_404(Notification, textinfo=textinfo)
    notification.status = 'done'
    notification.save()

    linkurl = '/village/' + village_name + '/spelleiderInterface/voorbeeld/'

    return HttpResponseRedirect(linkurl)


@csrf_exempt
def manage_notifications(request, village_name):
    village2 = get_object_or_404(Village, village_name=village_name)
    s = ''
    for notification in village2.notification_set.exclude(status='done'):
        s += '<li>'
        s += '<div class=\"collapsible-header\">'
        s += '<i class=\"material-icons\">place</i>'
        s += notification.type + '</div>'
        s += '<div class=\"collapsible-body body-not\">'
        s += '<p>' + notification.textinfo
        s += '<i class=\"material-icons right\" id=\"notification' + '\">done</i>'
        if notification.type == 'Verhuis':
            s += '<br><a class=\"left\" href=\"/plaats_nieuwe_inwoner/village/' + village2.village_name + '/' + notification.action + '/spelleiderInterface/plaats_nieuwe_inwoner/\"><i class=\"material-icons\">launch</i></a>'
        s += '</p></div>'
        s += '</li>'

    return HttpResponse(s)


def test_mat_ani(request):
    return render(request,'Autospelleider/test-material-animation.html')
