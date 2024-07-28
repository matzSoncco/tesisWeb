from typing import Any
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models.Ppe import Ppe
from .models.PpeLoan import PpeLoan, PpeLoanDetail
from .models.Equipment import Equipment
from .models.Material import Material
from .models.Tool import Tool
from .models.Worker import Worker
from .models.Loan import Loan
from .models.Unit import Unit

class AdminLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(AdminLoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(widget=forms.TextInput(attrs={
        "class": "input",
        "type": "text",
        "placeholder": "Ingrese su nombre de usuario"
    }), max_length=150)

    password = forms.CharField(widget=forms.TextInput(attrs={
        "class": "input",
        "type": "password",
        "placeholder": "Ingrese su contraseña"
    }))

    class Meta:
        model = User
        fields = ['username', 'password']


class AdminSignUpForm(UserCreationForm):
    name = forms.CharField(widget=forms.TextInput(attrs={
        "class": "input",
        "type": "text",
        "placeholder": "Ingrese sus nombres y apellidos"
    }), max_length=150,)

    username = forms.CharField(widget=forms.TextInput(attrs={
        "class": "input",
        "type": "text",
        "placeholder": "Cree su nombre de Usuario"
    }), max_length=150)

    email = forms.CharField(widget=forms.TextInput(attrs={
        "class": "input",
        "type": "email",
        "placeholder": "Ingrese su correo"
    }), max_length=150)

    phoneNumber = forms.CharField(widget=forms.TextInput(attrs={
        "class": "input",
        "type": "text",
        "placeholder": "Ingrese su número de celular"
    }), max_length=9)

    dni = forms.CharField(widget=forms.TextInput(attrs={
        "class": "input",
        "type": "text",
        "placeholder": "Ingrese su número de DNI"
    }), max_length=8)

    password1 = forms.CharField(widget=forms.TextInput(attrs={
        "class": "input",
        "type": "password",
        "placeholder": "Cree una contraseña"
    }))

    password2 = forms.CharField(widget=forms.TextInput(attrs={
        "class": "input",
        "type": "password",
        "placeholder": "Ingrese la contraseña nuevamente"
    }))

    class Meta:
        model = User
        fields = ('name', 'username', 'email', 'phoneNumber', 'dni', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = True  # Hacer que este usuario sea un administrador
        if commit:
            user.save()
        return user

class CreatePpeForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={
        "class": "input",
        "type": "text",
        "placeholder": "Ingrese el nombre del EPP"
    }))

    new_unit = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Nueva unidad'}))

    class Meta:
        model = Ppe
        fields = ['name', 'unit', 'image']
        widgets = {
            'image': forms.FileInput(attrs={
                "class": "input",
                "type": "file",
            }),
            'unit': forms.Select(attrs={'class': 'select-unit'}),
        }

    def __init__(self, *args, **kwargs):
        super(CreatePpeForm, self).__init__(*args, **kwargs)
        self.fields['image'].required = False
        self.fields['unit'].queryset = Unit.get_default_units()
        self.fields['unit'].empty_label = "Seleccione la unidad"
        
    def clean(self):
        cleaned_data = super().clean()
        new_unit = cleaned_data.get('new_unit')

        if new_unit:
            unit, created = Unit.objects.get_or_create(name=new_unit)
            cleaned_data['unit'] = unit

        print(f"Cleaned data: {cleaned_data}")  # Añade este print para depuración
        return cleaned_data

class PpeForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={
        "class": "input",
        "type": "text",
        "placeholder": "Ingrese el nombre del EPP"
    }))

    unitCost = forms.FloatField(widget=forms.NumberInput(attrs={
        "class": "input",
        "type": "number",
        "placeholder": "Ingrese el costo unitario"
    }))

    stock = forms.IntegerField(widget=forms.NumberInput(attrs={
        "class": "input",
        "type": "number",
        "placeholder": "Ingrese el stock ideal"
    }))

    duration = forms.IntegerField(widget=forms.NumberInput(attrs={
        "class": "input",
        "type": "number",
        "placeholder": "Ingrese la duracion del EPP"
    }))

    guideNumber = forms.CharField(widget=forms.TextInput(attrs={
        "class": "input",
        "type": "text",
        "placeholder": "Ingrese la el número de guía"
    }))
    
    quantity = forms.IntegerField(widget=forms.NumberInput(attrs={
        "class": "input",
        "type": "number",
        "placeholder": "Ingrese la cantidad a añadir",
        "min": "1",
        "max": "99999"
    }))

    creationDate = forms.DateField(widget=forms.DateInput(attrs={
        "class": "input",
        "type": "date"
    }))
    class Meta:
        model = Ppe
        fields = ['name', 'unitCost', 'stock', 'unit', 'guideNumber', 'image', 'duration', 'creationDate', 'quantity']
        widgets = {
            'image': forms.FileInput(attrs={
                "class": "input",
                "type": "file",
            }),
            'unit': forms.Select(attrs={'class': 'select-unit'}),
        }

    def __init__(self, *args, **kwargs):
        super(PpeForm, self).__init__(*args, **kwargs)
        self.fields['image'].required = False
        self.fields['unit'].queryset = Unit.get_default_units()
        self.fields['unit'].empty_label = "Select unit"
        
    def clean(self):
        cleaned_data = super().clean()
        new_unit = cleaned_data.get('new_unit')

        if new_unit:
            unit, created = Unit.objects.get_or_create(name=new_unit)
            cleaned_data['unit'] = unit

        return cleaned_data

class EquipmentForm(forms.ModelForm):
    level = forms.ChoiceField(widget=forms.Select(attrs={
        "class": "input",
        "placeholder": "Seleccione el nivel"
    }))
    class Meta:
        model = Equipment
        fields = ['name', 'level', 'stock', 'guideNumber', 'image']
        widgets = {
            'name': forms.TextInput(attrs={
                "class": "input",
                "type": "text",
                "placeholder": "Ingrese el nombre del equipo"
            }),
            'stock': forms.NumberInput(attrs={
                "class": "input",
                "type": "number",
                "placeholder": "Ingrese el stock"
            }),
            'guideNumber': forms.TextInput(attrs={
                "class": "input",
                "type": "text",
                "placeholder": "Ingrese el número de guía"
            }),
            'image': forms.FileInput(attrs={
                "class": "input",
                "type": "file",
            })
        }

    def __init__(self, *args, **kwargs):
        super(EquipmentForm, self).__init__(*args, **kwargs)
        self.fields['image'].required = False

class MaterialForm(forms.ModelForm):
    unit = forms.ChoiceField(choices=[('kg', 'Kilogramo'), ('m', 'Metro'), ('ltr', 'Litro')], widget=forms.Select(attrs={
        "class": "input",
        "placeholder": "Seleccione la unidad"
    }))

    class Meta:
        model = Material
        fields = ['name', 'stock', 'unit', 'guideNumber', 'image']
        widgets = {
            'name': forms.TextInput(attrs={
                "class": "input",
                "type": "text",
                "placeholder": "Ingrese el nombre del material"
            }),
            'stock': forms.NumberInput(attrs={
                "class": "input",
                "type": "number",
                "placeholder": "Ingrese el stock"
            }),
            'guideNumber': forms.TextInput(attrs={
                "class": "input",
                "type": "text",
                "placeholder": "Ingrese el número de guía"
            }),
            'image': forms.FileInput(attrs={
                "class": "input",
                "type": "file",
            })
        }

    def __init__(self, *args, **kwargs):
        super(MaterialForm, self).__init__(*args, **kwargs)
        self.fields['image'].required = False

class ToolForm(forms.ModelForm):
    level = forms.ChoiceField(widget=forms.Select(attrs={
        "class": "input",
        "placeholder": "Seleccione el nivel"
    }))

    class Meta:
        model = Tool
        fields = ['name', 'level', 'stock', 'guideNumber', 'image']
        widgets = {
            'name': forms.TextInput(attrs={
                "class": "input",
                "type": "text",
                "placeholder": "Ingrese el nombre de la herramienta"
            }),
            'stock': forms.NumberInput(attrs={
                "class": "input",
                "type": "number",
                "placeholder": "Ingrese el stock"
            }),
            'guideNumber': forms.TextInput(attrs={
                "class": "input",
                "type": "text",
                "placeholder": "Ingrese el número de guía"
            }),
            'image': forms.FileInput(attrs={
                "class": "input",
                "type": "file",
            })
        }
    
    def __init__(self, *args, **kwargs):
        super(ToolForm, self).__init__(*args, **kwargs)
        self.fields['image'].required = False

class WorkerForm(forms.ModelForm):
    dni = forms.CharField(widget=forms.TextInput(attrs={
        "class": "input",
        "type": "text",
        "placeholder": "Ingrese su número de DNI"
    }), max_length=8)

    workerStatus = forms.BooleanField(widget=forms.CheckboxInput(attrs={
        'class': 'input',
        'type': 'checkbox'
    }))

    class Meta:
        model = Worker
        fields = ['dni', 'name', 'surname', 'position', 'contractDate', 'workerStatus']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'input',
                'type': 'text',
                'placeholder': 'Ingrese los nombres'
            }),
            'surname': forms.TextInput(attrs={
                'class': 'surname-input',
                'type': 'text',
                'placeholder': 'Ingrese los apellidos'
            }),
            'position': forms.TextInput(attrs={
                'class': 'input',
                'type': 'text',
                'placeholder': 'Ingrese su cargo'
            }),
            'contractDate': forms.DateInput(attrs={
                'class': 'input',
                'type': 'date'
            }),
        }


class LoanForm(forms.ModelForm):
    material = forms.ModelChoiceField(label='Material', queryset=Material.objects.all(), required=True)
    tool = forms.ModelChoiceField(label='Herramienta', queryset=Tool.objects.all(), required=True)
    equipment = forms.ModelChoiceField(label='Equipo', queryset=Equipment.objects.all(), required=True)
    worker = forms.ModelChoiceField(label='Trabajador', queryset=Worker.objects.all(), required=True)
    loanStatus = forms.BooleanField(label='Estado (Devuelto/No devuelto)', required=False)

    class Meta:
        model = Loan
        fields = ['loanDate', 'returnLoanDate', 'worker', 'material', 'tool', 'equipment', 'workOrderCode', 'loanStatus']

        widgets = {
            'loanDate': forms.DateInput(attrs={'type': 'date'}),
            'returnLoanDate': forms.DateInput(attrs={'type': 'date'}),
            'loanStatus': forms.CheckboxInput(attrs={'class': 'status-checkbox'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        worker = cleaned_data.get('worker')
        loan_date = cleaned_data.get('loanDate')
        return_loan_date = cleaned_data.get('returnLoanDate')
    
        if worker and loan_date and return_loan_date:
            # Verificar si hay préstamos existentes para este trabajador en las fechas especificadas
            existing_loans = Loan.objects.filter(
                worker=worker,
                returnLoanDate__gte=return_loan_date,
                loanDate__lte=loan_date,
            ).exclude(pk=self.instance.pk).exists()
            
            if existing_loans:
                raise ValidationError(f'El trabajador ya tiene objetos prestados durante este período.')
        
        return cleaned_data
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['worker'].label_from_instance = self.label_from_instance
        self.fields['material'].label_from_instance = self.label_from_instance
        self.fields['tool'].label_from_instance = self.label_from_instance
        self.fields['equipment'].label_from_instance = self.label_from_instance
    
    def label_from_instance(self, obj):
        if isinstance(obj, Worker):
            return f"{obj.name} {obj.surname}"
        else:
            return obj.name
        
    def clean(self):
        cleaned_data = super().clean()
        worker = cleaned_data.get('worker')
        loan_date = cleaned_data.get('loanDate')
        new_loan_date = cleaned_data.get('newLoanDate')
    
        if worker and loan_date and new_loan_date:
            existing_ppe_loans = PpeLoan.objects.filter(
                worker=worker,
                loanDate__lte=new_loan_date,
                newLoanDate__gte=loan_date 
            ).exclude(pk=self.instance.pk).exists()
            
            if existing_ppe_loans:
                self.existing_ppe_loans  = True
                raise ValidationError(f'El trabajador ya tiene EPPs entregados durante este período.')
        
        return cleaned_data
    
    def _init_(self, *args, **kwargs):
        super()._init_(*args, **kwargs)
        self.fields['worker'].label_from_instance = self.label_from_instance
        
    
    def label_from_instance(self, obj):
        if isinstance(obj, Worker):
            return f"{obj.name} {obj.surname}"
        else:
            return obj.name
        
class PpeLoanForm(forms.ModelForm):
    class Meta:
        model = PpeLoan
        fields = ['worker', 'loanDate', 'newLoanDate', 'manager', 'description']

    def clean(self):
        cleaned_data = super().clean()
        worker = cleaned_data.get('worker')
        loan_date = cleaned_data.get('loanDate')
        new_loan_date = cleaned_data.get('newLoanDate')
    
        if worker and loan_date and new_loan_date:
            existing_ppe_loans = PpeLoan.objects.filter(
                worker=worker,
                loanDate__lte=new_loan_date,
                newLoanDate__gte=loan_date 
            ).exclude(pk=self.instance.pk).exists()
            
            if existing_ppe_loans:
                self.existing_ppe_loans  = True
                raise ValidationError(f'El trabajador ya tiene EPPs entregados durante este período.')
        
        return cleaned_data
    
    def _init_(self, *args, **kwargs):
        super()._init_(*args, **kwargs)
        self.fields['worker'].label_from_instance = self.label_from_instance
        
    
    def label_from_instance(self, obj):
        if isinstance(obj, Worker):
            return f"{obj.name} {obj.surname}"
        else:
            return obj.name
        
class PpeLoanDetailForm(forms.ModelForm):
    class Meta:
        model = PpeLoanDetail
        fields = ['ppe', 'quantity']

class ExceptionPpeLoanForm(forms.ModelForm):
    ppe = forms.ModelChoiceField(label='EPP', queryset=Ppe.objects.all(), required=True)
    worker = forms.ModelChoiceField(label='Trabajador', queryset=Worker.objects.all(), required=True)

    class Meta:
        model = PpeLoan
        fields = ['loanDate', 'newLoanDate', 'worker', 'ppe', 'manager', 'description']

        widgets = {
            'loanDate': forms.DateInput(attrs={'type': 'date'}),
            'newLoanDate': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def _init_(self, *args, **kwargs):
        super()._init_(*args, **kwargs)
        self.fields['worker'].label_from_instance = self.label_from_instance
        self.fields['ppe'].label_from_instance = self.label_from_instance
    
    def label_from_instance(self, obj):
        if isinstance(obj, Worker):
            return f"{obj.name} {obj.surname}"
        else:
            return obj.name