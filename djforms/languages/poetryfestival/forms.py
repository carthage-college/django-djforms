from django import forms

class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField(label='Email')
    poem_title = forms.CharField(
        max_length=200, label="Title of the poem"
    )
    poem_author = forms.CharField(
        max_length=100, label="Author of the poem"
    )
    poem_language = forms.CharField(
        max_length=50, label = "Language of the poem"
    )
    time_slot = forms.CharField(
        required = False, widget = forms.Textarea,
        label = """
            Please note if you have a preference for a particular time slot
            in which you wish to perform
        """,
        help_text = """
            (Note: Requests will be strongly considered but not guaranteed)
            """
        )
    comments = forms.CharField(
        required = False, widget = forms.Textarea,
        label = "Any Questions or comments?"
    )

