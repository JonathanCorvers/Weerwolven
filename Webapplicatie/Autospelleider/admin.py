from django.contrib import admin

# Register your models here.

from .models import *

class CharacterAdmin(admin.ModelAdmin):
    readonly_fields = ('created_date', 'modified_date')

admin.site.register(Group)
admin.site.register(GroupSubscription)
admin.site.register(Participant)
admin.site.register(Villager)
admin.site.register(Village)
admin.site.register(Dorpeling)
admin.site.register(Ziener)
admin.site.register(Heks)
admin.site.register(LeerlingZiener)
admin.site.register(Magier)
admin.site.register(AuraZiener)
admin.site.register(Bodyguard)
admin.site.register(Jager)
admin.site.register(Martelares)
admin.site.register(Medium)
admin.site.register(Priester)
admin.site.register(Prins)
admin.site.register(StoereKerel)
admin.site.register(Zieke)
admin.site.register(Onruststoker)
admin.site.register(Vrijmetselaar)
admin.site.register(Bezweerder)
admin.site.register(OudWijf)
admin.site.register(Looier)
admin.site.register(Sekteleider)
admin.site.register(OudeMan)
admin.site.register(Schurk)
admin.site.register(Wolfmens)
admin.site.register(Dubbelganger)
admin.site.register(Cupido)
admin.site.register(Tovenares)
admin.site.register(Dronkaard)
admin.site.register(Vervloekte)
admin.site.register(EenzameWolf)
admin.site.register(Volgeling)
admin.site.register(Weerwolf)
admin.site.register(Vampier)
admin.site.register(Welp)
admin.site.register(Notification)
admin.site.register(Reservation)
admin.site.register(ReservationSubscription)
admin.site.register(Subscription)