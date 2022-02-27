from django.urls import URLPattern, path
from django.conf import settings
from django.conf.urls.static import static
from Apps import views
from django.contrib.auth import views as auth_views
from .forms import PasswordChangeForm, PasswordReset, SetPassword

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('contact-us/', views.ContactUs.as_view(), name='contact-us'),
    # url for login & logout
    path('accounts/login/', views.UserLogin.as_view(), name='login' ),
    path('logout', views.logout_view, name='logout'),
    # url for registration
    path('register/', views.CutomerRegistration.as_view(), name='register'),
    # url start for change password
    path('passwordchange/', auth_views.PasswordChangeView.as_view(template_name='passwordchange.html', form_class=PasswordChangeForm, success_url='/passwordchangedone/'), name='passwordchange'),
    path('passwordchangedone/', auth_views.PasswordChangeDoneView.as_view(template_name='passwordchangedone.html'), name='passwordchangedone'),
    # url start for forgot password
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name="password_reset.html", form_class=PasswordReset), name="password_reset"),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name="password_reset_done.html"), name="password_reset_done"),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_confirm.html", form_class=SetPassword), name="password_reset_confirm"),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"), name="password_reset_complete"),
    path('profile/', views.profile, name='profile'),
    path('add-profile/', views.AddProfile.as_view(), name='add-profile'),
    path('search-report/', views.searchreport, name='search-report'),
    path('upload-report/', views.ReportUpload.as_view(), name='upload-report'),
    path('your-reports/', views.yourreports, name='your-reports'),
    path('FAQ/', views.FAQ, name='FAQ'),
    path('delete-report/<int:pk>', views.delete, name='delete-report'),
    path('search/', views.search, name='search'),
    path('doctor-refferals/', views.doctorrefferals, name='doctor-refferals'),
    path('lab-refferals/', views.labrefferals, name='lab-refferals'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)