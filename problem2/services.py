import base64
import hashlib
import os
from filecmp import cmp

from problem2.models import File
from problem2.settings import MEDIA_ROOT


def file_hash(file, type):
    # with file.read() as f:
    if type == 'SHA256':
        sha = hashlib.sha256()
    elif type == 'MD5':
        sha = hashlib.md5()
    else:
        raise ValueError('Unsupported hash function')
    sha.update(file.read())
    sha = sha.digest()
    res = base64.b64encode(sha)
    return res


def get_upload_number(instance, resolve_collisions=True):
    if resolve_collisions != True:
        return File.objects.filter(checksum_sha256=instance.checksum_sha256,
                                                            checksum_md5=instance.checksum_md5).count()
    else:
        same_checksum_collisions = list(File.objects.filter(checksum_sha256=instance.checksum_sha256,
                                                            checksum_md5=instance.checksum_md5).exclude(pk=instance.id).values('id', 'file').all())
        upload_number = len(same_checksum_collisions)+1
        for item in same_checksum_collisions:
            if not cmp(instance.file.path, os.path.join(MEDIA_ROOT, item['file'])):
                upload_number -= 1

        return upload_number
