from django.shortcuts import render
from django.views.generic.base import TemplateView
from chunked_upload.views import ChunkedUploadView, ChunkedUploadCompleteView
from .models import MyChunkedUpload
from django.views import View

class ChunkedUploadDemo(TemplateView):
    template_name = 'chunked_upload_demo.html'


class UploadFileView(View):
    pass