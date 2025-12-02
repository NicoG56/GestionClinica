from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from .models import CustomUser, Medico, Enfermera, Recepcionista, Paciente, Cita, RecetaMedica, HistoriaClinica, SignosVitales
from .forms import (
    LoginForm, CustomUserCreationForm, CustomUserEditForm, MedicoForm, EnfermeraForm, RecepcionistaForm,
    PacienteForm, HistoriaClinicaForm, CitaForm, RecetaMedicaForm, SignosVitalesForm, CitaMedicoForm
)

# Decoradores de permisos
def es_administrador(user):
    return user.is_authenticated and user.rol == 'administrador'

def es_medico(user):
    return user.is_authenticated and user.rol == 'medico'

def es_enfermera(user):
    return user.is_authenticated and user.rol == 'enfermera'

def es_recepcionista(user):
    return user.is_authenticated and user.rol == 'recepcionista'

def puede_gestionar_pacientes(user):
    return user.is_authenticated and user.rol in ['administrador', 'medico', 'enfermera', 'recepcionista']

def puede_ver_pacientes(user):
    """Permite ver información de pacientes (incluyendo médicos en modo solo lectura)"""
    return user.is_authenticated and user.rol in ['administrador', 'medico', 'enfermera', 'recepcionista']

def puede_editar_pacientes(user):
    """Permite editar datos personales de pacientes (NO incluye médicos)"""
    return user.is_authenticated and user.rol in ['administrador', 'enfermera', 'recepcionista']

def puede_gestionar_citas(user):
    return user.is_authenticated and user.rol in ['administrador', 'recepcionista']


# Vista de Login
def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            rut = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=rut, password=password)
            
            if user is not None:
                auth_login(request, user)
                messages.success(request, f'Bienvenido, {user.nombre}')
                return redirect('dashboard')
            else:
                messages.error(request, 'RUT o contraseña incorrectos')
        else:
            messages.error(request, 'Por favor, corrija los errores')
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})


# Vista de Logout
@login_required
def logout_view(request):
    auth_logout(request)
    messages.info(request, 'Sesión cerrada exitosamente')
    return redirect('login')


# Dashboard - redirige según el rol
@login_required
def dashboard(request):
    user = request.user
    
    if user.rol == 'administrador':
        return redirect('dashboard_administrador')
    elif user.rol == 'medico':
        return redirect('dashboard_medico')
    elif user.rol == 'enfermera':
        return redirect('dashboard_enfermera')
    elif user.rol == 'recepcionista':
        return redirect('dashboard_recepcionista')
    else:
        messages.error(request, 'No tiene un rol asignado')
        return redirect('login')


# Dashboard Administrador
@login_required
@user_passes_test(es_administrador)
def dashboard_administrador(request):
    total_usuarios = CustomUser.objects.count()
    total_pacientes = Paciente.objects.count()
    total_citas_hoy = Cita.objects.filter(fecha_hora__date=timezone.now().date()).count()
    
    usuarios_recientes = CustomUser.objects.order_by('-fecha_creacion')[:5]
    
    context = {
        'usuario': request.user,
        'total_usuarios': total_usuarios,
        'total_pacientes': total_pacientes,
        'total_citas_hoy': total_citas_hoy,
        'usuarios_recientes': usuarios_recientes,
    }
    
    return render(request, 'dashboard_administrador.html', context)


# Dashboard Médico
@login_required
@user_passes_test(es_medico)
def dashboard_medico(request):
    try:
        medico = request.user.medico
    except Medico.DoesNotExist:
        messages.error(request, 'No se encontró el perfil de médico asociado.')
        return redirect('login')
    
    hoy = timezone.now().date()
    
    citas_hoy = Cita.objects.filter(
        medico=medico,
        fecha_hora__date=hoy
    ).order_by('fecha_hora')
    
    citas_proximas = Cita.objects.filter(
        medico=medico,
        fecha_hora__date__gt=hoy,
        estado__in=['pendiente', 'confirmada']
    ).order_by('fecha_hora')[:5]
    
    # Total de pacientes atendidos por este médico
    pacientes_atendidos = Cita.objects.filter(medico=medico).values('paciente').distinct().count()
    # Total de pacientes en el sistema
    total_pacientes = Paciente.objects.count()
    
    context = {
        'usuario': request.user,
        'medico': medico,
        'citas_hoy': citas_hoy,
        'citas_proximas': citas_proximas,
        'pacientes_atendidos': pacientes_atendidos,
        'total_pacientes': total_pacientes,
    }
    
    return render(request, 'vista_medico.html', context)


# Dashboard Enfermera
@login_required
@user_passes_test(es_enfermera)
def dashboard_enfermera(request):
    hoy = timezone.now().date()
    
    citas_hoy = Cita.objects.filter(
        fecha_hora__date=hoy,
        estado__in=['confirmada', 'en_curso']
    ).order_by('fecha_hora')
    
    signos_hoy = SignosVitales.objects.filter(
        fecha_hora__date=hoy
    ).count()
    
    context = {
        'usuario': request.user,
        'citas_hoy': citas_hoy,
        'signos_hoy': signos_hoy,
    }
    
    return render(request, 'vista_enfermera.html', context)


# Dashboard Recepcionista
@login_required
@user_passes_test(es_recepcionista)
def dashboard_recepcionista(request):
    hoy = timezone.now().date()
    
    citas_hoy = Cita.objects.filter(fecha_hora__date=hoy).order_by('fecha_hora')
    citas_pendientes = Cita.objects.filter(estado='pendiente', fecha_hora__gte=timezone.now()).count()
    total_pacientes = Paciente.objects.count()
    
    context = {
        'usuario': request.user,
        'citas_hoy': citas_hoy,
        'citas_pendientes': citas_pendientes,
        'total_pacientes': total_pacientes,
    }
    
    return render(request, 'vista_recepcionista.html', context)


# ============= GESTIÓN DE USUARIOS (Solo Administrador) =============

@login_required
@user_passes_test(es_administrador)
def lista_usuarios(request):
    usuarios = CustomUser.objects.all().order_by('-fecha_creacion')
    
    # Filtros
    rol_filter = request.GET.get('rol')
    if rol_filter:
        usuarios = usuarios.filter(rol=rol_filter)
    
    context = {
        'usuarios': usuarios,
        'rol_filter': rol_filter,
    }
    
    return render(request, 'usuarios/lista.html', context)


@login_required
@user_passes_test(es_administrador)
def crear_usuario(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            
            # Si el rol es médico, crear el perfil de médico con los campos adicionales
            if usuario.rol == 'medico':
                Medico.objects.create(
                    usuario=usuario,
                    especialidad=request.POST.get('especialidad', ''),
                    numero_registro=request.POST.get('numero_registro', ''),
                    anos_experiencia=int(request.POST.get('anos_experiencia', 0)),
                    duracion_consulta=int(request.POST.get('duracion_consulta', 30)),
                    atiende_manana=request.POST.get('atiende_manana') == 'on',
                    hora_inicio_manana=request.POST.get('hora_inicio_manana', '08:30'),
                    hora_fin_manana=request.POST.get('hora_fin_manana', '12:30'),
                    atiende_tarde=request.POST.get('atiende_tarde') == 'on',
                    hora_inicio_tarde=request.POST.get('hora_inicio_tarde', '13:30'),
                    hora_fin_tarde=request.POST.get('hora_fin_tarde', '17:00'),
                    dias_atencion=request.POST.get('dias_atencion', '1,2,3,4,5')
                )
            elif usuario.rol == 'enfermera':
                Enfermera.objects.create(usuario=usuario)
            elif usuario.rol == 'recepcionista':
                Recepcionista.objects.create(usuario=usuario)
            
            messages.success(request, f'Usuario {usuario.nombre} creado exitosamente')
            return redirect('lista_usuarios')
        else:
            messages.error(request, 'Por favor, corrija los errores')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'usuarios/crear.html', {'form': form})


@login_required
@user_passes_test(es_administrador)
def editar_usuario(request, user_id):
    usuario = get_object_or_404(CustomUser, id=user_id)
    
    # Obtener el perfil de médico si existe
    medico = None
    if usuario.rol == 'medico':
        medico = Medico.objects.filter(usuario=usuario).first()
    
    if request.method == 'POST':
        form = CustomUserEditForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            
            # Si es médico, actualizar o crear el perfil
            if usuario.rol == 'medico':
                if medico:
                    # Actualizar perfil existente
                    medico.especialidad = request.POST.get('especialidad', '')
                    medico.numero_registro = request.POST.get('numero_registro', '')
                    medico.anos_experiencia = int(request.POST.get('anos_experiencia', 0))
                    medico.duracion_consulta = int(request.POST.get('duracion_consulta', 30))
                    medico.atiende_manana = request.POST.get('atiende_manana') == 'on'
                    medico.hora_inicio_manana = request.POST.get('hora_inicio_manana', '08:30')
                    medico.hora_fin_manana = request.POST.get('hora_fin_manana', '12:30')
                    medico.atiende_tarde = request.POST.get('atiende_tarde') == 'on'
                    medico.hora_inicio_tarde = request.POST.get('hora_inicio_tarde', '13:30')
                    medico.hora_fin_tarde = request.POST.get('hora_fin_tarde', '17:00')
                    medico.dias_atencion = request.POST.get('dias_atencion', '1,2,3,4,5')
                    medico.save()
                else:
                    # Crear nuevo perfil
                    Medico.objects.create(
                        usuario=usuario,
                        especialidad=request.POST.get('especialidad', ''),
                        numero_registro=request.POST.get('numero_registro', ''),
                        anos_experiencia=int(request.POST.get('anos_experiencia', 0)),
                        duracion_consulta=int(request.POST.get('duracion_consulta', 30)),
                        atiende_manana=request.POST.get('atiende_manana') == 'on',
                        hora_inicio_manana=request.POST.get('hora_inicio_manana', '08:30'),
                        hora_fin_manana=request.POST.get('hora_fin_manana', '12:30'),
                        atiende_tarde=request.POST.get('atiende_tarde') == 'on',
                        hora_inicio_tarde=request.POST.get('hora_inicio_tarde', '13:30'),
                        hora_fin_tarde=request.POST.get('hora_fin_tarde', '17:00'),
                        dias_atencion=request.POST.get('dias_atencion', '1,2,3,4,5')
                    )
            
            messages.success(request, f'Usuario {usuario.nombre} actualizado exitosamente')
            return redirect('lista_usuarios')
    else:
        form = CustomUserEditForm(instance=usuario)
    
    return render(request, 'usuarios/editar.html', {
        'form': form, 
        'usuario': usuario,
        'medico': medico
    })


@login_required
@user_passes_test(es_administrador)
def eliminar_usuario(request, user_id):
    usuario = get_object_or_404(CustomUser, id=user_id)
    
    if request.method == 'POST':
        nombre_usuario = usuario.nombre
        usuario.delete()
        messages.success(request, f'Usuario {nombre_usuario} eliminado exitosamente de la base de datos')
        return redirect('lista_usuarios')
    
    return render(request, 'usuarios/eliminar.html', {'usuario': usuario})


# ============= GESTIÓN DE PACIENTES =============

@login_required
@user_passes_test(puede_gestionar_pacientes)
def lista_pacientes(request):
    pacientes = Paciente.objects.all().order_by('nombre')
    
    # Búsqueda
    busqueda = request.GET.get('q')
    if busqueda:
        pacientes = pacientes.filter(
            Q(nombre__icontains=busqueda) |
            Q(rut__icontains=busqueda)
        )
    
    context = {
        'pacientes': pacientes,
        'busqueda': busqueda,
    }
    
    return render(request, 'pacientes/lista.html', context)


@login_required
@user_passes_test(puede_ver_pacientes)
def ver_paciente(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    citas = Cita.objects.filter(paciente=paciente).order_by('-fecha_hora')[:10]
    recetas = RecetaMedica.objects.filter(paciente=paciente).order_by('-fecha_emision')[:5]
    signos = SignosVitales.objects.filter(paciente=paciente).order_by('-fecha_hora')[:5]
    
    try:
        historia = paciente.historia
    except HistoriaClinica.DoesNotExist:
        historia = None
    
    context = {
        'paciente': paciente,
        'historia': historia,
        'citas': citas,
        'recetas': recetas,
        'signos': signos,
    }
    
    return render(request, 'pacientes/ver.html', context)


@login_required
@user_passes_test(puede_gestionar_pacientes)
def crear_paciente(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            paciente = form.save()
            messages.success(request, f'Paciente {paciente.nombre} registrado exitosamente')
            return redirect('ver_paciente', paciente_id=paciente.id)
    else:
        form = PacienteForm()
    
    return render(request, 'pacientes/crear.html', {'form': form})


@login_required
@user_passes_test(puede_editar_pacientes)
def editar_paciente(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    
    if request.method == 'POST':
        form = PacienteForm(request.POST, instance=paciente)
        if form.is_valid():
            form.save()
            messages.success(request, f'Paciente {paciente.nombre} actualizado exitosamente')
            return redirect('ver_paciente', paciente_id=paciente.id)
    else:
        form = PacienteForm(instance=paciente)
    
    return render(request, 'pacientes/editar.html', {'form': form, 'paciente': paciente})


@login_required
@user_passes_test(es_administrador)
def eliminar_paciente(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    
    if request.method == 'POST':
        nombre_paciente = paciente.nombre
        paciente.delete()
        messages.success(request, f'Paciente {nombre_paciente} eliminado exitosamente de la base de datos')
        return redirect('lista_pacientes')
    
    return render(request, 'pacientes/eliminar.html', {'paciente': paciente})


# ============= GESTIÓN DE CITAS =============

@login_required
def lista_citas(request):
    user = request.user
    
    if user.rol == 'medico':
        try:
            medico = user.medico
            citas = Cita.objects.filter(medico=medico)
        except Medico.DoesNotExist:
            citas = Cita.objects.none()
    elif user.rol in ['recepcionista', 'administrador']:
        citas = Cita.objects.all()
    elif user.rol == 'enfermera':
        citas = Cita.objects.filter(estado__in=['confirmada', 'en_curso'])
    else:
        citas = Cita.objects.none()
    
    citas = citas.order_by('-fecha_hora')
    
    # Filtros
    estado_filter = request.GET.get('estado')
    if estado_filter:
        citas = citas.filter(estado=estado_filter)
    
    fecha_filter = request.GET.get('fecha')
    if fecha_filter:
        citas = citas.filter(fecha_hora__date=fecha_filter)
    
    context = {
        'citas': citas,
        'estado_filter': estado_filter,
        'fecha_filter': fecha_filter,
    }
    
    return render(request, 'citas/lista.html', context)


@login_required
@user_passes_test(puede_gestionar_citas)
def crear_cita(request):
    if request.method == 'POST':
        form = CitaForm(request.POST)
        if form.is_valid():
            cita = form.save(commit=False)
            cita.creada_por = request.user
            cita.save()
            messages.success(request, f'Cita creada exitosamente para {cita.paciente.nombre} el {cita.fecha_hora.strftime("%d/%m/%Y a las %H:%M")}')
            return redirect('lista_citas')
    else:
        form = CitaForm()
    
    return render(request, 'citas/crear.html', {'form': form})


@login_required
@user_passes_test(puede_gestionar_citas)
def obtener_horarios_disponibles(request):
    """Vista AJAX para obtener horarios disponibles de un médico en una fecha"""
    from django.http import JsonResponse
    from datetime import datetime, date
    
    medico_id = request.GET.get('medico_id')
    fecha_str = request.GET.get('fecha')
    
    if not medico_id or not fecha_str:
        return JsonResponse({'horarios': []})
    
    try:
        medico = Medico.objects.get(id=medico_id)
        fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
        
        # Verificar que la fecha no sea en el pasado
        if fecha < date.today():
            return JsonResponse({'horarios': [], 'error': 'No se pueden agendar citas en fechas pasadas'})
        
        horarios = medico.obtener_horarios_disponibles(fecha)
        
        horarios_list = [
            {
                'value': h.strftime('%H:%M'),
                'text': h.strftime('%H:%M')
            } for h in horarios
        ]
        
        return JsonResponse({'horarios': horarios_list})
        
    except Medico.DoesNotExist:
        return JsonResponse({'horarios': [], 'error': 'Médico no encontrado'})
    except ValueError:
        return JsonResponse({'horarios': [], 'error': 'Formato de fecha inválido'})


@login_required
def ver_cita(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id)
    
    # Verificar permisos
    user = request.user
    if user.rol == 'medico' and cita.medico != user:
        messages.error(request, 'No tiene permisos para ver esta cita')
        return redirect('lista_citas')
    
    recetas = RecetaMedica.objects.filter(cita=cita)
    signos = SignosVitales.objects.filter(cita=cita)
    
    context = {
        'cita': cita,
        'recetas': recetas,
        'signos': signos,
    }
    
    return render(request, 'citas/ver.html', context)


@login_required
def editar_cita(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id)
    user = request.user
    
    # Médicos solo pueden actualizar estado, diagnóstico y tratamiento
    if user.rol == 'medico':
        if cita.medico != user:
            messages.error(request, 'No tiene permisos para editar esta cita')
            return redirect('lista_citas')
        
        if request.method == 'POST':
            form = CitaMedicoForm(request.POST, instance=cita)
            if form.is_valid():
                form.save()
                messages.success(request, 'Cita actualizada exitosamente')
                return redirect('ver_cita', cita_id=cita.id)
        else:
            form = CitaMedicoForm(instance=cita)
    else:
        # Recepcionistas y administradores pueden editar todo
        if request.method == 'POST':
            form = CitaForm(request.POST, instance=cita)
            if form.is_valid():
                form.save()
                messages.success(request, 'Cita actualizada exitosamente')
                return redirect('ver_cita', cita_id=cita.id)
        else:
            form = CitaForm(instance=cita)
    
    return render(request, 'citas/editar.html', {'form': form, 'cita': cita})


@login_required
@user_passes_test(puede_gestionar_citas)
def eliminar_cita(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id)
    
    if request.method == 'POST':
        cita.estado = 'cancelada'
        cita.save()
        messages.success(request, 'Cita cancelada exitosamente')
        return redirect('lista_citas')
    
    return render(request, 'citas/eliminar.html', {'cita': cita})


# ============= GESTIÓN DE RECETAS (Solo Médicos) =============

@login_required
@user_passes_test(es_medico)
def crear_receta(request):
    try:
        medico = request.user.medico
    except Medico.DoesNotExist:
        messages.error(request, 'No se encontró el perfil de médico asociado.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = RecetaMedicaForm(request.POST, medico=medico)
        if form.is_valid():
            receta = form.save(commit=False)
            receta.medico = medico
            receta.save()
            messages.success(request, f'Receta emitida exitosamente para {receta.paciente.nombre}')
            return redirect('lista_recetas')
    else:
        form = RecetaMedicaForm(medico=medico)
    
    return render(request, 'recetas/crear.html', {'form': form})


@login_required
def lista_recetas(request):
    user = request.user
    
    if user.rol == 'medico':
        try:
            medico = user.medico
            recetas = RecetaMedica.objects.filter(medico=medico)
        except Medico.DoesNotExist:
            recetas = RecetaMedica.objects.none()
    else:
        recetas = RecetaMedica.objects.all()
    
    recetas = recetas.order_by('-fecha_emision')
    
    context = {
        'recetas': recetas,
    }
    
    return render(request, 'recetas/lista.html', context)


@login_required
def ver_receta(request, receta_id):
    receta = get_object_or_404(RecetaMedica, id=receta_id)
    
    return render(request, 'recetas/ver.html', {'receta': receta})


@login_required
def descargar_receta_pdf(request, receta_id):
    receta = get_object_or_404(RecetaMedica, id=receta_id)
    
    # Crear la respuesta HTTP con tipo PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="receta_{receta.paciente.rut}_{receta.fecha_emision.strftime("%Y%m%d")}.pdf"'
    
    # Crear el PDF
    doc = SimpleDocTemplate(response, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
    elements = []
    
    # Estilos
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#0066cc'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=12,
        textColor=colors.HexColor('#333333'),
        spaceAfter=12,
        spaceBefore=12
    )
    normal_style = styles['Normal']
    
    # Encabezado
    elements.append(Paragraph("RECETA MÉDICA", title_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Información del médico
    elements.append(Paragraph("<b>DATOS DEL MÉDICO</b>", heading_style))
    medico_data = [
        ['Nombre:', receta.medico.usuario.nombre],
        ['Especialidad:', receta.medico.especialidad],
        ['Registro Profesional:', receta.medico.numero_registro],
    ]
    medico_table = Table(medico_data, colWidths=[2*inch, 4.5*inch])
    medico_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e8f4f8')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    elements.append(medico_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Información del paciente
    elements.append(Paragraph("<b>DATOS DEL PACIENTE</b>", heading_style))
    paciente_data = [
        ['Nombre:', receta.paciente.nombre],
        ['RUT:', receta.paciente.rut],
        ['Fecha de Nacimiento:', receta.paciente.fecha_nacimiento.strftime('%d/%m/%Y')],
        ['Teléfono:', receta.paciente.telefono],
    ]
    paciente_table = Table(paciente_data, colWidths=[2*inch, 4.5*inch])
    paciente_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e8f4f8')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    elements.append(paciente_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Medicamentos
    elements.append(Paragraph("<b>MEDICAMENTOS PRESCRITOS</b>", heading_style))
    medicamentos_paragraph = Paragraph(receta.medicamentos.replace('\n', '<br/>'), normal_style)
    elements.append(medicamentos_paragraph)
    elements.append(Spacer(1, 0.2*inch))
    
    # Indicaciones
    elements.append(Paragraph("<b>INDICACIONES</b>", heading_style))
    indicaciones_paragraph = Paragraph(receta.indicaciones.replace('\n', '<br/>'), normal_style)
    elements.append(indicaciones_paragraph)
    elements.append(Spacer(1, 0.3*inch))
    
    # Información de la receta
    elements.append(Paragraph("<b>INFORMACIÓN DE LA RECETA</b>", heading_style))
    info_data = [
        ['Fecha de Emisión:', receta.fecha_emision.strftime('%d/%m/%Y %H:%M')],
        ['Vigencia hasta:', receta.vigencia.strftime('%d/%m/%Y')],
    ]
    info_table = Table(info_data, colWidths=[2*inch, 4.5*inch])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e8f4f8')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    elements.append(info_table)
    elements.append(Spacer(1, 0.5*inch))
    
    # Firma
    elements.append(Spacer(1, 0.5*inch))
    firma_style = ParagraphStyle('firma', parent=styles['Normal'], alignment=TA_CENTER, fontSize=10)
    elements.append(Paragraph("_" * 40, firma_style))
    elements.append(Paragraph(f"<b>{receta.medico.usuario.nombre}</b>", firma_style))
    elements.append(Paragraph(f"{receta.medico.especialidad}", firma_style))
    elements.append(Paragraph(f"Reg. Prof. {receta.medico.numero_registro}", firma_style))
    
    # Construir el PDF
    doc.build(elements)
    
    return response


# ============= GESTIÓN DE SIGNOS VITALES (Enfermeras) =============

@login_required
@user_passes_test(es_enfermera)
def registrar_signos(request):
    try:
        enfermera = request.user.enfermera
    except Enfermera.DoesNotExist:
        messages.error(request, 'No se encontró el perfil de enfermera asociado.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = SignosVitalesForm(request.POST)
        if form.is_valid():
            signos = form.save(commit=False)
            signos.enfermera = enfermera
            signos.save()
            messages.success(request, f'Signos vitales registrados para {signos.paciente.nombre}')
            return redirect('lista_signos')
    else:
        form = SignosVitalesForm()
    
    return render(request, 'signos/registrar.html', {'form': form})


@login_required
def lista_signos(request):
    signos = SignosVitales.objects.all().order_by('-fecha_hora')
    
    # Filtro por paciente
    paciente_id = request.GET.get('paciente')
    if paciente_id:
        signos = signos.filter(paciente_id=paciente_id)
    
    context = {
        'signos': signos,
    }
    
    return render(request, 'signos/lista.html', context)


# ============= GESTIÓN DE HISTORIA CLÍNICA =============

@login_required
@user_passes_test(lambda u: u.rol in ['medico', 'enfermera', 'administrador'])
def crear_historia(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    
    # Verificar si ya tiene historia clínica
    try:
        historia = paciente.historia
        messages.info(request, 'Este paciente ya tiene una historia clínica')
        return redirect('editar_historia', historia_id=historia.id)
    except HistoriaClinica.DoesNotExist:
        pass
    
    if request.method == 'POST':
        form = HistoriaClinicaForm(request.POST)
        if form.is_valid():
            historia = form.save(commit=False)
            historia.actualizado_por = request.user
            historia.save()
            messages.success(request, 'Historia clínica creada exitosamente')
            return redirect('ver_paciente', paciente_id=paciente.id)
    else:
        form = HistoriaClinicaForm(initial={'paciente': paciente})
    
    return render(request, 'historia/crear.html', {'form': form, 'paciente': paciente})


@login_required
@user_passes_test(lambda u: u.rol in ['medico', 'enfermera', 'administrador'])
def editar_historia(request, historia_id):
    historia = get_object_or_404(HistoriaClinica, id=historia_id)
    
    if request.method == 'POST':
        form = HistoriaClinicaForm(request.POST, instance=historia)
        if form.is_valid():
            historia = form.save(commit=False)
            historia.actualizado_por = request.user
            historia.save()
            messages.success(request, 'Historia clínica actualizada exitosamente')
            return redirect('ver_paciente', paciente_id=historia.paciente.id)
    else:
        form = HistoriaClinicaForm(instance=historia)
    
    return render(request, 'historia/editar.html', {'form': form, 'historia': historia})
