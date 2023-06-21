import base64
from io import BytesIO
from softarex_django_project import settings
from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa
import os
import tensorflow as tf


form_attr = {'class': 'form-control'}


model_path = os.path.join(settings.BASE_DIR, 'main/static/model')
model = tf.saved_model.load(model_path)


def image_to_base64(image):
    # Конвертируем изображение в строку base64
    buffered = BytesIO()
    image.save(buffered, format='JPEG')
    image_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
    return image_base64


class DataMixin:
    def __init__(self):
        self.context = None
        self.request = None

    def get_context(self, **kwargs):
        kwargs_copy = kwargs.copy()
        self.context = kwargs

        return self.context


