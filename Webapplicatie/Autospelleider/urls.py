from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'Autospelleider'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^reservation/create/$', views.create_reservation, name='createReservation'),
    url(r'^reservation/create/code/$', views.create_reservation_code, name='createReservationCode'),
    url(r'^inschrijven/(?P<group_code>.+?)/$', views.subscription_with_code, name='createSubscriptionCode'),
    url(r'^inschrijving/bekijken/(?P<reservation_code>.+?)/$', views.view_reservation, name='viewReservation'),
    url(r'^reservation/change/(?P<reservation_code>.+?)/$', views.change_reservation, name='changeReservation'),
    url(r'^contact/mail/$', views.contact_mail, name='sendContactMail'),
    url(r'^setup/$', login_required(views.setup), name='setup'),
    url(r'^setup/inschrijvingen$', login_required(views.inschrijvingen), name='inschrijvingen'),
    url(r'^setup/selectCharacters$', login_required(views.select_characters), name='selectCharacters'),
    url(r'^setup/balanceVillages$', login_required(views.balance_villages), name='balanceVillages'),
    url(r'^village/(?P<village_name>.+?)/participants/$', views.village, name='village'),
    url(r'^village/(?P<village_name>.+?)/orderSeats/$', views.order_seats, name='orderSeats'),
    url(r'^villages/maakInwoners/$', views.maak_inwoners, name='maakInwoners'),
    url(r'^village/(?P<village_name>.+?)/villagers/$', views.villagers, name='villagers'),
    url(r'^village/(?P<village_name>.+?)/setTimer/$', views.set_timer, name='setTimer'),
    url(r'^village/(?P<village_name>.+?)/spelleiderInterface/(?P<seat>[0-9]+?)/(?P<new_village_name>.+?)/$', views.leave_village, name='leaveVillage'),
    url(r'^enterVillage/(?P<village_name>.+?)/spelleiderInterface/(?P<villager_name>.+?)/(?P<villager_name_left>.+?)/$', views.enter_village, name='enterVillage'),
    url(r'^village/(?P<village_name>.+?)/spelleiderInterface/$', views.spelleider_interface, name='spelleiderInterface'),
    url(r'^village/(?P<village_name>.+?)/spelleiderInterface/(?P<participant_ID>[0-9]+?)/$', views.spelleider_interface, name='spelleiderInterface'),
    url(r'^village/(?P<village_name>.+?)/spelleiderInterface/(?P<auto_boodschap>.+?)/$', views.spelleider_interface_auto, name='spelleiderInterfaceAuto'),
    url(r'^plaats_nieuwe_inwoner/village/(?P<village_name>.+?)/(?P<villager_name>.+?)/spelleiderInterface/(?P<auto_boodschap>.+?)/$', views.spelleider_interface_auto, name='spelleiderInterfaceAutoPlaats'),
    url(r'^village/(?P<village_name>.+?)/spelleiderInterface/(?P<nieuwe_inwoner_name>.+?)/(?P<auto_boodschap>.+?)/$', views.spelleider_interface_auto, name='spelleiderInterfaceAutoInwoner'),
    url(r'^manageNotifications/(?P<village_name>.+?)/spelleiderInterface/$', views.manage_notifications, name='manageNotifications'),
#    url(r'^village/(?P<village_name>.+?)/namenrondje/$', views.spelleider_interface_auto_namenrondje, name='namenrondje'),
    url(r'^villages/$', views.villages, name='villages'),
    url(r'^participants/$', views.participants, name='participants'),
    url(r'^genereerInschrijvingen/$', views.genereer_inschrijvingen, name='genereerInschrijvingen'),
    url(r'^verdeelDeelnemers/$', views.verdeel_deelnemers, name='verdeelDeelnemers'),
    url(r'^genereerDorpsnamen/$', views.genereer_dorpsnamen, name='genereerDorpsnamen'),
    url(r'^testmaterialanimation/$', views.test_mat_ani, name='testMaterialAnimation'),
]
