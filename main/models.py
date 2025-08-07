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


class RequestLog(models.Model):
    """Model to log HTTP requests for auditing and monitoring."""
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Timestamp")
    method = models.CharField(max_length=10, verbose_name="HTTP Method")
    path = models.CharField(max_length=255, verbose_name="Request Path")
    query_string = models.TextField(blank=True, verbose_name="Query String")
    remote_ip = models.GenericIPAddressField(verbose_name="Remote IP")
    user_agent = models.TextField(blank=True, verbose_name="User Agent")
    response_status = models.IntegerField(verbose_name="Response Status")
    response_time = models.FloatField(verbose_name="Response Time (seconds)")
    user = models.ForeignKey(
        'auth.User', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        verbose_name="User"
    )
    is_authenticated = models.BooleanField(default=False, verbose_name="Is Authenticated")

    class Meta:
        verbose_name = "Request Log"
        verbose_name_plural = "Request Logs"
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['timestamp']),
            models.Index(fields=['method']),
            models.Index(fields=['path']),
            models.Index(fields=['response_status']),
        ]

    def __str__(self):
        return f"{self.method} {self.path} - {self.timestamp}"

    def get_duration_display(self):
        """Return formatted response time."""
        if self.response_time < 1:
            return f"{self.response_time * 1000:.0f}ms"
        return f"{self.response_time:.2f}s"
