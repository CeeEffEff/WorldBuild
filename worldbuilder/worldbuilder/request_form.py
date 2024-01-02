from django import forms

LOCATIONS = (
    ("Covent Garden", "Covent Garden"),
    ("Soho", "Soho"),
    ("West End", "West End"),
    ("South Bank", "South Bank"),
    ("Shoreditch", "Shoreditch"),
    ("Hoxton", "Hoxton"),
    ("Islington", "Islington"),
    ("Camden", "Camden"),
    ("Tanygrisiau", "Tanygrisiau")
)
VENUE_TYPES = (
    ("restaurants", "restaurants"),
    ("bars and pubs", "bars and pubs"),
    ("theatre shows", "theatre shows"),
    ("things to do", "things to do"),
)


class RequestForm(forms.Form):
    location = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=LOCATIONS
    )
    venue_type = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=VENUE_TYPES
    )
    tags = forms.CharField(
        initial="good for couples, romantic",
        widget=forms.Textarea
    )
    use_timeout_content = forms.BooleanField(
        widget=forms.CheckboxInput,
        required=False,
        initial=True
    )

    def __init__(self, *args, **kwargs):
        super(RequestForm, self).__init__(*args, **kwargs)
        self.fields['tags'].widget.attrs['cols'] = 40
        self.fields['tags'].widget.attrs['rows'] = 6
