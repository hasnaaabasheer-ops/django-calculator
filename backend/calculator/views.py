from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .forms import CalculatorForm

from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie


@login_required
def calculator(request):

    display = request.session.get("display", "0")

    if request.method == "POST":

        form = CalculatorForm(request.POST)

        if form.is_valid():

            button = form.cleaned_data["button"]

            # Clear
            if button == "C":

                display = "0"

            # Backspace
            elif button == "back":

                if display != "0":
                    display = display[:-1]

                if display == "":
                    display = "0"

            # Numbers and decimal
            elif button in "0123456789.":

                if display == "0":
                    display = button
                else:
                    display += button

            # Operators
            elif button in ["+", "-", "*", "/"]:

                # Don't allow two operators together
                if display[-1] not in ["+", "-", "*", "/"]:

                    display += button

            # Equal
            elif button == "=":

                try:

                    # Separate the expression
                    expression = display

                    # Find the operator
                    if "+" in expression:
                        number1, number2 = expression.split("+")
                        result = float(number1) + float(number2)

                    elif "-" in expression:
                        number1, number2 = expression.split("-")
                        result = float(number1) - float(number2)

                    elif "*" in expression:
                        number1, number2 = expression.split("*")
                        result = float(number1) * float(number2)

                    elif "/" in expression:
                        number1, number2 = expression.split("/")

                        if float(number2) == 0:
                            display = "Error"
                        else:
                            result = float(number1) / float(number2)

                    else:
                        result = float(expression)

                    if display != "Error":

                        if result.is_integer():
                            display = str(int(result))
                        else:
                            display = str(result)

                except:
                    display = "Error"

            # Save expression
            request.session["display"] = display

    else:

        form = CalculatorForm()

    return render(
        request,
        "calculator/calcu.html",
        {
            "form": form,
            "display": display,
        }
    )

def api_test(request):
    return JsonResponse({
        "message": "React and Django connected successfully!"
    })

@ensure_csrf_cookie
def csrf_token(request):
    return JsonResponse({
        "csrfToken": get_token(request)
    })
import json
import re

from django.http import JsonResponse
from django.views.decorators.http import require_POST


@require_POST
def calculator_api(request):
    try:
        data = json.loads(request.body)

        expression = data.get('expression', '')

        if not expression:
            return JsonResponse({
                'error': 'Please enter a calculation.'
            }, status=400)

        if not re.fullmatch(r'[0-9+\-*/.() ]+', expression):
            return JsonResponse({
                'error': 'Invalid expression.'
            }, status=400)

        try:
            result = eval(expression, {"__builtins__": {}}, {})
        except ZeroDivisionError:
            return JsonResponse({
                'error': 'Cannot divide by zero.'
            }, status=400)
        except Exception:
            return JsonResponse({
                'error': 'Invalid calculation.'
            }, status=400)

        return JsonResponse({
            'expression': expression,
            'result': result
        })

    except (json.JSONDecodeError, TypeError):
        return JsonResponse({
            'error': 'Invalid request data.'
        }, status=400)