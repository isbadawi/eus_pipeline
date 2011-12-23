from form_utils.forms import BetterModelForm
from blurbs.models import Blurb

class BlurbForm(BetterModelForm):
    class Meta:
        model = Blurb
        fieldsets = [
           ('Contact information', {
               'fields': ['author', 'email']
           }),
           ('Blurb', {
              'fields': ['title', 'body', 'run_until', 'comments']
           }),
        ] 
