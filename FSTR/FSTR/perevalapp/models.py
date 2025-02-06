from django.db import models


class User(models.Model):
    email = models.EmailField()
    surname = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    patronymic = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)


class Coords(models.Model):
    length = models.FloatField(max_length=50)
    width = models.FloatField(max_length=50)
    height = models.IntegerField()


class Level(models.Model):
    winter = models.CharField(max_length=20, verbose_name='Зима', blank=True, null=True)
    summer = models.CharField(max_length=20, verbose_name='Лето', blank=True, null=True)
    autumn = models.CharField(max_length=20, verbose_name='Осень', blank=True, null=True)
    spring = models.CharField(max_length=20, verbose_name='Весна', blank=True, null=True)


class Pereval(models.Model):
    new = "new"
    pending = "pending"
    accepted = "accepted"
    rejected = "rejected"
    CHOISES = [
        (new, "новый"),
        (pending, "модератор проверяет работу"),
        (accepted, "модерация прошла успешно"),
        (rejected, "модерация прошла, информация не принята"),
    ]

    beauty_title = models.CharField(max_length=255, default='пер.')
    title = models.CharField(max_length=255)
    other_title = models.CharField(max_length=255)
    connect = models.TextField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    add_time = models.DateTimeField(auto_now_add=True)
    coords = models.ForeignKey(Coords, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=CHOISES, default=new)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)


class Images(models.Model):
    data = models.URLField()
    title = models.CharField(max_length=255)
    pereval = models.ForeignKey(Pereval, on_delete=models.CASCADE, related_name='images')