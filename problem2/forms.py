from django import forms
from django.core.exceptions import ValidationError

from problem2.models import File
from problem2.settings import MAX_UPLOAD_SIZE


class FileForm(forms.ModelForm):

    class Meta:
        model = File
        fields = ('file',)

    def save(self, *args, commit=True, **kwargs):
        self.instance.checksum_sha256 = kwargs.pop('sha256')
        self.instance.checksum_md5 = kwargs.pop('md5')

        return super(FileForm, self).save(commit)

    def clean_file(self):
        file = self.cleaned_data.get('file', None)
        if file:
            if file.size > MAX_UPLOAD_SIZE:
                SizeValidationError = type('SizeValidationError', (ValidationError, ), {'message': ''})
                raise SizeValidationError(message="Uploading file should be less than 10KB")
            return file
        else:
            raise ValidationError("There is no uploaded file")
