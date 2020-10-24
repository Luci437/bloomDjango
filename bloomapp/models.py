from django.db import models

# Create your models here.


class Account(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, max_length=100)
    password = models.CharField(max_length=100)



class Groups(models.Model):
    user_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    group_name = models.CharField(max_length=20)
    group_code = models.CharField(max_length=5)
    group_type = models.BooleanField(default=True)


class JoinedGroup(models.Model):
    user_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    group_id = models.ForeignKey(Groups, on_delete=models.CASCADE)


class Reviews(models.Model):
    review = models.CharField(max_length=500)
    user_id = models.ForeignKey(Account, on_delete=models.DO_NOTHING)
    status = models.BooleanField(default=False)
    group_id = models.ForeignKey(Groups, on_delete=models.DO_NOTHING, null=True)




