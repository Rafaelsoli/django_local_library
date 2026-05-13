import datetime
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from catalog.models import BookInstance

class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text="insira uma data entre agora e 4 semanas (padrão 3)")
    # aqui deu ruim pq eu coloquei o Date e não date, eh case sensitive esse trem
    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        if data < datetime.date.today():
            raise ValidationError(_('Data invalida - renovação no passado'))
        
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Data invalida - renovação marcada para mais de 4 semanas'))
        
        return data
    class Meta:
        model = BookInstance
        fields = ['due_back']
        labels = {'due_back': _('Renewal date')}
        help_text = {'due_back': _('Enter a date between now and 4 weeks (default 3)')}