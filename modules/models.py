from django.db import models

from config import settings

# Create your models here.

NULLABLE = {
    'null': True,
    'blank': True,
}


class Module(models.Model):
    serial_number = models.PositiveIntegerField(unique=True, verbose_name='порядковый номер', default=0)
    name = models.CharField(max_length=150, verbose_name='название')
    description = models.TextField(verbose_name='описание', default='ваше описание модуля')
    image = models.ImageField(upload_to='modules/', verbose_name='картинка', **NULLABLE)
    url_video = models.URLField(verbose_name='ссылка на видео', **NULLABLE)
    last_update = models.DateField(auto_now=True, verbose_name='последнее обновление')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='владелец')
    is_published = models.BooleanField(default=True, verbose_name='опубликован')

    def save(self, *args, **kwargs):
        """ Сохранение порядкового номера """
        if not self.pk:
            last_module = Module.objects.order_by('-serial_number').first()
            if last_module:
                self.serial_number = last_module.serial_number + 1
            else:
                self.serial_number = 1
        super(Module, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'модуль'
        verbose_name_plural = 'модули'
        ordering = ('serial_number',)
