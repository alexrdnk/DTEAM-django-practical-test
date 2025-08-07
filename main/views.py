from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import CV


class CVListView(ListView):
    """View to display a list of all CVs."""
    model = CV
    template_name = 'main/cv_list.html'
    context_object_name = 'cvs'
    paginate_by = 10

    def get_queryset(self):
        """Return all CVs ordered by creation date."""
        return CV.objects.all().order_by('-created_at')


class CVDetailView(DetailView):
    """View to display a single CV in detail."""
    model = CV
    template_name = 'main/cv_detail.html'
    context_object_name = 'cv'

    def get_object(self, queryset=None):
        """Get the CV object by ID."""
        return get_object_or_404(CV, pk=self.kwargs.get('pk'))
