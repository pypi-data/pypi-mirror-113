"""SatNOGS DB django base Forms class"""
from bootstrap_modal_forms.forms import BSModalModelForm
from django.core.exceptions import ValidationError
from django.forms import TextInput
from django.utils.translation import gettext_lazy as _

from db.base.models import SatelliteEntry, Transmitter, TransmitterEntry


def existing_uuid(value):
    """ensures the UUID is existing and valid"""
    try:
        Transmitter.objects.get(uuid=value)
    except Transmitter.DoesNotExist as error:
        raise ValidationError(
            _('%(value)s is not a valid uuid'),
            code='invalid',
            params={'value': value},
        ) from error


class TransmitterCreateForm(BSModalModelForm):  # pylint: disable=too-many-ancestors
    """Model Form class for TransmitterEntry objects"""
    class Meta:
        model = TransmitterEntry
        fields = [
            'description', 'type', 'status', 'uplink_low', 'uplink_high', 'uplink_drift',
            'uplink_mode', 'downlink_low', 'downlink_high', 'downlink_drift', 'downlink_mode',
            'invert', 'baud', 'citation', 'service', 'coordination', 'coordination_url'
        ]
        labels = {
            'downlink_low': _('Downlink freq.'),
            'uplink_low': _('Uplink freq.'),
            'invert': _('Inverted Transponder?'),
        }
        widgets = {
            'description': TextInput(),
        }


class TransmitterUpdateForm(BSModalModelForm):  # pylint: disable=too-many-ancestors
    """Model Form class for TransmitterEntry objects"""
    class Meta:
        model = TransmitterEntry
        fields = [
            'description', 'type', 'status', 'uplink_low', 'uplink_high', 'uplink_drift',
            'uplink_mode', 'downlink_low', 'downlink_high', 'downlink_drift', 'downlink_mode',
            'invert', 'baud', 'citation', 'service', 'coordination', 'coordination_url'
        ]
        labels = {
            'downlink_low': _('Downlink freq.'),
            'uplink_low': _('Uplink freq.'),
            'invert': _('Inverted Transponder?'),
        }
        widgets = {
            'description': TextInput(),
        }


class SatelliteCreateForm(BSModalModelForm):
    """Form that uses django-bootstrap-modal-forms for satellite editing"""
    class Meta:
        model = SatelliteEntry
        fields = [
            'norad_cat_id', 'norad_follow_id', 'name', 'names', 'description', 'operator',
            'status', 'countries', 'website', 'dashboard_url', 'launched', 'deployed', 'decayed',
            'image', 'citation'
        ]
        labels = {
            'norad_cat_id': _('Norad ID'),
            'norad_follow_id': _('Followed Norad ID'),
            'names': _('Other names'),
            'countries': _('Countries of Origin'),
            'launched': _('Launch Date'),
            'deployed': _('Deploy Date'),
            'decayed': _('Re-entry Date'),
            'description': _('Description'),
            'dashboard_url': _('Dashboard URL'),
            'operator': _('Owner/Operator'),
        }
        widgets = {'names': TextInput()}


class SatelliteUpdateForm(BSModalModelForm):
    """Form that uses django-bootstrap-modal-forms for satellite editing"""
    class Meta:
        model = SatelliteEntry
        fields = [
            'norad_cat_id', 'norad_follow_id', 'name', 'names', 'description', 'operator',
            'status', 'countries', 'website', 'dashboard_url', 'launched', 'deployed', 'decayed',
            'image', 'citation'
        ]
        labels = {
            'norad_cat_id': _('Norad ID'),
            'norad_follow_id': _('Followed Norad ID'),
            'names': _('Other names'),
            'countries': _('Countries of Origin'),
            'launched': _('Launch Date'),
            'deployed': _('Deploy Date'),
            'decayed': _('Re-entry Date'),
            'description': _('Description'),
            'dashboard_url': _('Dashboard URL'),
            'operator': _('Owner/Operator'),
        }
        widgets = {'names': TextInput()}
