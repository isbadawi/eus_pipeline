# Create your views here.

from django.views.generic.edit import CreateView
from blurbs.forms import BlurbForm

class SubmitBlurbView(CreateView):
    form_class = BlurbForm
    template_name = 'blurbs/submit.html'
