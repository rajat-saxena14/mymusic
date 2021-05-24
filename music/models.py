from django.db import models
from django.core.validators import FileExtensionValidator

# Create your models here.

class Album(models.Model):
    title=models.CharField(max_length=100,null=False,help_text='Enter the Album Title')
    artist=models.CharField(max_length=100,help_text='Enter the Names of Album Artists')
    genre=models.CharField(max_length=50,help_text='Enter the Album Genre')
    year=models.DateField(help_text='Enter Album Release Date with Format: YYYY-MM-DD ')
    image=models.FileField(validators=[FileExtensionValidator(['jpg','png','webp','jpeg'])],default='')


    def __str__(self):
        return self.title

class Song(models.Model):
    al_id=models.ForeignKey(Album,on_delete=models.CASCADE)
    title=models.CharField(max_length=100,help_text='Enter the Song Title')
    artist=models.CharField(max_length=100,help_text='Enter the Names of Song Artists')
    genre=models.CharField(max_length=20,help_text='Enter the Song Genre')
    image = models.FileField(validators=[FileExtensionValidator(['jpg', 'png'])])
    sfile=models.FileField(validators=[FileExtensionValidator(['mp3','aac'])])


    def __str__(self):
        return self.title

class Palbum(models.Model):
    title=models.CharField(max_length=100,null=False,help_text='Enter the Album Title')
    artist=models.CharField(max_length=100,help_text='Enter the Names of Album Artists')
    genre=models.CharField(max_length=50,help_text='Enter the Album Genre')
    year=models.DateField(help_text='Enter Album Release Date with Format: YYYY-MM-DD ')
    image=models.FileField(validators=[FileExtensionValidator(['jpg','png','webp','jpeg'])],default='')
    price = models.IntegerField(default=0)


    def __str__(self):
        return self.title

class Plist(models.Model):
    al_id=models.ForeignKey(Palbum,on_delete=models.CASCADE)
    title=models.CharField(max_length=100,help_text='Enter the Song Title')
    artist=models.CharField(max_length=100,help_text='Enter the Names of Song Artists')
    genre=models.CharField(max_length=20,help_text='Enter the Song Genre')
    sfile=models.FileField(validators=[FileExtensionValidator(['mp3','mp4','aac'])])
    image=models.FileField(validators=[FileExtensionValidator(['jpg','png'])])

    def __str__(self):
        return self.title

class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    items_json = models.CharField(max_length=5000)
    amount = models.IntegerField( default=0)
    name = models.CharField(max_length=90)
    email = models.CharField(max_length=111)
    address = models.CharField(max_length=111)
    city = models.CharField(max_length=111)
    state = models.CharField(max_length=111)
    zip_code = models.CharField(max_length=111)
    phone = models.CharField(max_length=111, default="")

class OrderUpdate(models.Model):
    update_id  = models.AutoField(primary_key=True)
    order_id = models.IntegerField(default="")
    update_desc = models.CharField(max_length=5000)
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.update_desc[0:7] + "..."

