from django.forms import ModelForm

class AuthorForm(ModelForm):
    class Meta:
        model = Author
        #fields = ['name', 'title', 'birth_date']
        #exclude = ['smth']
        fields = ['__all__']
        widgets = {
            'name': Textarea(attrs={'cols': 80, 'rows': 20}),
        }
        labels = {
            'name': _('Writer')
        }
        help_texts = {
            'name': _('Some useful help text.')
        }
        error_message = {
            'name': {
                'max_length': _('This writers name is too long')
            }
        }

class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ['name', 'authors']