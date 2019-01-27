from .models import Animal, Equipement
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages


def index(request):
    animals = Animal.objects.all()
    equipements = Equipement.objects.all()
    return render(request, 'animalerie/index.html', {'animals': animals, 'equipements': equipements})


def nourrir(animal):
    mangeoire = Equipement.objects.get(nom="mangeoire")
    if mangeoire.verifie_disponibilite() == "occupe":
        return "Impossible, la mangeoire est actuellement occupée par " + str(mangeoire.cherche_occupant())

    if animal.lit_etat() != "affame":
        return "Désolé, " + str(animal) + " n'a pas faim!"

    animal.change_etat('repus')
    animal.change_lieu(mangeoire)


def divertir(animal):
    roue = Equipement.objects.get(nom="roue")
    if roue.verifie_disponibilite() == "occupe":
        return "Impossible, la roue est actuellement occupée par " + str(roue.cherche_occupant())
    if animal.lit_etat() != "repus":
        return "Désolé, " + str(animal) + " n'est pas en état de faire du sport !"
    animal.change_etat('fatigue')
    animal.change_lieu(roue)


def coucher(animal):
    nid = Equipement.objects.get(nom="nid")
    if nid.verifie_disponibilite() == "occupe":
        return "Impossible, le nid est actuellement occupée par " + str(nid.cherche_occupant())
    if animal.lit_etat() != "fatigue":
        return "Désolé, " + str(animal) + " n'est pas fatigué !"
    animal.change_lieu(nid)
    animal.change_etat('endormi')


def reveiller(animal):
    litiere = Equipement.objects.get(nom = "litiere")
    if animal.lit_etat() is not None:
        if animal.lit_etat() != 'endormi':
            return 'Désolé,'+ str(animal)+ "ne dort pas."
        else:
            animal.change_etat('affame')
            animal.change_lieu(litiere)
    else:
        return "Désolé,"+str(animal)+ "n'est pas un animal connu"

def action(request):
    try:
        selected_animal = request.POST['animal']
        selected_action = request.POST['action']
    except (KeyError, Animal.DoesNotExist):
        messages.info(request, "Un animal ET une action doivent être sélectionnés")
    else:
        animal=Animal.objects.get(pk=selected_animal)
        if selected_action=="nourrir":
            messages.info(request, nourrir(animal))
        if selected_action=="divertir":
            messages.info(request, divertir(animal))
        if selected_action=="coucher":
            messages.info(request, coucher(animal))
        if selected_action=="reveiller":
            messages.info(request, reveiller(animal))
    return HttpResponseRedirect(reverse('animalerie:index'))


