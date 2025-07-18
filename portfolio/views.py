from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView, DeleteView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Portfolio


# Function Based View for List
def applicant_list(request):
    """List all applicants with portfolios"""
    users_with_portfolios = User.objects.filter(portfolio__isnull=False).select_related('portfolio',
                                                                                        'portfolio__project')
    context = {
        'applicants': users_with_portfolios,
        'position': 'Junior Developer'
    }
    return render(request, 'applicant_list.html', context)


# Class Based View for Detail
class ApplicantDetailView(DetailView):
    model = User
    template_name = 'applicant_detail.html'
    context_object_name = 'applicant'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['portfolio'] = self.object.portfolio
        except Portfolio.DoesNotExist:
            context['portfolio'] = None
        return context


# Class Based View for Delete
class ApplicantDeleteView(DeleteView):
    model = User
    slug_field = 'username'
    slug_url_kwarg = 'username'
    success_url = reverse_lazy('portfolio:list')

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        messages.success(request, f'Applicant {user.get_full_name()} has been deleted successfully.')
        return super().delete(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        # Direct delete without confirmation page
        return self.delete(request, *args, **kwargs)
