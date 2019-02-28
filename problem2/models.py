import uuid

from django.db import models


def file_name(instance, filename):
    from django.contrib.contenttypes.models import ContentType
    content_type = ContentType.objects.get_for_model(instance).model
    ext = filename.split('.')[-1]
    filename = 'uploads/{0}/{1}.{2}'.format(content_type, uuid.uuid4(), ext)
    return filename


class File(models.Model):
    file = models.FileField(upload_to=file_name)
    date_created = models.DateTimeField(auto_now_add=True)
    checksum_sha256 = models.CharField(max_length=256, null=False, blank=False)
    checksum_md5 = models.CharField(max_length=256, null=False, blank=False)

    class Meta:
        db_table = 'problem2_file'
