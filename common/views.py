from django.views.generic import TemplateView


class AboutMeView(TemplateView):
    template_name = 'about_me.html'


class ContactInfoView(TemplateView):
    template_name = 'contact_info.html'
