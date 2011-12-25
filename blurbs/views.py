import json
from django.views.generic import TemplateView
from blurbs.models import Blurb
from django.shortcuts import render

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

