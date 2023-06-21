import base64
import io
import json
import logging
import os
import pickle
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from fpdf import FPDF
from django.http import HttpResponse, FileResponse
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from main.forms import RegisterForm, LoginForm, FileUploadForm
from main.models import Computation, User
from main.utils import DataMixin, image_to_base64, model

from PIL import Image
import numpy as np
import tensorflow as tf

from softarex_django_project import settings

logger = logging.getLogger(__name__)


def index(request):
    return render(request, "index.html")


class Register(DataMixin, CreateView):
    form_class = RegisterForm
    template_name = 'auth/register.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        utils_context = self.get_context(title='Registration')
        return dict(list(context.items()) + list(utils_context.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)

        logger.info(f'{self.request.user} registered')

        return redirect('home')


class Login(DataMixin, LoginView):
    form_class = LoginForm
    template_name = 'auth/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        u_context = self.get_context(title="Authorization")
        return dict(list(context.items()) + list(u_context.items()))

    def get_success_url(self):
        logger.info(f'{self.request.user} logged in')

        return reverse_lazy('home')


def user_logout(request):
    logger.info(f'{request.user} logged out')

    logout(request)
    return redirect('home')


class Profile(DataMixin, TemplateView):
    template_name = 'profile/index.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        u_context = self.get_context(title="Profile")
        return dict(list(context.items()) + list(u_context.items()))


class Computations(DataMixin, TemplateView):
    template_name = 'computations/index.html'
    form_class = FileUploadForm

    def get(self, request, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data['file']
            image = Image.open(file)
            image = image.convert('L')
            pixel_array = np.array(image)

            ser_pixel_array = pixel_array.astype(int)
            serialized = json.dumps(ser_pixel_array.tolist())

            pixel_array = pixel_array.astype(np.float32) / 255.0
            pixel_array = np.expand_dims(pixel_array, axis=(0, 3))  # Добавляем размерности батча и каналов
            pixel_array = np.repeat(pixel_array, 3, axis=3)

            predict_fn = model.signatures['serving_default']

            result = predict_fn(resnet50_input=pixel_array)
            result = result['dense_1'].numpy()
            predictions = result[0]

            definitions = ["angry", "disgust", "fear", "happy", "sad", "surprise", "neutral"]
            predictions = {definition: prediction for definition, prediction in zip(definitions, predictions)}

            image_base64 = image_to_base64(image)

            data = {
                'form': form,
                'predictions_dict': predictions,
                'predictions': predictions.items(),
                'max_item': max(predictions.values()),
                'image': image_base64,
            }
            

            ser_predictions = {}
            for key, value in predictions.items():
                ser_predictions[key] = str(value)

            ser_predictions = json.dumps(ser_predictions)


            self.request.user.computation_quantity += 1
            self.request.user.save()

            Computation.objects.create(author=self.request.user, image_array=serialized, results=ser_predictions)

            return render(request, self.template_name, data)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        u_context = self.get_context(title="Computations")
        return dict(list(context.items()) + list(u_context.items()))


def save_as_pdf(request):
    if request.method == 'POST':
        data = request.POST.get('data', '')
        data = data.replace('\'','\"')
        data = json.loads(data)
        
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="table.pdf"'

        pdf = SimpleDocTemplate(response, pagesize=letter)

        table_data = [['Type', 'Value']] 
        for key, value in data.items():
            table_data.append([key, value])

        table = Table(table_data)

        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ])

        table.setStyle(style)


        elements = [table]
        pdf.build(elements)

        

        return response

def save_as_json(request):
    if request.method == 'POST':    
        data = request.POST.get('data', '') 
        data = data.replace('\'','\"')
        data = json.loads(data)
        json_data = json.dumps(data)

        response = HttpResponse(json_data, content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename="data.json"'

        return response