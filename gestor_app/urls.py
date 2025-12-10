from django.urls import path
from . import views

urlpatterns = [
    # Autenticación
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboards
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/administrador/', views.dashboard_administrador, name='dashboard_administrador'),
    path('dashboard/medico/', views.dashboard_medico, name='dashboard_medico'),
    path('dashboard/enfermera/', views.dashboard_enfermera, name='dashboard_enfermera'),
    path('dashboard/recepcionista/', views.dashboard_recepcionista, name='dashboard_recepcionista'),
    
    # Gestión de Usuarios (Solo Administrador)
    path('usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('usuarios/crear/', views.crear_usuario, name='crear_usuario'),
    path('usuarios/<int:user_id>/editar/', views.editar_usuario, name='editar_usuario'),
    path('usuarios/<int:user_id>/eliminar/', views.eliminar_usuario, name='eliminar_usuario'),
    
    # Gestión de Pacientes
    path('pacientes/', views.lista_pacientes, name='lista_pacientes'),
    path('pacientes/crear/', views.crear_paciente, name='crear_paciente'),
    path('pacientes/<int:paciente_id>/', views.ver_paciente, name='ver_paciente'),
    path('pacientes/<int:paciente_id>/editar/', views.editar_paciente, name='editar_paciente'),
    path('pacientes/<int:paciente_id>/eliminar/', views.eliminar_paciente, name='eliminar_paciente'),
    
    # Historia Clínica
    path('pacientes/<int:paciente_id>/historia/crear/', views.crear_historia, name='crear_historia'),
    path('historia/<int:historia_id>/editar/', views.editar_historia, name='editar_historia'),
    
    # Gestión de Citas
    path('citas/', views.lista_citas, name='lista_citas'),
    path('citas/crear/', views.crear_cita, name='crear_cita'),
    path('citas/<int:cita_id>/', views.ver_cita, name='ver_cita'),
    path('citas/<int:cita_id>/editar/', views.editar_cita, name='editar_cita'),
    path('citas/<int:cita_id>/eliminar/', views.eliminar_cita, name='eliminar_cita'),
    path('api/horarios-disponibles/', views.obtener_horarios_disponibles, name='obtener_horarios_disponibles'),
    
    # Recetas Médicas (Solo Médicos)
    path('recetas/', views.lista_recetas, name='lista_recetas'),
    path('recetas/crear/', views.crear_receta, name='crear_receta'),
    path('recetas/<int:receta_id>/', views.ver_receta, name='ver_receta'),
    path('recetas/<int:receta_id>/pdf/', views.descargar_receta_pdf, name='descargar_receta_pdf'),
    
    # Signos Vitales (Enfermeras)
    path('signos/', views.lista_signos, name='lista_signos'),
    path('signos/registrar/', views.registrar_signos, name='registrar_signos'),
    
    # Gestión de Medicamentos (Administrador)
    path('medicamentos/', views.lista_medicamentos, name='lista_medicamentos'),
    path('medicamentos/crear/', views.crear_medicamento, name='crear_medicamento'),
    path('medicamentos/<int:medicamento_id>/editar/', views.editar_medicamento, name='editar_medicamento'),
    path('medicamentos/<int:medicamento_id>/eliminar/', views.eliminar_medicamento, name='eliminar_medicamento'),
    path('api/medicamentos/buscar/', views.buscar_medicamentos, name='buscar_medicamentos'),
]