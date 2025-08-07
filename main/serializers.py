from rest_framework import serializers
from .models import CV


class CVSerializer(serializers.ModelSerializer):
    """Serializer for CV model."""
    
    class Meta:
        model = CV
        fields = [
            'id', 'firstname', 'lastname', 'skills', 
            'projects', 'bio', 'contacts', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_contacts(self, value):
        """Validate contacts field."""
        if not value.strip():
            raise serializers.ValidationError("Contact information cannot be empty.")
        return value
    
    def validate_bio(self, value):
        """Validate bio field."""
        if not value.strip():
            raise serializers.ValidationError("Bio cannot be empty.")
        if len(value) < 10:
            raise serializers.ValidationError("Bio must be at least 10 characters long.")
        return value


class CVListSerializer(serializers.ModelSerializer):
    """Simplified serializer for CV list view."""
    
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = CV
        fields = ['id', 'full_name', 'skills', 'created_at']
    
    def get_full_name(self, obj):
        """Get the full name of the CV."""
        return obj.get_full_name() 