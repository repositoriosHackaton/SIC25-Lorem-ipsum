from usuario import Usuario

class ValoresSaludables:
    def __init__(self, user:Usuario):
        self.user = user
        self.tmb = TMB(user.peso, user.altura, user.edad, user.genero)
        self.calorias = calorias_saludables(self.tmb, user.nivel_ejercicio)
        self.grasas = grasas_saludables(self.calorias)
        self.grasas_saturadas = grasas_saturadas_saludables(self.calorias)
        self.colesterol = colesterol_saludable(self.calorias)
        self.sodio = sodio_saludable()
        self.carbohidratos = carbohidratos_saludables(self.calorias)
        self.fibra = fibra_saludable(self.calorias)
        self.azucares = azucares_saludables(self.calorias)
        self.proteinas = proteinas_saludables(self.calorias)



def TMB(peso, altura, edad, genero):
    if genero == "hombre":
        return 88.362+ 13.397*peso + 4.799 * altura - 5.677 * edad
    
    return 447.593 + 9.247 * peso + 3.098 * altura - 4.330 * edad

def calorias_saludables(tmb, nivel_ejericicio):
    if nivel_ejericicio == "sedentario":
        return tmb * 1.2
    if nivel_ejericicio == "ligero":
        return tmb * 1.375
    if nivel_ejericicio == "moderado":
        return tmb * 1.55
    if nivel_ejericicio == "activo":
        return tmb * 1.725
    if nivel_ejericicio == "muy activo":
        return tmb * 1.9

def grasas_saludables(calorias):
    return calorias * 0.25 / 9

def grasas_saturadas_saludables(calorias):
    return calorias * 0.07 / 9

def colesterol_saludable(calorias):
    return calorias * 0.03 / 9

def sodio_saludable():
    return 1500

def carbohidratos_saludables(calorias):
    return calorias * 0.45 / 4

def fibra_saludable(calorias):
    return 14 * calorias / 1000

def azucares_saludables(calorias):
    return 0.05 * calorias / 4

def proteinas_saludables(calorias):
    return 0.15 * calorias / 4
