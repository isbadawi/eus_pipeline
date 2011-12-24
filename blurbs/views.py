from django.views.generic import TemplateView
from blurbs.models import Blurb

class PipelineView(TemplateView):
    template_name = 'blurbs/generate.html'

    def get_context_data(self, **kwargs):
        context = super(PipelineView, self).get_context_data(**kwargs)
        context['blurbs'] = Blurb.objects.active()
        return context
