from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Recipe, Comment, Rating

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'category', 'difficulty', 'prep_time', 'cook_time', 'servings', 'ingredients', 'instructions', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Recipe name...'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': 'Short description...'}),
            'category': forms.Select(attrs={'class': 'form-input'}),
            'difficulty': forms.Select(attrs={'class': 'form-input'}),
            'prep_time': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Minutes'}),
            'cook_time': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Minutes'}),
            'servings': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Servings'}),
            'ingredients': forms.Textarea(attrs={'class': 'form-input', 'rows': 6, 'placeholder': 'One ingredient per line:\n2 cups flour\n1 tsp salt\n...'}),
            'instructions': forms.Textarea(attrs={'class': 'form-input', 'rows': 8, 'placeholder': 'One step per line:\nPreheat oven to 350°F\nMix dry ingredients\n...'}),
            'image': forms.FileInput(attrs={'class': 'form-input'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': 'Share your thoughts...'}),
        }

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['score']

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Email'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Username'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-input', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-input', 'placeholder': 'Confirm password'})
