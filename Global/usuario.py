class Usuario:
    # Crea la variable session del usuario
    def __init__(self, request):
        self.request = request
        self.session = request.session
        usuario = self.session.get("usuario")
        if not usuario:
            usuario = self.session["usuario"] = {}
        self.usuario = usuario

    def add(self, usuario):
        self.usuario = {
            "id": usuario.id,
            "nombre": usuario.nom_usuario,
            "rol_id": usuario.rol_id,
            "esta_autenticado": True,
            "perfil": usuario.ruta_foto.url if usuario.ruta_foto else False,
        }
        self.save()

    def save(self):
        self.session["usuario"] = self.usuario
        self.session.modified = True

    def clear(self):
        self.session["usuario"] = {}
        self.session.modified = True

    def edit_perfil(self, perfil):
        self.usuario["perfil"] = perfil.url
        self.save()

    def edit_nombre(self, nombre):
        self.usuario["nombre"] = nombre
        self.save()
