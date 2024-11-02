from django.shortcuts import render, redirect
from .models import Expense, Category, WeeklyGoal
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User
from django.contrib import messages

def login_page(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.all().filter(username=username).exists():
            validUser = authenticate(username=username, password=password)
            if validUser:
                login(request, validUser)   # Add user to a session
                return redirect("home")
            else:
                messages.info(request, f"Invalid Password, Try Again")
        else:
            messages.info(request, f"username \"{username}\" Not found")

    return render(request, 'login.html')

def signup_page(request):
    if request.method == 'POST':
        # Get the form data
        first_name = request.POST.get('firstName')
        lastName = request.POST.get('lastName')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        # filter the user from User model
        user = User.objects.filter(username=username)

        if user.exists():
            messages.info(request, f"Username already exists")
            return redirect('login_page')
        else:
            user = User.objects.create(
                first_name = first_name,
                last_name = lastName,
                username = username,
                email = email,
                # password can't be set directly, as it would not encrypt it & remain as raw str!
            )
            # Django's set_password method encrypts the password
            user.set_password(password)
            user.save()  # Save the user to the database
            messages.info(request, f"Account created successfully")

    return render(request, 'signup.html')


@login_required
def home(request):
    expenses = Expense.objects.filter(user=request.user)
    current_week_start = timezone.now().date() - timedelta(days=timezone.now().weekday())
    current_goal = WeeklyGoal.objects.filter(
        user=request.user,
        start_date__lte=current_week_start,
        end_date__gte=current_week_start
    ).first()
    
    total_expenses = sum(exp.amount for exp in expenses)
    goal_status = None
    if current_goal:
        goal_status = "Within Goal" if total_expenses <= current_goal.goal_amount else "Exceeding Goal"
    
    context = {
        'expenses': expenses,
        'current_goal': current_goal,
        'total_expenses': total_expenses,
        'goal_status': goal_status
    }
    return render(request, 'home.html', context)


def logout_page(request):
    logout(request)
    return redirect('login_page')

@login_required
def add_expense(request):
    if request.method == "POST":
        category_id = request.POST['category']
        amount = request.POST['amount']
        category = Category.objects.get(id=category_id)
        Expense.objects.create(user=request.user, category=category, amount=amount)
        return redirect('home')
    categories = Category.objects.filter(user=request.user) | Category.objects.filter(user__isnull=True)
    return render(request, 'add_expense.html', {'categories': categories})

@login_required
def set_weekly_goal(request):
    if request.method == "POST":
        start_date = timezone.now().date() - timedelta(days=timezone.now().weekday())
        end_date = start_date + timedelta(days=6)
        goal_amount = request.POST['goal_amount']
        WeeklyGoal.objects.update_or_create(
            user=request.user,
            start_date=start_date,
            end_date=end_date,
            defaults={'goal_amount': goal_amount}
        )
        return redirect('home')
    return render(request, 'set_weekly_goal.html')
