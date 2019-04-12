from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import TrackerCertification, BadReason, PixelProblem, StripProblem, TrackingProblem
from django.forms import ModelForm, RadioSelect, CheckboxSelectMultiple, ModelMultipleChoiceField
from checklists.forms import ChecklistFormMixin

class CertifyForm(ModelForm):

    pixel = forms.ChoiceField(choices=TrackerCertification.SUBCOMPONENT_STATUS_CHOICES, widget=forms.RadioSelect())
    strip = forms.ChoiceField(choices=TrackerCertification.SUBCOMPONENT_STATUS_CHOICES, widget=forms.RadioSelect())
    tracking = forms.ChoiceField(choices=TrackerCertification.SUBCOMPONENT_STATUS_CHOICES, widget=forms.RadioSelect())

    date = forms.DateField(
        widget=forms.SelectDateWidget(years=range(2017, timezone.now().year + 2)),
        initial=timezone.now
    )

    class Meta:
        model = TrackerCertification
        fields = [
            'pixel',
            'strip',
            'tracking',
            'pixel_lowstat',
            'strip_lowstat',
            'tracking_lowstat',
            'pixel_problems',
            'strip_problems',
            'tracking_problems',
            'bad_reason',
            'comment',
            'reference_runreconstruction',
            'date',
            'trackermap',
        ]

    def clean(self):
        cleaned_data = super(CertifyForm, self).clean()
        return cleaned_data
'''
        is_sistrip_bad = cleaned_data.get('sistrip') == 'Bad'
        is_tracking_good = cleaned_data.get('tracking') == 'Good'

        if is_sistrip_bad and is_tracking_good:
            self.add_error(None, ValidationError(
                "Tracking can not be GOOD if SiStrip is BAD. Please correct."))

        run_type = cleaned_data.get('type')
        reference_run = cleaned_data.get('reference_run')

        if run_type and reference_run:
            if run_type.runtype != reference_run.runtype:
                self.add_error(None, ValidationError(
                    "Reference run is incompatible with selected Type. ({} != {})"
                        .format(run_type.runtype, reference_run.runtype)))
'''

class CertifyFormWithChecklistForm(CertifyForm, ChecklistFormMixin):
    pass
