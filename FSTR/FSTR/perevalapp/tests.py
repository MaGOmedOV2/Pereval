
""" Описание тестов:
(setUp)- Этот метод выполняется перед каждым тестом и создает необходимые объекты для тестирования
(пользователь, перевал, координаты, уровень и изображение).
1 (test_get) - проверка создания и получение списка перевалов.
2 (test_get_detail) - проверка совпадения данных.
3 (test_create_and_user_reuse) - проверка использования уже имеющегося пользователя а не добавление дубликата.
4 (test_not_create) - проверка на наличие обязательных полей.
5 (test_update) - проверка обновлений по методу 'patch'.
6 (test_update_not_status_new) - проверка обновления при статусах кроме 'new'.
7 (test_user_update) - проверка не изменяемости пользователя.
8 (test_ok) - проверка на то что не произошло изменение данных после их передачи.
"""

import json
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from FSTR.perevalapp.serializers import *
from rest_framework.test import APIRequestFactory


class PerevalApiTestCase(APITestCase):
    def setUp(self) -> None:
        self.pereval_one = Pereval.objects.create(
            user=User.objects.create(
                email="TestOne@mail.ru",
                fam="TestOne",
                name="TestOne",
                otc="TestOne",
                phone="8-001-001-01-01"
            ),
            beauty_title="PerevalOne",
            title="PerevalOne",
            other_title="PerevalOne",
            connect="",
            coords=Coords.objects.create(
                latitude=27.00001,
                longitude=10.00001,
                height=3991
            ),
            level=Level.objects.create(
                winter='',
                summer='',
                autumn='',
                spring=''
            )
        )
        self.images_1_1 = Images.objects.create(
            data="https://pereval.ru/pereval1-1.jpg",
            title="pereval1-1",
            pereval=self.pereval_one
        )
        self.images_1_1 = Images.objects.create(
            data="https://pereval.ru/pereval1-2.jpg",
            title="pereval1-2",
            pereval=self.pereval_one
        )

        self.pereval_two = Pereval.objects.create(
            user=User.objects.create(
                email="TestTwo@mail.ru",
                fam="TestTwo",
                name="TestTwo",
                otc="TestTwo",
                phone="8-002-002-02-02"
            ),
            beauty_title="PerevalTwo",
            title="PerevalTwo",
            other_title="PerevalTwo",
            connect="",
            coords=Coords.objects.create(
                latitude=27.00002,
                longitude=10.00002,
                height=3992
            ),
            level=Level.objects.create(
                winter='',
                summer='',
                autumn='',
                spring=''
            )
        )
        self.images_2_1 = Images.objects.create(
            data="https://pereval.ru/pereval2-1.jpg",
            title="pereval2-1",
            pereval=self.pereval_two
        )
        self.images_2_2 = Images.objects.create(
            data="https://pereval.ru/pereval2-2.jpg",
            title="pereval2-2",
            pereval=self.pereval_two
        )

        self.pereval_three = Pereval.objects.create(
            user=User.objects.create(
                email="TestThree@mail.ru",
                fam="TestThree",
                name="TestThree",
                otc="TestThree",
                phone="8-003-003-03-03"
            ),
            beauty_title="PerevalThree",
            title="PerevalThree",
            other_title="PerevalThree",
            connect="",
            coords=Coords.objects.create(
                latitude=27.00003,
                longitude=10.00003,
                height=3993
            ),
            level=Level.objects.create(
                winter='',
                summer='',
                autumn='',
                spring=''
            ),
            status="pending"
        )
        self.images_3_1 = Images.objects.create(
            data="https://pereval.ru/pereval3-1.jpg",
            title="pereval3-1",
            pereval=self.pereval_three
        )
        self.images_3_2 = Images.objects.create(
            data="https://pereval.ru/pereval3-2.jpg",
            title="pereval3-2",
            pereval=self.pereval_three
        )

    # начало имени мутода дожно начинаться с "test_",'pereval-list' это basename с приставкой -list
    # ,many=True только если передаем список
    def test_get(self):
        url = reverse('pereval-list')
        response = self.client.get(url)
        factory = APIRequestFactory()
        request = factory.get(url)
        serializer_data = PerevalSerializer([self.pereval_one, self.pereval_two, self.pereval_three], many=True,
                                            context={'request': request}).data
        for pereval in Pereval.objects.all():
            print('********')
            print(pereval.id)
            print('--------')
        self.assertEqual(status.HTTP_200_OK, response.status_code)  # проверка статуса
        self.assertEqual(serializer_data, response.data.get("results"))  # совпадения данных
        self.assertEqual(len(serializer_data), 3)  # проверка создалось ли нужно количество объектов

    def test_get_detail(self):
        url = reverse('pereval-detail', args=(self.pereval_one.id,))
        response = self.client.get(url)
        factory = APIRequestFactory()
        request = factory.get(url)
        serializer_data = PerevalSerializer(self.pereval_one, context={'request': request}).data
        for pereval in Pereval.objects.all():
            print('********')
            print(pereval.id)
            print('--------')
        self.assertEqual(status.HTTP_200_OK, response.status_code)  # проверка статуса
        self.assertEqual(serializer_data, response.data)  # совпадения данных

    def test_create_and_user_reuse(self):
        url = reverse('pereval-list')
        data = {
            'user': {
                'email': 'TestOne@mail.ru',
                'fam': 'TestOne',
                'name': 'TestOne',
                'otc': 'TestOne',
                'phone': '8-001-001-01-01'
            },
            'beauty_title': 'PerevalFive',
            'title': 'PerevalFive',
            'other_title': 'PerevalFive',
            'connect': '',
            'coords': {
                'latitude': 27.00005,
                'longitude': 10.00005,
                'height': 3995
            },
            'level': {
                'winter': 'a5',
                'summer': 'a5',
                'autumn': 'a5',
                'spring': 'a5'
            },
            'images': [
                {
                    'data': 'https://pereval.ru/pereval5-1.jpg',
                    'title': 'pereval5-1'
                },
                {
                    'data': 'https://pereval.ru/pereval5-2.jpg',
                    'title': 'pereval5-2'
                }
            ]
        }
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data, content_type='application/json')
        for pereval in Pereval.objects.all():
            print('********')
            print(pereval.id)
            print('--------')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(3, Pereval.objects.all().count())
        self.assertEqual(3, User.objects.all().count())

    def test_not_create(self):
        url = reverse('pereval-list')
        data = {
            'user': {
                'email': '',
                'fam': '',
                'name': '',
                'otc': '',
                'phone': ''
            },
            'beauty_title': '',
            'title': '',
            'other_title': '',
            'connect': '',
            'coords': {
                'latitude': 27.00000,
                'longitude': 10.00000,
                'height': 3990
            },
            'level': {
                'winter': '',
                'summer': '',
                'autumn': '',
                'spring': ''
            },
            'images': [
                {
                    'data': '',
                    'title': ''
                },
                {
                    'data': '',
                    'title': ''
                }
            ]
        }
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        for pereval in Pereval.objects.all():
            print('********')
            print(pereval.id)
            print('--------')
        self.assertEqual(3, Pereval.objects.all().count())

    def test_update(self):
        url = reverse('pereval-detail', args=(self.pereval_one.id,))
        data = {
            'user': {
                'email': self.pereval_one.user.email,
                'fam': self.pereval_one.user.fam,
                'name': self.pereval_one.user.name,
                'otc': self.pereval_one.user.otc,
                'phone': self.pereval_one.user.phone
            },
            'beauty_title': self.pereval_one.beauty_title,
            'title': self.pereval_one.title,
            'other_title': self.pereval_one.other_title,
            'connect': 'Информация',
            'coords': {
                'latitude': 27.11111,
                'longitude': 10.11111,
                'height': 39911
            },
            'level': {
                'winter': '1A',
                'summer': '1B',
                'autumn': '1C',
                'spring': '1D'
            },
            'images': [
                {
                    'data': 'https://pereval.ru/pereval1-1.jpg',
                    'title': 'pereval1-1'
                },
                {
                    'data': 'https://pereval.ru/pereval1-2.jpg',
                    'title': 'pereval1-2'
                }
            ],
            'status': 'pending'
        }
        json_data = json.dumps(data)
        response = self.client.patch(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)  # проверка статуса
        print(self.pereval_one.status)
        self.pereval_one.refresh_from_db()
        print(self.pereval_one.status)
        self.assertEqual(27.11111, self.pereval_one.coords.latitude)
        self.assertEqual(10.11111, self.pereval_one.coords.longitude)
        self.assertEqual(39911, self.pereval_one.coords.height)
        self.assertEqual('1A', self.pereval_one.level.winter)
        self.assertEqual('1B', self.pereval_one.level.summer)
        self.assertEqual('1C', self.pereval_one.level.autumn)
        self.assertEqual('1D', self.pereval_one.level.spring)
        self.assertEqual('pending', self.pereval_one.status)

    def test_update_not_status_new(self):
        url = reverse('pereval-detail', args=(self.pereval_three.id,))
        data = {
            'user': {
                'email': self.pereval_three.user.email,
                'fam': self.pereval_three.user.fam,
                'name': self.pereval_three.user.name,
                'otc': self.pereval_three.user.otc,
                'phone': self.pereval_three.user.phone
            },
            'beauty_title': self.pereval_three.beauty_title,
            'title': self.pereval_three.title,
            'other_title': self.pereval_three.other_title,
            'connect': '',
            'coords': {
                'latitude': 27.33333,
                'longitude': 10.33333,
                'height': 399333
            },
            'level': {
                'winter': '',
                'summer': '',
                'autumn': '',
                'spring': ''
            },
            'images': [
                {
                    'data': 'https://pereval.ru/pereval3-1.jpg',
                    'title': 'pereval3-1'
                },
                {
                    'data': 'https://pereval.ru/pereval3-2.jpg',
                    'title': 'pereval3-2'
                }
            ]
        }
        json_data = json.dumps(data)
        response = self.client.patch(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.pereval_three.refresh_from_db()
        self.assertEqual(27.00003, self.pereval_three.coords.latitude)
        self.assertEqual(10.00003, self.pereval_three.coords.longitude)
        self.assertEqual(3993, self.pereval_three.coords.height)

    def test_user_update(self):
        url = reverse('pereval-detail', args=(self.pereval_two.id,))
        data = {
            'user': {
                'email': 'email@email.ru',
                'fam': 'TestUUFalse',
                'name': 'TestUUFalse',
                'otc': 'TestUUFalse',
                'phone': '8-888-888-88-88'
            },
            'beauty_title': 'PerevalTwo',
            'title': 'PerevalTwo',
            'other_title': 'PerevalTwo',
            'connect': '',
            'coords': {
                'latitude': 27.00002,
                'longitude': 10.00002,
                'height': 3992
            },
            'level': {
                'winter': '',
                'summer': '',
                'autumn': '',
                'spring': ''
            },
            'images': [
                {
                    'data': 'https://pereval.ru/pereval2-1.jpg',
                    'title': 'pereval2-1'
                },
                {
                    'data': 'https://pereval.ru/pereval2-2.jpg',
                    'title': 'pereval2-2'
                }
            ]
        }
        json_data = json.dumps(data)
        response = self.client.patch(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.pereval_two.refresh_from_db()
        self.assertEqual('TestTwo@mail.ru', self.pereval_two.user.email)
        self.assertEqual('TestTwo', self.pereval_two.user.fam)
        self.assertEqual('TestTwo', self.pereval_two.user.name)
        self.assertEqual('TestTwo', self.pereval_two.user.otc)
        self.assertEqual('8-002-002-02-02', self.pereval_two.user.phone)


class PerevalSerializerTestCase(TestCase):
    def setUp(self) -> None:
        self.pereval_one = Pereval.objects.create(
            user=User.objects.create(
                email="Test1@mail.ru",
                fam="TestOne",
                name="TestOne",
                otc="TestOne",
                phone="8-001-001-01-01"
            ),
            beauty_title="PerevalOne",
            title="PerevalOne",
            other_title="PerevalOne",
            connect="",
            coords=Coords.objects.create(
                latitude=27.00001,
                longitude=10.00001,
                height=3991
            ),
            level=Level.objects.create(
                winter='',
                summer='',
                autumn='',
                spring=''
            )
        )
        self.images_1_1 = Images.objects.create(
            data="https://pereval.ru/pereval1-1.jpg",
            title="pereval1-1",
            pereval=self.pereval_one
        )
        self.images_1_2 = Images.objects.create(
            data="https://pereval.ru/pereval1-2.jpg",
            title="pereval1-2",
            pereval=self.pereval_one
        )

    def test_ok(self):
        url = reverse('pereval-list')
        factory = APIRequestFactory()
        request = factory.get(url)
        data = PerevalSerializer([self.pereval_one], many=True, context={'request': request}).data
        expected_data = [
            {
                'id': self.pereval_one.id,
                'user': {
                    'email': 'Test1@mail.ru',
                    'fam': 'TestOne',
                    'name': 'TestOne',
                    'otc': 'TestOne',
                    'phone': '8-001-001-01-01'
                },
                'beauty_title': 'PerevalOne',
                'title': 'PerevalOne',
                'other_title': 'PerevalOne',
                'connect': '',
                'coords': {
                    'latitude': 27.00001,
                    'longitude': 10.00001,
                    'height': 3991
                },
                'level': {
                    'winter': '',
                    'summer': '',
                    'autumn': '',
                    'spring': ''
                },
                'images': [
                    {
                        'data': 'https://pereval.ru/pereval1-1.jpg',
                        'title': 'pereval1-1'
                    },
                    {
                        'data': 'https://pereval.ru/pereval1-2.jpg',
                        'title': 'pereval1-2'
                    }
                ],
                'status': 'new'
            }
        ]
        self.assertEqual(expected_data, data)
