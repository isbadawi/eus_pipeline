import json
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.shortcuts import render
from blurbs.models import Blurb
from blurbs.forms import BlurbForm
from blurbs.forms import DocumentFormSet

class CreateBlurbView(CreateView):
    template_name = 'blurbs/submit.html'
    form_class = BlurbForm
    success_url = '/blurbs/submitted/'

    def get_context_data(self, **kwargs):
        context = super(CreateBlurbView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['document_formset'] = DocumentFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            context['document_formset'] = DocumentFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        document_form = context['document_formset']
        if document_form.is_valid():
            self.object = form.save()
            document_form.instance = self.object
            document_form.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

class PipelineView(TemplateView):
    template_name = 'blurbs/generate.html'

    def get_context_data(self, **kwargs):
        context = super(PipelineView, self).get_context_data(**kwargs)
        context['blurbs'] = Blurb.objects.active()
        return context

    def _prepare(self, blurb):
        blurb = blurb.replace('<p>', '<p style="margin: 0; margin-top: 3px; margin-bottom: 10px; padding: 0; font-size: 13px; font-weight: normal; color: #535353; line-height: 22px; text-align: justify;">')
        blurb = blurb.replace('<a ', '<a style="color: #ff0000" ')
        return blurb

    def post(self, request, *args, **kwargs):
        pipeline = json.loads(request.POST.get('pipeline', ''))
        headers = pipeline['headers']
        ids = sum([h['blurbs'] for h in headers], [])
        blurbs = Blurb.objects.in_bulk(ids)
        index = 1
        for i, header in enumerate(headers):
            header['entries'] = []
            for blurb in header['blurbs']:
                header['entries'].append({
                    'index': index,
                    'title': blurbs[blurb].title 
                })
                index += 1
            header['letter'] = chr(ord('a') + i)
        blurbs = [blurbs[i] for i in ids]
        blurbs = [{
            'index': i,
            'title': blurb.title,
            'body': self._prepare(blurb.body) 
        } for i, blurb in enumerate(blurbs, 1)]
        return render(request, 'pipeline.html', {
            'sidebar_entries': headers,
            'stories': blurbs,
            'events': pipeline['events']
        })

