from django.db import models

# Create your models here.


class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.__class__.objects.exclude(id=self.id).delete()
        super(SingletonModel, self).save(*args, **kwargs)

    @classmethod
    def load(cls):
        try:
            return cls.objects.get()
        except cls.DoesNotExist:
            return cls()


class ConfigBase(SingletonModel):
    title = models.CharField(max_length=125)
    description = models.TextField()

    def __str__(self):
        return self.title


class Rules(ConfigBase):
    pass


class AboutUs(ConfigBase):
    pass
