from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.db.models import Sum
from django.utils import timezone
from .models import Evenement, Participation, Signalement, Profil
from .forms import EvenementForm, SignalementForm, InscriptionForm


def home(request):
    stats = {
        'benevoles': Profil.objects.count(),
        'kg_collectes': Participation.objects.aggregate(Sum('kg_collectes'))['kg_collectes__sum'] or 0,
        'evenements': Evenement.objects.filter(date__lt=timezone.now()).count(),
    }
    return render(request, 'home.html', {'stats': stats})


def carte(request):
    evenements = Evenement.objects.filter(date__gte=timezone.now())
    signalements = Signalement.objects.filter(traite=False)
    return render(request, 'carte.html', {
        'evenements': evenements,
        'signalements': signalements,
    })


def evenement_detail(request, pk):
    evenement = get_object_or_404(Evenement, pk=pk)
    est_inscrit = False
    if request.user.is_authenticated:
        est_inscrit = Participation.objects.filter(user=request.user, evenement=evenement).exists()
    return render(request, 'evenement_detail.html', {
        'evenement': evenement,
        'est_inscrit': est_inscrit,
    })


@login_required
def inscription_evenement(request, pk):
    evenement = get_object_or_404(Evenement, pk=pk)
    if not evenement.est_complet():
        Participation.objects.get_or_create(user=request.user, evenement=evenement)
        messages.success(request, "Inscription confirmée !")
    else:
        messages.error(request, "Événement complet")
    return redirect('evenement_detail', pk=pk)


@login_required
def desinscription_evenement(request, pk):
    evenement = get_object_or_404(Evenement, pk=pk)
    Participation.objects.filter(user=request.user, evenement=evenement).delete()
    messages.info(request, "Désinscription effectuée")
    return redirect('evenement_detail', pk=pk)


@login_required
def creer_evenement(request):
    if request.method == 'POST':
        form = EvenementForm(request.POST)
        if form.is_valid():
            evenement = form.save(commit=False)
            evenement.organisateur = request.user
            evenement.save()
            messages.success(request, "Événement créé !")
            return redirect('evenement_detail', pk=evenement.pk)
    else:
        form = EvenementForm()
    return render(request, 'evenement_form.html', {'form': form})


@login_required
def modifier_evenement(request, pk):
    evenement = get_object_or_404(Evenement, pk=pk)
    if request.user != evenement.organisateur:
        messages.error(request, "Vous n'êtes pas autorisé à modifier cet événement")
        return redirect('evenement_detail', pk=pk)

    if request.method == 'POST':
        form = EvenementForm(request.POST, instance=evenement)
        if form.is_valid():
            form.save()
            messages.success(request, "Événement modifié !")
            return redirect('evenement_detail', pk=pk)
    else:
        form = EvenementForm(instance=evenement)
    return render(request, 'evenement_form.html', {'form': form, 'evenement': evenement})


@login_required
def supprimer_evenement(request, pk):
    evenement = get_object_or_404(Evenement, pk=pk)
    if request.user != evenement.organisateur:
        messages.error(request, "Vous n'êtes pas autorisé à supprimer cet événement")
        return redirect('evenement_detail', pk=pk)

    if request.method == 'POST':
        evenement.delete()
        messages.success(request, "Événement supprimé")
        return redirect('carte')
    return render(request, 'evenement_confirm_delete.html', {'evenement': evenement})


@login_required
def signaler(request):
    if request.method == 'POST':
        form = SignalementForm(request.POST, request.FILES)
        if form.is_valid():
            signalement = form.save(commit=False)
            signalement.user = request.user
            signalement.save()
            messages.success(request, "Signalement enregistré, merci !")
            return redirect('carte')
    else:
        form = SignalementForm()
    return render(request, 'signalement_form.html', {'form': form})


@login_required
def profil(request):
    profil, created = Profil.objects.get_or_create(user=request.user)
    participations = Participation.objects.filter(user=request.user).select_related('evenement')
    signalements = Signalement.objects.filter(user=request.user)
    return render(request, 'profil.html', {
        'profil': profil,
        'participations': participations,
        'signalements': signalements,
    })


def register(request):
    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profil.objects.create(user=user)
            login(request, user)
            messages.success(request, "Bienvenue sur Rad0 !")
            return redirect('home')
    else:
        form = InscriptionForm()
    return render(request, 'registration/register.html', {'form': form})
