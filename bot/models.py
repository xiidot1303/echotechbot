from django.db import models
from django.core.validators import FileExtensionValidator

class Bot_user(models.Model):
    user_id = models.BigIntegerField(null=True)
    name = models.CharField(null=True, blank=True, max_length=256, default='', verbose_name='Ism')
    username = models.CharField(null=True, blank=True, max_length=256, verbose_name='username')
    firstname = models.CharField(null=True, blank=True, max_length=256, verbose_name='Никнейм')
    phone = models.CharField(null=True, blank=True, max_length=16, default='', verbose_name='Telefon')
    REGION_CHOICES = [
        ('andijan', 'Andijon viloyati'),
        ('bukhara', 'Buxoro viloyati'),
        ('fergana', 'Farg‘ona viloyati'),
        ('jizzakh', 'Jizzax viloyati'),
        ('kashkadarya', 'Qashqadaryo viloyati'),
        ('khorezm', 'Xorazm viloyati'),
        ('namangan', 'Namangan viloyati'),
        ('navoiy', 'Navoiy viloyati'),
        ('samarkand', 'Samarqand viloyati'),
        ('sirdaryo', 'Sirdaryo viloyati'),
        ('surkhandarya', 'Surxondaryo viloyati'),
        ('tashkent', 'Toshkent viloyati'),
        ('karakalpakstan', 'Qoraqalpog‘iston Respublikasi'),
        ('tashkent_city', 'Toshkent')
    ]
    region = models.CharField(null=True, blank=True, max_length=256, choices=REGION_CHOICES, verbose_name='Viloyat')
    address = models.CharField(null=True, blank=True, max_length=256, verbose_name='Manzil')
    lang = models.CharField(null=True, blank=True, max_length=4, verbose_name='')
    date = models.DateTimeField(db_index=True, null=True, auto_now_add=True, blank=True, verbose_name='Sana')
    point = models.IntegerField(null=True, blank=True, default=0)

    async def add_point(self, point):
        self.point += point
        await self.asave()

    def __str__(self) -> str:
        try:
            return self.name + ' ' + str(self.phone)
        except:
            return super().__str__()

    class Meta:
        verbose_name = "Bot foydalanuvchisi"
        verbose_name_plural = "Bot foydalanuvchilari"
    
class Message(models.Model):
    bot_users = models.ManyToManyField('bot.Bot_user', blank=True, related_name='bot_users_list', verbose_name='Пользователи бота')
    text = models.TextField(null=True, blank=False, max_length=1024, verbose_name='Текст')
    photo = models.FileField(null=True, blank=True, upload_to="message/photo/", verbose_name='Фото',
        validators=[FileExtensionValidator(allowed_extensions=['jpg','jpeg','png','bmp','gif'])]
    )
    video = models.FileField(
        null=True, blank=True, upload_to="message/video/", verbose_name='Видео',
        validators=[FileExtensionValidator(allowed_extensions=['MOV','avi','mp4','webm','mkv'])]
        )
    file = models.FileField(null=True, blank=True, upload_to="message/file/", verbose_name='Файл')
    is_sent = models.BooleanField(default=False)
    date = models.DateTimeField(db_index=True, null=True, auto_now_add=True, blank=True, verbose_name='Дата')

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"

class ProductsFile(models.Model):
    file_uz = models.FileField(null=True, blank=False, verbose_name="Fayl (Uz)")
    file_ru = models.FileField(null=True, blank=False, verbose_name="Fayl (Ru)")

    class Meta:
        verbose_name = "Mahsulotlar"
        verbose_name_plural = "Mahsulotlar"

class Diler(models.Model):
    text_uz = models.TextField(null=True, blank=False, max_length=2048, verbose_name="Matn (Uz)")
    text_ru = models.TextField(null=True, blank=False, max_length=2048, verbose_name="Matn (Ru)")

    class Meta:
        verbose_name = "Dilerlar"
        verbose_name_plural = "Dilerlar"

class TermOfElectric(models.Model):
    file_uz = models.FileField(null=True, blank=False, verbose_name="Fayl (Uz)")
    file_ru = models.FileField(null=True, blank=False, verbose_name="Fayl (Ru)")

    class Meta:
        verbose_name = "Elektriklar uchun aksiya shartlari"
        verbose_name_plural = "Elektriklar uchun aksiya shartlari"

class TermOfBusinessman(models.Model):
    file_uz = models.FileField(null=True, blank=False, verbose_name="Fayl (Uz)")
    file_ru = models.FileField(null=True, blank=False, verbose_name="Fayl (Ru)")

    class Meta:
        verbose_name = "Tadbirkorlar uchun aksiya shartlari"
        verbose_name_plural = "Tadbirkorlar uchun aksiya shartlari"
    
class Prize(models.Model):
    file_uz = models.FileField(null=True, blank=False, verbose_name="Fayl (Uz)")
    file_ru = models.FileField(null=True, blank=False, verbose_name="Fayl (Ru)")

    class Meta:
        verbose_name = "Sovg'alar"