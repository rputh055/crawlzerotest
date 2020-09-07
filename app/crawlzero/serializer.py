from rest_framework import serializers
from .models import File

class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ('file',) 

    def clean_file(self):
        file = self.cleaned_data['file']
        ext = file.name.split('.')[-1].lower()
        if ext not in ["xls", "csv", "xlsx"]:
            raise serializers.ValidationError("Only xls, csv and xlsx files are allowed.")
        # return cleaned data is very important.
        return file