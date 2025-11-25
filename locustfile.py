from locust import HttpUser, task, between, SequentialTaskSet
import random

class RecepcionistaWorkflow(SequentialTaskSet):
    """Flujo típico de una recepcionista"""
    
    def on_start(self):
        # Login como recepcionista
        response = self.client.post("/", {
            "username": "44444444-4",
            "password": "recepcionista123"
        }, allow_redirects=False)
        
        if response.status_code in [200, 302]:
            print("✓ Recepcionista login exitoso")
    
    @task
    def ver_dashboard(self):
        self.client.get("/dashboard/recepcionista/")
    
    @task
    def buscar_paciente(self):
        # Simula búsqueda de paciente
        self.client.get("/pacientes/")
    
    @task
    def ver_lista_citas(self):
        self.client.get("/citas/")
    
    @task
    def ver_detalle_paciente(self):
        # Ver un paciente aleatorio (IDs 1-3 de los datos de prueba)
        paciente_id = random.randint(1, 3)
        self.client.get(f"/pacientes/{paciente_id}/")


class MedicoWorkflow(SequentialTaskSet):
    """Flujo típico de un médico"""
    
    def on_start(self):
        # Login como médico
        response = self.client.post("/", {
            "username": "22222222-2",
            "password": "medico123"
        }, allow_redirects=False)
        
        if response.status_code in [200, 302]:
            print("✓ Médico login exitoso")
    
    @task
    def ver_dashboard(self):
        self.client.get("/dashboard/medico/")
    
    @task
    def ver_citas_del_dia(self):
        self.client.get("/citas/")
    
    @task
    def ver_lista_pacientes(self):
        self.client.get("/pacientes/")
    
    @task
    def ver_lista_recetas(self):
        self.client.get("/recetas/")
    
    @task
    def generar_pdf_receta(self):
        # Genera PDF de la receta de prueba (ID 1)
        self.client.get("/recetas/1/pdf/", name="/recetas/[id]/pdf/")


class EnfermeraWorkflow(SequentialTaskSet):
    """Flujo típico de una enfermera"""
    
    def on_start(self):
        # Login como enfermera
        response = self.client.post("/", {
            "username": "33333333-3",
            "password": "enfermera123"
        }, allow_redirects=False)
        
        if response.status_code in [200, 302]:
            print("✓ Enfermera login exitoso")
    
    @task
    def ver_dashboard(self):
        self.client.get("/dashboard/enfermera/")
    
    @task
    def ver_lista_signos(self):
        self.client.get("/signos/")
    
    @task
    def ver_citas_confirmadas(self):
        self.client.get("/citas/?estado=confirmada")


class AdministradorWorkflow(SequentialTaskSet):
    """Flujo típico de un administrador"""
    
    def on_start(self):
        # Login como admin
        response = self.client.post("/", {
            "username": "11111111-1",
            "password": "admin123"
        }, allow_redirects=False)
        
        if response.status_code in [200, 302]:
            print("✓ Administrador login exitoso")
    
    @task
    def ver_dashboard(self):
        self.client.get("/dashboard/administrador/")
    
    @task
    def ver_usuarios(self):
        self.client.get("/usuarios/")
    
    @task
    def ver_pacientes(self):
        self.client.get("/pacientes/")
    
    @task
    def ver_todas_citas(self):
        self.client.get("/citas/")


# ===== USUARIOS DE LOCUST =====

class RecepcionistaUser(HttpUser):
    """Simula una recepcionista usando el sistema"""
    wait_time = between(2, 5)  # Espera entre 2-5 segundos entre acciones
    weight = 3  # Mayor peso = más usuarios de este tipo
    tasks = [RecepcionistaWorkflow]


class MedicoUser(HttpUser):
    """Simula un médico usando el sistema"""
    wait_time = between(3, 8)  # Los médicos toman más tiempo
    weight = 2
    tasks = [MedicoWorkflow]


class EnfermeraUser(HttpUser):
    """Simula una enfermera usando el sistema"""
    wait_time = between(2, 6)
    weight = 2
    tasks = [EnfermeraWorkflow]


class AdministradorUser(HttpUser):
    """Simula un administrador usando el sistema"""
    wait_time = between(5, 10)  # Los admins realizan tareas más espaciadas
    weight = 1
    tasks = [AdministradorWorkflow]


# ===== CONFIGURACIÓN ADICIONAL =====

class UsuarioMixto(HttpUser):
    """Usuario que simula acciones rápidas y comunes sin login"""
    wait_time = between(1, 3)
    weight = 2
    
    @task(5)
    def ver_pagina_login(self):
        """Simula usuarios intentando acceder al login"""
        self.client.get("/")
    
    @task(1)
    def intento_acceso_directo(self):
        """Simula usuarios intentando acceder sin autenticación"""
        self.client.get("/dashboard/")
