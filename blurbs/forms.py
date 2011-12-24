from form_utils.forms import BetterModelForm
from django import forms
from blurbs.models import Blurb
import datetime

class BlurbForm(BetterModelForm):
    LIFESPAN_CHOICES = [
        (i, '%d week%s' % (i, 's' if i > 1 else '')) for i in range(1, 6)
    ]
    run_for = forms.TypedChoiceField(
        coerce=lambda i: datetime.timedelta(weeks=int(i) - 1),
        empty_value=None,
        choices=LIFESPAN_CHOICES
    )
    class Meta:
        model = Blurb
        fieldsets = [
           ('Contact information', {
               'fields': ['name', 'email'],
           }),
           ('Blurb', {
              'fields': ['title', 'body', 'run_for', 'comments']
           }),
        ] 

    def save(self, commit=True):
        m = super(BlurbForm, self).save(commit=False)
        d = datetime.date.today()
        sunday = d + datetime.timedelta(days=6 - d.weekday())
        m.run_until = sunday + self.cleaned_data['run_for']
        if commit:
            m.save()
        return m

