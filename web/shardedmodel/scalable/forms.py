from django import forms

from .models import Mapping
# from . import errors

class MappingActionForm(forms.Form):
    target = forms.CharField(
        required = True,
        help_text = 'target host to split data',
        widget = forms.Textarea,
    )

    def form_action(self, mapping, target):
        return Mapping.migrate(self, mapping, target)

    def save(self, mapping, target):
        # try:
        mapping, action = self.form_action(mapping, target)
        # except errors.Error as e:
        #     error_message = str(e)
        #     self.add_error(None, error_message)
        #     raise

        return mapping, action