from .models import *
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'name', 'surname', 'phone', 'patronymic']


class CoordsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Coords
        fields = ['length', 'width', 'height']


class LevelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Level
        fields = ['winter', 'sumemr', 'autumn', 'spring']


class ImagesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Images
        fields = ['data', 'title', 'pereval']


class PerevalSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Pereval
        fields = ['beauty_title', 'title', 'other_title', 'connect', 'user', 'add_time', 'coords', 'status', 'level']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_instance, created = User.objects.get_or_create(**user_data)
        coords_data = validated_data.pop('coords')
        coords_instance = Coords.objects.create(**coords_data)
        level_data = validated_data.pop('level')
        level_instance = Level.objects.create(**level_data)
        images_data = validated_data.pop('images')
        pereval_instance = Pereval.objects.create(user=user_instance, coords=coords_instance, level=level_instance,
                                                  ** validated_data, )
        for img in images_data:
            data = img.pop('data')
            title = img.pop('title')
            Images.objects.create(pereval=pereval_instance, title=title, data=data)

        return pereval_instance
