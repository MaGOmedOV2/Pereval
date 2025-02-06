from rest_framework.test import APITestCase
from FSTR.perevalapp.serializers import *


class PerevalApiTestCase(APITestCase):
    def setUp(self) -> None:
        self.pereval_one = Pereval.objects.create(
            user=User.objects.create(
                email="abcd@gmail.com",
                fam="pim",
                name="pam",
                otc="pom",
                phone="8-123-456-78-90"
            ),
            beauty_title="Перевал 1 ",
            title="Перевал 1",
            other_title="Перевал 1",
            connect="",
            coords=Coords.objects.create(
                latitude=20.1122,
                longitude=10.3344,
                height=5678
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