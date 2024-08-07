from django import forms
from .models import Expense, Category


class ExpenseSearchForm(forms.ModelForm):
    ORDER_BY_CHOICES = [
        ('category__name', 'Category A-Z'),
        ('-category__name', 'Category Z-A'),
        ('-date', 'Date Descending'),
        ('date', 'Date Ascending'),
    ]

    class Meta:
        model = Expense
        fields = ('name',)

    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    categories = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        queryset=Category.objects.all(),
        required=False,
    )
    order_by = forms.ChoiceField(
        choices=ORDER_BY_CHOICES,
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = False

    def clean(self):
        cleaned_data = super().clean()
        date_from = cleaned_data.get('date_from')
        date_to = cleaned_data.get('date_to')

        if date_from and date_to:
            if date_to < date_from:
                raise forms.ValidationError(
                    "The end date must be later than the start date."
                )

        return cleaned_data
