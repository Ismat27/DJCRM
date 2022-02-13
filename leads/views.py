from django.core.mail import send_mail
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from .models import Agent, Lead
from .forms import LeadForm, ModelLeadForm, CustomUserCreationForm
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class SignUpView(generic.CreateView):
    template_name = 'registration/signup.html'
    form_class = CustomUserCreationForm

    def get_success_url(self) :
        return reverse('login')

class LandingPageView(generic.TemplateView):
    template_name = "landing.html"

class LeadListView(LoginRequiredMixin, generic.ListView):
    template_name = 'leads/lead_list.html'
    queryset =  Lead.objects.all()
    context_object_name = 'leads' # default is object_list

class LeadDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'leads/lead_detail.html'
    queryset =  Lead.objects.all()
    context_object_name = 'lead' # default is object_list


class LeadCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = 'leads/lead_create.html'
    form_class = ModelLeadForm

    def get_success_url(self) :
        return reverse('leads:lead_list')

    def form_valid(self, form):
        send_mail(
            subject="Lead create uccessfully",
            message="A lead has been created. Go to the site to verify this",
            from_email="test@test.com",
            recipient_list=["test@test2.com"]
        )
        return super(LeadCreateView, self).form_valid(form) 

def lead_create(request):
    form = ModelLeadForm()
    if request.method == "POST":
        form = ModelLeadForm(request.POST)
        if form.is_valid():
           form.save()
        return redirect('/leads')
    context = {
        'form': form 
    }
    return render(request, 'leads/lead_create.html', context)

class LeadUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'leads/lead_update.html'
    queryset =  Lead.objects.all()
    form_class = ModelLeadForm

    def get_success_url(self) :
        return reverse('leads:lead_list')


def lead_update(request, pk):
    lead = Lead.objects.get(id=pk)
    form = ModelLeadForm(instance=lead)
    if request.method == "POST":
        form = ModelLeadForm(request.POST, instance=lead)
        if form.is_valid():
            form.save()
        return redirect('/leads')
    context = {
        'lead':lead,
        'form': form
    }
    return render(request, 'leads/lead_update.html', context)

class LeadDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name = 'leads/lead_delete.html'
    queryset =  Lead.objects.all()

    def get_success_url(self) :
        return reverse('leads:lead_list')

def lead_delete(request, pk):
    lead = Lead.objects.get(id=pk)
    lead.delete()
    return redirect('/leads')

# def landing_page(request):
#     return render(request, 'landing.html')

# def lead_list(request):
#     leads = Lead.objects.all()
#     context = {
#         'leads':leads
#     }
#     return render(request, 'leads/lead_list.html', context)

# def lead_detail(request, pk):
#     lead = Lead.objects.get(id=pk)
#     context = {
#         'lead':lead
#     }
#     return render(request, 'leads/lead_detail.html', context)

# def lead_update(request, pk):
#     lead = Lead.objects.get(id=pk)
#     form = LeadForm()
#     if request.method == "POST":
#         form = LeadForm(request.POST)
#         if form.is_valid():
#             first_name = form.cleaned_data['first_name']
#             last_name = form.cleaned_data['last_name']
#             age = form.cleaned_data['age']
#             lead.first_name = first_name
#             lead.last_name = last_name
#             lead.age = age
#             lead.save()
             
#         return redirect('/leads')
#     context = {
#         'lead':lead,
#         'form': form
#     }
#     return render(request, 'leads/lead_update.html', context)

# def lead_create(request):
    # form = LeadForm()
    # if request.method == "POST":
    #     form = LeadForm(request.POST)
    #     if form.is_valid():
    #         first_name = form.cleaned_data['first_name']
    #         last_name = form.cleaned_data['last_name']
    #         age = form.cleaned_data['age']
    #         agent = Agent.objects.first()
    #         Lead.objects.create(
    #             first_name  =  first_name,
    #             last_name  =  last_name,
    #             age=age,
    #             agent  =  agent
    #         )
    #     return redirect('/leads')
    # context = {
    #     'form': form 
    # }
#     return render(request, 'leads/lead_create.html', context)