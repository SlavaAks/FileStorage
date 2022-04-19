
from django.db import models
from users.models import User

def user_directory_path(instance, filename):
    # путь, куда будет осуществлена загрузка MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class FileStorage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated= models.DateTimeField(auto_now=True)
    hash_content = models.CharField(max_length=255,null=False,unique=True)
    content = models.FileField(upload_to=user_directory_path)

    def delete(self, *args, **kwargs):
        # You have to prepare what you need before delete the model
        storage, path = self.content.storage, self.content.path
        # Delete the model before the file
        super(FileStorage, self).delete(*args, **kwargs)
        # Delete the file after the model
        storage.delete(path)

    class Meta:
        ordering = ('created',)
        verbose_name = 'file'
        verbose_name_plural = 'files'

    def __str__(self):
        return self.content.name
