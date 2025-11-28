from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, DetailView
from django.contrib.auth import get_user_model
from django.db.models import Sum

from .models import DropOffPoint, Submission, Reward
from .forms import SubmissionForm, RegisterForm, LoginForm

User = get_user_model()


# ---------------- HOME ----------------

def home_view(request):
    rewards = Reward.objects.all()
    total_users = User.objects.count()
    total_submissions = Submission.objects.count()
    total_kg = Submission.objects.aggregate(total=Sum('quantity'))['total'] or 0
    total_rewards = Reward.objects.count()
    
    # Pontos por tipo de material
    material_points = {
        "Papel/Papelão": 5,
        "Plástico": 10,
        "Vidro": 8,
        "Metal": 12,
        "Eletrônicos": 20,
        "Orgânico": 2,
    }

    user_points = 0
    if request.user.is_authenticated:
        user_points = Submission.objects.filter(user=request.user).aggregate(total=Sum('points'))['total'] or 0

    context = {
        'rewards': rewards,
        'total_users': total_users,
        'total_submissions': total_submissions,
        'total_kg': total_kg,
        'total_rewards': total_rewards,
        'material_points': material_points,
        'user_points': user_points,
        
    }

    return render(request, "home.html", context)


# ---------------- AUTENTICAÇÃO ----------------

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Conta criada com sucesso!")
            return redirect("home")
    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect("home")
            else:
                messages.error(request, "Usuário ou senha inválidos")
    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("login")


# ---------------- USERS ----------------

class UserListView(ListView):
    model = User
    template_name = "users/user_list.html"
    context_object_name = "users"


class UserDetailView(DetailView):
    model = User
    template_name = "users/user_detail.html"
    context_object_name = "user_obj"


# ---------------- PONTOS DE COLETA ----------------

class DropOffPointListView(ListView):
    model = DropOffPoint
    template_name = "dropoff/dropoff_list.html"
    context_object_name = "points"


# ---------------- SUBMISSÕES ----------------

class SubmissionListView(ListView):
    model = Submission
    template_name = "submissions/submission_list.html"
    context_object_name = "submissions"

    def get_queryset(self):
        return Submission.objects.filter(user=self.request.user)


class SubmissionDetailView(DetailView):
    model = Submission
    template_name = "submissions/submission_detail.html"
    context_object_name = "submission"


@login_required
def create_submission(request):
    if request.method == "POST":
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.user = request.user
            submission.status = "pending"

            # Calcula pontos
            points_dict = {
                "papel": 5,
                "plastico": 10,
                "vidro": 8,
                "metal": 12,
                "eletronico": 20,
                "organico": 2,
            }
            submission.points = float(submission.quantity) * points_dict.get(submission.material_type, 0)
            submission.save()

            messages.success(request, "Descarte enviado! Aguarde validação.")
            return redirect("home")
    else:
        form = SubmissionForm()

    return render(request, "submissions/submission_form.html", {"form": form})


# ---------------- RECOMPENSAS ----------------

class RewardListView(ListView):
    model = Reward
    template_name = "rewards/reward_list.html"
    context_object_name = "rewards"


@login_required
def redeem_reward(request, reward_id):
    reward = get_object_or_404(Reward, id=reward_id)
    user = request.user

    if user.pontos < reward.points_required:
        messages.error(request, "Você não tem pontos suficientes!")
        return redirect("reward-list")

    user.pontos -= reward.points_required
    user.save()

    messages.success(request, f"Recompensa '{reward.title}' resgatada com sucesso!")
    return redirect("reward-list")


# ---------------- CADASTRAR DESCARTE (BOTÃO DO HOME) ----------------

@login_required
def cadastrar_descarte(request):
    return redirect("submission-create")
