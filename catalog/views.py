from django.views import generic
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DeleteView, TemplateView
from django.contrib.auth import logout
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Application, Category
from .forms import RegisterForm, ApplicationForm


def index(request):
    completed_applications = Application.objects.filter(status='completed').order_by('-created_at')[:4]
    context = {'completed_applications': completed_applications}
    return render(request, 'index.html', context)

class Register(CreateView):
    template_name = 'registration/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('login')

def logout_view(request):
    logout(request)
    return redirect('index')

class ApplicationCreate(LoginRequiredMixin, CreateView):
    model = Application
    form_class = ApplicationForm
    template_name = 'create_application.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class Profile(LoginRequiredMixin, ListView):
    model = Application
    template_name = 'profile.html'
    context_object_name = 'user_applications'

    def get_queryset(self):
        user = self.request.user
        status_filter = self.request.GET.get('status')
        queryset = Application.objects.filter(user=user).order_by('-created_at')

        if status_filter in ['new', 'in_progress', 'completed']:
            queryset = queryset.filter(status=status_filter)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_filter'] = self.request.GET.get('status', '')
        return context

def is_admin(user):
    return user.is_staff

class ApplicationDelete(DeleteView):
    model = Application
    template_name = 'delete_application.html'
    success_url = reverse_lazy('profile')

class AdminPanel(LoginRequiredMixin, TemplateView):
    template_name = 'admin_panel.html'
    def dispatch(self, request, *args, **kwargs):
        if not is_admin(request.user):
            return redirect('index')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['applications'] = Application.objects.select_related('user', 'category').all().order_by('-created_at')
        context['categories'] = Category.objects.all()
        return context

@login_required
@user_passes_test(is_admin) # Проверяем права
def change_application_status(request):
    if request.method == 'POST':
        application_id = request.POST.get('application_id')
        new_status = request.POST.get('new_status')

        application = get_object_or_404(Application, id=application_id)
        valid_statuses = [choice[0] for choice in Application.STATUS_CHOICES]
        if new_status in valid_statuses:
            old_status_display = application.get_status_display()
            application.status = new_status
            application.save()
            messages.success(
                request,
                f'Статус заявки "{application.title}" изменён с "{old_status_display}" на "{new_status}".'
            )
    return redirect( 'admin_panel')

@login_required
@user_passes_test(is_admin)
def add_category(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        if name:
            if not Category.objects.filter(name=name).exists():
                Category.objects.create(name=name)
                messages.success(request, f'Категория "{name}" добавлена.')
            else:
                messages.error(request, f'Категория "{name}" уже существует.')
    return redirect('admin_panel')

@login_required
@user_passes_test(is_admin) # Проверяем права
def delete_category(request, category_id):
    if request.method == 'POST':
        category = get_object_or_404(Category, id=category_id)
        category_name = category.name
        category.delete()
        messages.success(request, f'Категория "{category_name}" и связанные заявки удалены.')
    return redirect('admin_panel')