from django import forms
from django.db.models import fields
from django.forms import ModelForm
from django.contrib.auth.forms import AuthenticationForm
from ddi.models import *
from ddi.mikrotik import MikrotikAPI

# class FormRouter(ModelForm):
#     class Meta:
#         model = Router
#         fields = '__all__'

#         widgets = {
#             'config': forms.TextInput({'class':'form-control'}),
#             'value': forms.TextInput({'class':'form-control'}),
#         }

class FormOS(ModelForm):
    class Meta:
        model = OS
        fields = '__all__'

        widgets = {
            'name': forms.TextInput({'class':'form-control', 'placeholder':'Press Enter to add OS'}),
        }

class FormIpAddress(ModelForm):
    class Meta:
        model = Ip_Address
        fields = '__all__'

        widgets = {
            'ip_address': forms.TextInput({'class':'form-control input-mask-trigger','data-inputmask':"'alias':'ip'"}),
            'hostname': forms.TextInput({'class':'form-control ps-0 form-control-line'}),
            'description': forms.TextInput({'class':'form-control ps-0 form-control-line'}),
            'subnet': forms.Select({'class':'form-control'}),
            'os': forms.Select({'class':'form-control'}),
            'username': forms.TextInput({'class':'form-control'}),
            'password': forms.PasswordInput({'class':'form-control','data-toggle':'password'}),
        }

class FormSubnet(ModelForm):
    class Meta:
        model = Subnet
        fields = '__all__'

        widgets = {
            'netmask': forms.NumberInput({'class':'form-control ps-0 form-control-line'}),
            'ip_network': forms.TextInput({'class':'form-control input-mask-trigger','data-inputmask':"'alias':'ip'"}),
            'ip_broadcast': forms.TextInput({'class':'form-control input-mask-trigger','data-inputmask':"'alias':'ip'"}),
            'description': forms.TextInput({'class':'form-control ps-0 form-control-line'}),
        }

class FormDHCP_Server(ModelForm):
    class Meta:
        model = Dhcp_Server
        fields = '__all__'

        widgets = {
            'name': forms.TextInput({'class':'form-control'}),
            'subnet': forms.TextInput({'class':'form-control','placeholder':'ex : 192.168.1.0/24'}),
            'ip_start': forms.TextInput({'class':'form-control input-mask-trigger','data-inputmask':"'alias':'ip'"}),
            'ip_end': forms.TextInput({'class':'form-control input-mask-trigger','data-inputmask':"'alias':'ip'"}),
            'gateway': forms.TextInput({'class':'form-control input-mask-trigger','data-inputmask':"'alias':'ip'"}),
            'dns': forms.TextInput({'class':'form-control','placeholder':'user comma for more than one, ex : 8.8.8.8,8.8.4.4'}),
            'idm_network': forms.HiddenInput(),
            'idm_pool': forms.HiddenInput(),
            'idm_dhcp': forms.HiddenInput(),
        }

class FormDHCP_Static(ModelForm):
    class Meta:
        model = Dhcp_Static
        fields = '__all__'
        
        widgets = {
            'name': forms.TextInput({'class':'form-control'}),
            'mac': forms.TextInput({'class':'form-control input-mask-trigger','data-inputmask':"'alias':'mac'"}),
            'ip': forms.TextInput({'class':'form-control input-mask-trigger','data-inputmask':"'alias':'ip'"}),
            'description': forms.Textarea({'class':'form-control'}),
            'id': forms.HiddenInput(),
        }

class FormDomain(ModelForm):
    class Meta:
        model = Domain
        fields = '__all__'

        widgets = {
            'domain': forms.TextInput({'class':'form-control'}),
            'ip': forms.TextInput({'class':'form-control input-mask-trigger','data-inputmask':"'alias':'ip'"}),
            'description': forms.Textarea({'class':'form-control'}),
        }

class FormSubDomain(ModelForm):
    class Meta:
        model = Subdomain
        fields = '__all__'

        widgets = {
            'id': forms.HiddenInput(),
            'domain': forms.Select({'class':'form-control'}),
            'subdomain': forms.TextInput({'class':'form-control'}),
            'ip': forms.TextInput({'class':'form-control input-mask-trigger','data-inputmask':"'alias':'ip'"}),
            'description': forms.Textarea({'class':'form-control'}),
        }

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Username Here ...'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Enter Password Here ...'}))