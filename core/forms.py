from django import forms
from core.models import ProductReview

class ProductReviewForms(forms.ModelForm):
    review = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': "Write a Review"}
        ))

    class Meta:
        model = ProductReview
        fields = ['review', 'ratings']