from django import forms
from PIL import Image
from master.models import OnBoardingScreens
from django.core.exceptions import ValidationError
from io import BytesIO

class OnBoardingScreenAdminForm(forms.ModelForm):
    class Meta:
        model = OnBoardingScreens
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        image = cleaned_data.get('image')

        if image:
             # Read the file content from the in-memory uploaded file
            file_content = BytesIO(image.read())
            image = Image.open(file_content)
            width, height = image.size
            required_width = 720  
            required_height = 1280 

            if width != required_width or height != required_height:
                raise ValidationError("The image should be in WxH 720x1280 dimension.")
