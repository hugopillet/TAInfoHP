from django.db import models

choix_etat = (('affame','affame'), ('repus', 'repus'), ('endormi', 'endormi'), ('fatigue', 'fatigue'))

class Equipement(models.Model):
    nom = models.TextField()
    dispo = models.TextField()

    def __str__(self):
        return self.nom

    def verifie_disponibilite(self):
        return self.dispo

    def cherche_occupant(self):
        lanimal=[]
        animals = Animal.objects.all()
        for animal in animals:
            if animal.lit_lieu==self.nom:
                lanimal.add(animal)
        if lanimal==[]:
            print("Cet équipement n'est pas occupé")
            return None
        else:
            return lanimal

class Animal(models.Model):
    nom = models.TextField()
    lieu = models.TextField()
    type = models.TextField()
    etat = models.CharField(max_length=100, choices=choix_etat)
    race = models.TextField()

    def __str__(self):
        return self.nom

    def lit_etat(self):
        return self.etat

    def lit_lieu(self):
        return self.lieu

    def change_etat(self, etat):
        if etat not in ["affame", "fatigue", "repus", "endormi"]:
            return "Désolé, " + str(etat) + " n'est pas un état autorisé"

        self.etat=etat
        self.save()
        print("Changement d'état ok")

    def change_lieu(self, lieu):
        equipements=Equipement.objects.all()
        if lieu not in equipements:
            return "Désolé, " + lieu.nom + " n'est pas un équipement"

        if lieu.verifie_disponibilite() == "libre":
            old=self.lieu
            self.lieu=str(lieu)
            if str(lieu)!="litiere":
                lieu.dispo="occupe"
            ancien_lieu = Equipement.objects.get(nom=old)
            ancien_lieu.dispo="libre"
            ancien_lieu.save()
            lieu.save()
            self.save()
            print("Changement de lieu ok")
        else:
            return "Désolé, " + lieu.nom + " est déjà occupé !"