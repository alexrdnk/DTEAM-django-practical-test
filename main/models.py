from django.db import models


class CV(models.Model):
    """CV model to store professional information."""
    firstname = models.CharField(max_length=100, verbose_name="First Name")
    lastname = models.CharField(max_length=100, verbose_name="Last Name")
    skills = models.TextField(verbose_name="Skills", help_text="List your technical and soft skills")
    projects = models.TextField(verbose_name="Projects", help_text="Describe your key projects and achievements")
    bio = models.TextField(verbose_name="Bio", help_text="Professional summary and background")
    contacts = models.TextField(verbose_name="Contact Information", help_text="Email, phone, LinkedIn, etc.")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        verbose_name = "CV"
        verbose_name_plural = "CVs"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.firstname} {self.lastname}"

    def get_full_name(self):
        """Return the full name of the person."""
        return f"{self.firstname} {self.lastname}"
