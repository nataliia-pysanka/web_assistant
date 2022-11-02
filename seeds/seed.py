from flask_seeder import Seeder, generator
from src.models import Contact, Group, User
from src.repository.contacts_repr import *
from src.repository.users_repr import *
from src.repository.notes_repr import *
from random import choices, randint
from faker import Faker

fake = Faker()


# class GroupSeeder(Seeder):
#     def run(self):
#         """Seeds set of basic groups"""
#         groups = ['family', 'friends', 'services', 'job']
#         for group_name in groups:
#             add_group(group_name)


# class UserSeeder(Seeder):
#     def run(self):
#         create_user('admin@gmail.com', 'admin')


# class ContactSeeder(Seeder):
#     def run(self):
#         groups = get_groups()
#         user = get_user_by_email('admin@gmail.com')
#         for _ in range(50):
#             contact_data = {'user_id': user.id,
#                             'first_name': fake.first_name(),
#                             'last_name': fake.last_name(),
#                             'adress': fake.address().replace('\n', ''),
#                             'birth': fake.date_between_dates(date_start='-50y',
#                                                              date_end='-30y'),
#                             'phones': [fake.phone_number()
#                                        for _ in range(randint(0, 2))],
#                             'emails': [fake.email()
#                                        for _ in range(randint(0, 2))],
#                             'groups': list(set(choices(groups, k=randint(1, 2))))
#                             }
#
#             contact = create_contact(**contact_data)
#             print("Adding contact: %s" % contact)


# class TagSeeder(Seeder):
#     def run(self):
#         """Seeds set of basic tags for notes"""
#         tags = ['story', 'memory', 'work', 'warning', 'important', 'to_do']
#         for tag_name in tags:
#             add_tag(tag_name)


class NoteSeeder(Seeder):
    def run(self):
        tags = get_tags()
        user = get_user_by_email('admin@gmail.com')
        for _ in range(20):
            note_data = {'user_id': user.id,
                         'title': fake.sentence(nb_words=5),
                         'text': fake.text(max_nb_chars=1200),
                         'tags': list(set(choices(tags, k=randint(1, 2))))
                         }

            note = create_note(**note_data)
            print("Adding note: %s" % note)
            # print(note_data)
