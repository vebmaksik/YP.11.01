from django import forms
from .models import Equipment, Workshop, Category, FixerProfile, Review

class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = ['name', 'description', 'price', 'level', 'color', 'photo', 'is_exists', 'category', 'workshop', 'collection']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class WorkshopForm(forms.ModelForm):
    class Meta:
        model = Workshop
        fields = ['name', 'description', 'logo']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class FixerProfileForm(forms.ModelForm):
    class Meta:
        model = FixerProfile
        fields = ['user', 'role', 'avatar', 'bio']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['equipment', 'user', 'rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4}),
        }