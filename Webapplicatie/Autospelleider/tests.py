from django.test import TestCase

# Create your tests here.

from .models import Participant, Group, Villager, Village


def create_participant(first_name='Jonathan', last_name='Corvers', participant_ID=0, reservation_ID=0, main_subscriber=False, paid=False, **optional):
    if 'group' in optional:
        p = Participant(first_name=first_name, last_name=last_name, participant_ID=participant_ID, reservation_ID=reservation_ID, main_subscriber=main_subscriber, paid=paid, group=group)
        p.save()
    else:
        p = Participant(first_name=first_name, last_name=last_name, participant_ID=participant_ID, reservation_ID=reservation_ID, main_subscriber=main_subscriber, paid=paid)
        p.save()

    return  p


def create_group(group_ID=0, group_size=1):
    ps = {}
    group = Group(group_ID=group_ID)
    group.save()
    for x in range(0, group_size):
        key = 'p' + str(x+1)
        value = Participant(first_name='Jonathan' + str(x), last_name='Corvers', participant_ID=x, group=group)
        value.save()
        ps[key] = value

    group.save()

    return group


def create_villager(participant, role='Weerwolf'):
    villager = Villager(participant=participant, role=role)
    villager.save()
    return villager


class VillageMethodTests(TestCase):
    def test_sum_group_sizes(self):
        village = Village(village_name='testVillage')
        village.save()
        g1 = create_group(group_ID=1, group_size=3)
        g1.village = village
        g1.save()
        g2 = create_group(group_ID=2, group_size=5)
        g2.village = village
        g2.save()
        self.assertEqual(village.sum_group_sizes(), 8)

    def test_count_villagers(self):
        village = Village(village_name='testVillage')
        village.save()
        p1 = create_participant(participant_ID=1, reservation_ID=1)
        p2 = create_participant(participant_ID=2, reservation_ID=2)
        p3 = create_participant(participant_ID=3, reservation_ID=2)
        p1.save()
        p2.save()
        p3.save()
        v1 = create_villager(participant=p1)
        v1.village = village
        v1.save()
        v2 = create_villager(participant=p2)
        v2.village = village
        v2.save()
        v3 = create_villager(participant=p3)
        v3.village = village
        v3.save()
        self.assertEqual(village.count_villagers(), 3)



class GroupMethodTests(TestCase):
    def test_group_size(self):
        g = create_group(group_ID=0,group_size=3)
        self.assertEqual(g.group_size(), 3)

    def test_count_groupmembers_familiar_if_group_in_this_village(self):
        v = Village(village_name='Bloetebeke', village_ID=0)
        v.save()
        g = create_group(group_ID=0,group_size=3)
        g2 = create_group(group_ID=1,group_size=3)
        g.save()
        self.assertEqual(v.count_groupmembers_familiar_if_group_in_this_village(g), 3)


class VillagerMethodTests(TestCase):
    def test_new_villagers_have_no_relations(self):
        ps = {}
        villagers = {}
        for x in range(0, 3):
            key = 'p' + str(x+1)
            value = Participant(participant_ID=x)
            value.save()
            ps[key] = value
            value2 = Villager(role='Weerwolf', participant=value)
            value2.save()

            villagers[key] = value2

        for x in range(0, 3):
            key = 'p' + str(x+1)
            self.assertQuerysetEqual(villagers[key].familiars.all(), [])

    def test_add_familiar(self):
        """Testing that only the assigned relations are created and no extras, also that it is symmetrical"""
        ps = {}
        villagers = {}
        for x in range(0, 3):
            key = 'p' + str(x+1)
            name = 'Jonathan' + str(x)
            value = create_participant(first_name=name, participant_ID=x)
            print(value.first_name)
            value.save()
            ps[key] = value
            value2 = Villager(role='Weerwolf', participant=value)
            value2.save()

            villagers[key] = value2

        villagers['p1'].add_familiar(villagers['p2'])
        villagers['p1'].save()
        villagers['p2'].save()

        #print('Dit wordt geprint: <Villager: ' + villagers['p2'].participant.first_name + ' ' + villagers['p2'].participant.last_name + '>')
        self.assertQuerysetEqual(villagers['p1'].familiars.all(), ['<Villager: ' + villagers['p2'].participant.first_name + ' ' + villagers['p2'].participant.last_name + '>'])
        self.assertQuerysetEqual(villagers['p2'].familiars.all(), ['<Villager: ' + villagers['p1'].participant.first_name + ' ' + villagers['p1'].participant.last_name + '>'])
