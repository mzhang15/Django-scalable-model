from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse, path
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse

from .forms import MappingActionForm
from .models import Mapping

class MappingAdmin(admin.ModelAdmin):
    fields = ['min_shard', 'max_shard', 'perm', 'target1', 'target2']
    list_display = (
        'min_shard',
        'max_shard',
        'perm',
        'target1',
        'target2',
    )
    # list_select_related = (
    #     'id'
    # )

    # def get_urls(self):
    #     urls = super().get_urls
    #     custom_urls = [
    #         path('migrate/', self.process_migrate),
    #     ]
    #     return custom_urls + urls

    def mapping_actions(self, obj):
        return format_html(
            '<a class="button" href="{}">Migrate</a>',
            reverse('admin:migrate', args=[obj.pk])
        )
    # mapping_actions.short_description = 'Mapping Actions'
    # mapping_actions.allow_tags = True

    def process_migrate(self, request, mapping_id, *args, **kwargs):
        return self.process_action(
            request = request,
            mapping_id = mapping_id,
            action_form = MappingActionForm,
        )

    def process_action(self, request, mapping_id, action_form):
        mapping = self.get_object(request, mapping_id)
        if request.method != 'POST':
            form = action_form()
        else:
            form = action_form(request.POST)
            if form.is_valid():
                try:
                    form.save(mapping, request.target)
                except:
                    # If save() raised, the form will a have a non
                    # field error containing an informative message.
                    pass
                else:
                    self.message_user(request, 'Success')
                    url = reverse(
                        'admin:account_account_change',
                        args=[mapping.pk],
                        current_app=self.admin_site.name,
                    )
                    return HttpResponseRedirect(url)
        context = self.admin_site.each_context(request)
        context['opts'] = self.model._meta
        context['form'] = form
        context['mapping'] = mapping
        return TemplateResponse(
            request,
            'admin/scalable/mapping/mapping_action.html',
            context,
        )

admin.site.register(Mapping, MappingAdmin)

