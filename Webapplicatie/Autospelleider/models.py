import datetime
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone
import base64

# Create your models here.


@python_2_unicode_compatible
class Reservation(models.Model):
    reservation_ID = models.IntegerField(blank=True, null=True, default=-1)
    amount_paid = models.PositiveIntegerField(default=0)
    voorverkoop = models.BooleanField(default=timezone.now() < datetime.datetime(2017,2,19))
    creation_time = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return 'reservatie ' + str(self.id)

    def amount_due(self):
        subscriptions = self.subscription_set.all()
        return len(subscriptions) * (5 * self.voorverkoop + 7 * (1 - self.voorverkoop))

    def paid(self):
        return self.amount_due() == self.amount_paid


@python_2_unicode_compatible
class ReservationSubscription(models.Model):
    reservation_ID = models.IntegerField(blank=True, null=True, default=-1)
    amount_paid = models.PositiveIntegerField(default=0)
    voorverkoop = models.BooleanField(default=timezone.now() < datetime.datetime(2017,2,19))
    creation_time = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return 'reservatie ' + str(self.id)

    def amount_due(self):
        subscriptions = self.subscription_set.all()
        return len(subscriptions) * (5 * self.voorverkoop + 7 * (1 - self.voorverkoop))

    def paid(self):
        return self.amount_due() == self.amount_paid


@python_2_unicode_compatible
class Timer(models.Model):
    start_time = models.DateTimeField()
    stop_time = models.DateTimeField()
    not_done = models.BooleanField(default=True)
    purpose = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return str(self.start_time.hour)


@python_2_unicode_compatible
class Village(models.Model):
    village_name = models.CharField(max_length=200)
    village_ID = models.PositiveIntegerField(null=True)
    start_inhabitants = models.PositiveIntegerField(null=True)
    timer = models.OneToOneField(Timer, related_name='village_timer', on_delete=models.CASCADE, blank=True, null=True)
    balance = models.IntegerField(null=True, blank=True)
    start_characters_amounts = models.CharField(max_length=200, null=True,blank=True)
    start_characters = models.CharField(max_length=1000, null=True,blank=True)
    influences = models.CharField(max_length=200, null=True,blank=True)

    def set_start_characters(self,x):
        start = ''
        for character in x:
            start += character + '!'
        self.start_characters = start
        self.save()

    def get_start_characters(self):
        chars = []
        char = ''
        for c in self.start_characters:
            if c != '!':
                char = char + c
            else:
                chars.append(char)
                char = ''

        return chars

    def set_influences(self, x):
        start = ''
        for character in x:
            start += str(character) + '!'
        self.influences = start
        self.save()

    def get_influences(self):
        chars = []
        char = ''
        for c in self.influences:
            if c != '!':
                char = char + c
            else:
                chars.append(int(char))
                char = ''

        return chars

    def set_start_characters_amounts(self, x):
        start = ''
        for character in x:
            start += str(character) + '!'
        self.start_characters_amounts = start
        self.save()

    def get_start_characters_amounts(self):
        chars = []
        char = ''
        for c in self.start_characters_amounts:
            if c != '!':
                char = char + c
            else:
                chars.append(int(char))
                char = ''

        return chars

    def __str__(self):
        return self.village_name

    def count_villagers(self):
        return len(self.villager_set.all())

    def sum_group_sizes(self):
        sum = 0
        for group in self.group_set.all():
            sum += group.group_size()

        return sum

    def count_groupmembers_familiar_if_group_in_this_village(self, group):
        sum = 0
        for group1 in self.group_set.all():
            if group1 in group.familiar_groups.all() and group1.group_ID != group.group_ID:
                sum += group1.group_size()

        sum += group.group_size()
        return sum

    def get_balance(self):
        if self.influences and self.start_characters_amounts:
            x = self.get_influences()
            y = self.get_start_characters_amounts()
            import numpy as np
            return np.dot(x, y)
        else:
            return 'Error'


@python_2_unicode_compatible
class Group(models.Model):
    group_code = models.CharField(blank=True, null=True, max_length=200)
    group_ID = models.IntegerField(blank=True, null=True, default=-1)
    village = models.ForeignKey(Village, on_delete=models.SET_NULL, blank=True, null=True)
    familiar_groups = models.ManyToManyField("self", blank=True, related_name='group_familiar_groups')

    def __str__(self):
        '''if self.group_code:
            return self.group_code
        else:'''
        return 'Group ' + str(self.id)

    def group_size(self):
        return len(self.participant_set.all())

    def group_subscriptions_size(self):
        return len(self.subscription_set.all())

    def move_to(self,village):
        if self.village:
            vill = self.village
            vill.start_inhabitants -= self.group_size()
            vill.save()
        village.start_inhabitants += self.group_size()
        village.save()
        self.village = village
        self.save()

    def included_reservations(self):
        res = []
        participants_list = self.participant_set.all()
        for participant in participants_list:
            res.append(participant.reservation_ID)

        return res

    def add_familiar_group(self, group):
        self.familiar_groups.add(group)
        self.save()


@python_2_unicode_compatible
class GroupSubscription(models.Model):
    group_code = models.CharField(blank=True, null=True, max_length=200)
    group_ID = models.IntegerField(blank=True, null=True, default=-1)
    village = models.ForeignKey(Village, on_delete=models.SET_NULL, blank=True, null=True)
    familiar_groups = models.ManyToManyField("self", blank=True, related_name='group_familiar_groups')

    def __str__(self):
        '''if self.group_code:
            return self.group_code
        else:'''
        return 'Group ' + str(self.id)

    def group_size(self):
        return len(self.participant_set.all())

    def group_subscriptions_size(self):
        return len(self.subscription_set.all())

    def move_to(self,village):
        if self.village:
            vill = self.village
            vill.start_inhabitants -= self.group_size()
            vill.save()
        village.start_inhabitants += self.group_size()
        village.save()
        self.village = village
        self.save()

    def included_reservations(self):
        res = []
        participants_list = self.participant_set.all()
        for participant in participants_list:
            res.append(participant.reservation_ID)

        return res

    def add_familiar_group(self, group):
        self.familiar_groups.add(group)
        self.save()


@python_2_unicode_compatible
class Subscription(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    age = models.PositiveIntegerField()
    reservation = models.ForeignKey(ReservationSubscription, on_delete=models.CASCADE, null=True)
    group = models.ForeignKey(GroupSubscription, on_delete=models.SET_NULL, blank=True, null=True)
    main_subscriber = models.BooleanField(default=False)
    present = models.BooleanField(default=False)
    email = models.EmailField(max_length=254)

    def __str__(self):
        return self.first_name + ' ' + self.last_name


@python_2_unicode_compatible
class Participant(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    participant_ID = models.PositiveIntegerField(null=True)
    reservation_ID = models.PositiveIntegerField(null=True)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, blank=True, null=True,)
    main_subscriber = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    present = models.BooleanField(default=False)

    def __str__(self):
        return self.first_name + ' ' + self.last_name


@python_2_unicode_compatible
class Villager(models.Model):
    role = models.CharField(max_length=200, blank=True)
    familiars = models.ManyToManyField("self", blank=True, related_name='villager_familiars')
    village = models.ForeignKey(Village, on_delete=models.SET_NULL, blank=True, null=True)
    participant = models.OneToOneField(Participant, on_delete=models.CASCADE, null=True)
    alive = models.BooleanField(default=True)
    seat = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return self.participant.first_name + ' ' + self.participant.last_name

    def add_familiar(self, villager):
        self.familiars.add(villager)
        self.save()


@python_2_unicode_compatible
class Character(models.Model):
    character_name = models.CharField(max_length=200)
    balance_effect = models.IntegerField(null=True, blank=True)
    explanation = models.CharField(max_length=1000, blank=True, null=True)
    priority = models.PositiveIntegerField(null=True, blank=True)
    village = models.ForeignKey(Village, on_delete=models.SET_NULL, blank=True, null=True)
    multiplicable = models.BooleanField(default=False)
    maxi = models.IntegerField(default=1)
    mini = models.IntegerField(default=1)
    villager = models.OneToOneField(Villager, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        abstract = True


@python_2_unicode_compatible
class Dorpeling(Character):
    character_name = 'Dorpeling'
    balance_effect = 1
    explanation = "De taak van de dorpelingen is om de weerwolven, vampiers en de sekteleider te vinden en deze aan het eind van de dag te lynchen."
    priority = 33
    multiplicable = True
    maxi = -1


@python_2_unicode_compatible
class Ziener(Character):
    character_name = 'Ziener'
    balance_effect = 7
    explanation = "Placeholder"
    priority = 31
    maxi = 1


@python_2_unicode_compatible
class Heks(Character):
    character_name = 'Heks'
    balance_effect = 4
    explanation = "Placeholder"
    priority = 27
    maxi = 1


@python_2_unicode_compatible
class LeerlingZiener(Character):
    character_name = 'Leerling-ziener'
    balance_effect = 4
    explanation = "Placeholder"
    priority = 3
    maxi = 1


@python_2_unicode_compatible
class Magier(Character):
    character_name = 'Magiër'
    balance_effect = 4
    explanation = "Placeholder"
    priority = 28
    maxi = 1


@python_2_unicode_compatible
class AuraZiener(Character):
    character_name = 'Aura-ziener'
    balance_effect = 3
    explanation = "Placeholder"
    priority = 30
    maxi = 1


@python_2_unicode_compatible
class Bodyguard(Character):
    character_name = 'Bodyguard'
    balance_effect = 3
    explanation = "Placeholder"
    priority = 17
    maxi = 1


@python_2_unicode_compatible
class Jager(Character):
    character_name = 'Jager'
    balance_effect = 3
    explanation = "Placeholder"
    priority = 5
    maxi = 1


@python_2_unicode_compatible
class Martelares(Character):
    character_name = 'Martelares'
    balance_effect = 3
    explanation = "Placeholder"
    priority = 9
    maxi = 1


@python_2_unicode_compatible
class Medium(Character):
    character_name = 'Medium'
    balance_effect = 3
    explanation = "Placeholder"
    priority = 26
    maxi = 1


@python_2_unicode_compatible
class Priester(Character):
    character_name = 'Priester'
    balance_effect = 3
    explanation = "Placeholder"
    priority = 19
    maxi = 1


@python_2_unicode_compatible
class Prins(Character):
    character_name = 'Prins'
    balance_effect = 3
    explanation = "Placeholder"
    priority = 14
    maxi = 1


@python_2_unicode_compatible
class StoereKerel(Character):
    character_name = 'Stoere kerel'
    balance_effect = 3
    explanation = "Placeholder"
    priority = 15
    maxi = 1


@python_2_unicode_compatible
class Zieke(Character):
    character_name = 'Zieke'
    balance_effect = 3
    explanation = "Placeholder"
    priority = 4
    maxi = 1


@python_2_unicode_compatible
class Onruststoker(Character):
    character_name = 'Onruststoker'
    balance_effect = 2
    explanation = "Placeholder"
    priority = 21
    maxi = 1


@python_2_unicode_compatible
class Vrijmetselaar(Character):
    character_name = 'Vrijmetselaar'
    balance_effect = 2
    explanation = "Placeholder"
    priority = 10
    multiplicable = True
    maxi = 3
    mini = 2


@python_2_unicode_compatible
class Bezweerder(Character):
    character_name = 'Bezweerder'
    balance_effect = 1
    explanation = "Placeholder"
    priority = 20
    maxi = 1


@python_2_unicode_compatible
class OudWijf(Character):
    character_name = 'Oud Wijf'
    balance_effect = 1
    explanation = "Placeholder"
    priority = 18
    maxi = 1


@python_2_unicode_compatible
class Looier(Character):
    character_name = 'Looier'
    balance_effect = 1
    explanation = "Placeholder"
    priority = 8
    maxi = 1


@python_2_unicode_compatible
class Sekteleider(Character):
    character_name = 'Sekteleider'
    balance_effect = 1
    explanation = "Placeholder"
    priority = 29
    maxi = 1


@python_2_unicode_compatible
class OudeMan(Character):
    character_name = 'Oude Man'
    balance_effect = 0
    explanation = "Placeholder"
    priority = 11
    maxi = 1


@python_2_unicode_compatible
class Schurk(Character):
    character_name = 'Schurk'
    balance_effect = 0
    explanation = "Placeholder"
    priority = 7
    maxi = 1


@python_2_unicode_compatible
class Wolfmens(Character):
    character_name = 'Wolfmens'
    balance_effect = -1
    explanation = "Placeholder"
    priority = 6
    maxi = 1


@python_2_unicode_compatible
class Dubbelganger(Character):
    character_name = 'Dubbelganger'
    balance_effect = -2
    explanation = "Placeholder"
    priority = 2
    maxi = 1


@python_2_unicode_compatible
class Cupido(Character):
    character_name = 'Cupido'
    balance_effect = -3
    explanation = "Placeholder"
    priority = 1
    maxi = 1


@python_2_unicode_compatible
class Tovenares(Character):
    character_name = 'Tovenares'
    balance_effect = -3
    explanation = "Placeholder"
    priority = 32
    maxi = 1


@python_2_unicode_compatible
class Dronkaard(Character):
    character_name = 'Dronkaard'
    balance_effect = -3
    explanation = "Placeholder"
    priority = 16
    maxi = 1


@python_2_unicode_compatible
class Vervloekte(Character):
    character_name = 'Vervloekte'
    balance_effect = -3
    explanation = "Placeholder"
    priority = 24
    maxi = 1


@python_2_unicode_compatible
class EenzameWolf(Character):
    character_name = 'Eenzame wolf'
    balance_effect = -5
    explanation = "Placeholder"
    priority = 13
    maxi = 1


@python_2_unicode_compatible
class Volgeling(Character):
    character_name = 'Volgeling'
    balance_effect = -6
    explanation = "Placeholder"
    priority = 22
    maxi = 1


@python_2_unicode_compatible
class Weerwolf(Character):
    character_name = 'Weerwolf'
    balance_effect = -6
    explanation = "Placeholder"
    priority = 23
    multiplicable = True
    maxi = -1


@python_2_unicode_compatible
class Vampier(Character):
    character_name = 'Vampier'
    balance_effect = -8
    explanation = "Placeholder"
    priority = 25
    multiplicable = True
    maxi = -1


@python_2_unicode_compatible
class Welp(Character):
    character_name = 'Welp'
    balance_effect = -8
    explanation = "Placeholder"
    priority = 12
    maxi = 1


@python_2_unicode_compatible
class Notification(models.Model):
    village = models.ForeignKey(Village, on_delete=models.CASCADE, blank=True, null=True)
    type = models.CharField(max_length=200, blank=True, null=True)
    textinfo = models.CharField(max_length=200, blank=True, null=True)
    action = models.CharField(max_length=200, blank=True, null=True)
    creation_time = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=200, default='todo')

    def add_data(self, key, value):
        self.data[key] = value

    def get_data(self, key):
        return self.data[key]


