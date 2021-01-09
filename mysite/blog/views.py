from django.template import loader
from django.http import HttpResponse
from django.views.generic import View
from django.views.generic.base import TemplateView


# Create your views here.
class IndexView(TemplateView):
  
  template_name = "blog/index.html"
  