from django.http import HttpResponse
from django.shortcuts import render

from problem2.forms import FileForm
from problem2 import services


def create_file(request):
    file = None
    for k, v in request.FILES.items():
        file = request.FILES[k]
    sha256 = services.file_hash(file, 'SHA256')
    md5 = services.file_hash(file, 'SHA256')

    form = FileForm(request.POST, request.FILES)
    if form.is_valid():
        instance = form.save(sha256=sha256, md5=md5)
        return render(request, 'index.html', {'upload_number': services.get_upload_number(instance), 'sha256': sha256, 'md5': md5, 'url': instance.file.url})

    return HttpResponse(form.errors['file'].data)


def get_form(request):
    form = FileForm()
    return render(request, 'index.html', {'form': form})

INDEX = {
    'GET': get_form,
    'POST': create_file
}


def index(request):
    return INDEX[request.method](request)
