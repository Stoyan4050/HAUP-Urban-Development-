"""
views.py
"""

import collections
import json
from math import ceil, floor
from django.contrib.auth import authenticate, login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import redirect, render
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.views import View
from pyproj import Transformer
from .forms import ChangePasswordForm, RegisterForm, LoginForm, NewPasswordForm
from .models import Classification, Tile, User
from .tokens import TOKEN_GENERATOR
from .utils import extract_available_years, send_email, transform_tile_to_coordinates, \
    transform_coordinates_to_tile, manual_classify


class BaseView(View):
    """
    class BaseView(View)
    """

    @staticmethod
    def get(request):
        """
        @staticmethod
        def get(request)
        """

        if request.user.is_authenticated:
            return redirect("urban_development:map_page")

        return redirect("urban_development:login_page")


class GuestView(View):
    """
    class GuestView(View)
    """

    @staticmethod
    def get(request):
        """
        @staticmethod
        def get(request)
        """

        logout(request)
        return redirect("urban_development:map_page")


class LoginView(View):
    """
    class LoginView(View)
    """

    _context = {
        "title": "Login Page",
        "action": "/urban_development/login/",
        "hyperlinks": {
            "Click here to change your password": "/urban_development/change_password/",
            "Click here to register": "/urban_development/register/",
            "Log in as a guest": "/urban_development/guest/",
        },
        "button": "Log in",
    }

    def get(self, request):
        """
        def get(self, request)
        """

        self._context["form"] = LoginForm()
        return render(request, "pages/login_page.html", context=self._context)

    def post(self, request):
        """
        def post(self, request)
        """

        form = LoginForm(data=request.POST)

        if form.is_valid():
            email = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)
                return redirect("urban_development:map_page")

        self._context["form"] = form
        return render(request, "pages/login_page.html", context=self._context)


class LogoutView(View):
    """
    class LogoutView(View)
    """

    @staticmethod
    def get(request):
        """
        @staticmethod
        def get(request)
        """

        logout(request)
        return redirect("urban_development:login_page")


class RegisterView(View):
    """
    class RegisterView(View)
    """

    _context = {
        "title": "Registration Page",
        "action": "/urban_development/register/",
        "hyperlinks": {
            "Click here to log in": "/urban_development/login/",
        },
        "button": "Register",
    }

    def get(self, request):
        """
        def get(self, request)
        """

        self._context["form"] = RegisterForm()
        return render(request, "pages/register_and_change_password_page.html", context=self._context)

    def post(self, request):
        """
        def post(self, request)
        """

        form = RegisterForm(data=request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            return redirect("urban_development:send_activation_email_page", uid=user.id)

        self._context["form"] = form
        return render(request, "pages/register_and_change_password_page.html", context=self._context)


class SendActivationEmailView(View):
    """
    class SendActivationEmailView(View)
    """

    _context = {
        "hyperlinks": {
            "Click here to log in": "/urban_development/login/",
        },
    }

    def get(self, request, uid):
        """
        def get(self, request, uid)
        """

        self._context["hyperlinks"] = {
            **{
                "Click here to resend the activation email":
                    "/urban_development/send_activation_email/" + uid,
            },
            **self._context["hyperlinks"]
        }

        if send_email(uid, get_current_site(request).domain,
                      "Activate your Urban Development account.",
                      "pages/account_activation_email.html"):
            self._context["title"] = "Activation Email Sent"
            return render(request, "pages/register_and_change_password_page.html", context=self._context)

        self._context["title"] = "Activation Email Not Sent"
        return render(request, "templates/user_data_template.html", context=self._context)


class AccountActivatedView(View):
    """
    class AccountActivatedView(View)
    """

    _context = {
        "hyperlinks": {
            "Click here to log in": "/urban_development/login/",
        },
    }

    def get(self, request, uidb64, token):
        """
        def get(self, request, uidb64, token)
        """

        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, ObjectDoesNotExist):
            user = None

        if user is not None and TOKEN_GENERATOR.check_token(user, token):
            user.is_active = True
            user.save()
            self._context["title"] = "Account Activated Successfully"
            return render(request, "templates/user_data_template.html", context=self._context)

        self._context["title"] = "Invalid Activation Link"
        return render(request, "templates/user_data_template.html", context=self._context)


class ChangePasswordView(View):
    """
    class ChangePasswordView(View)
    """

    _context = {
        "title": "Change Password",
        "action": "/urban_development/change_password/",
        "hyperlinks": {
            "Click here to log in": "/urban_development/login/",
        },
        "button": "Change Password",
    }

    def get(self, request):
        """
        def get(self, request)
        """

        self._context["form"] = ChangePasswordForm()
        return render(request, "pages/register_and_change_password_page.html", context=self._context)

    def post(self, request):
        """
        def post(self, request)
        """

        form = ChangePasswordForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data.get("email")
            user = User.objects.get(email=email)
            return redirect("urban_development:send_change_password_email_page", uid=user.id)

        self._context["form"] = form
        return render(request, "pages/register_and_change_password_page.html", context=self._context)


class SendChangePasswordEmailView(View):
    """
    class SendChangePasswordEmailView(View)
    """

    _context = {
        "hyperlinks": {
            "Click here to log in": "/urban_development/login/",
        },
    }

    def get(self, request, uid):
        """
        def get(self, request, uid)
        """

        self._context["hyperlinks"] = {
            **{
                "Click here to resend the change password email":
                    "/urban_development/send_change_password_email/" + uid,
            },
            **self._context["hyperlinks"]
        }

        if send_email(uid, get_current_site(request).domain,
                      "Change the password for your Urban Development account.",
                      "pages/change_password_email.html"):
            self._context["title"] = "Change Password Email Sent"
            return render(request, "pages/register_and_change_password_page.html", context=self._context)

        self._context["title"] = "Change Password Email Not Sent"
        return render(request, "templates/user_data_template.html", context=self._context)


class PasswordChangedView(View):
    """
    class PasswordChangedView(View)
    """

    _form_context = {
        "title": "Change password",
        "hyperlinks": {
            "Click here to log in": "/urban_development/login/",
        },
        "button": "Change Password",
    }
    _context = {
        "hyperlinks": {
            "Click here to log in": "/urban_development/login/",
        },
    }

    def get(self, request, uidb64, token):
        """
        def get(self, request, uidb64, token)
        """

        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, ObjectDoesNotExist):
            user = None

        if user is not None and TOKEN_GENERATOR.check_token(user, token):
            form = NewPasswordForm(user=user)
            self._form_context["form"] = form
            self._form_context["action"] = "/urban_development/password_changed/" + uidb64 + "/" + token + "/"
            return render(request, "pages/register_and_change_password_page.html", context=self._form_context)

        self._context["title"] = "Password Not Changed"
        return render(request, "templates/user_data_template.html", context=self._context)

    def post(self, request, uidb64, token):
        """
        def post(self, request, uidb64, token)
        """

        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, ObjectDoesNotExist):
            user = None

        if user is not None and TOKEN_GENERATOR.check_token(user, token):
            form = NewPasswordForm(data=request.POST, user=user)

            if form.is_valid():
                new_password = form.cleaned_data.get("new_password1")
                user.set_password(new_password)
                user.save()
                self._context["title"] = "Password Changed Successfully"
                return render(request, "templates/user_data_template.html", context=self._context)

            self._form_context["form"] = form
            self._form_context["action"] = "/urban_development/password_changed/" + uidb64 + "/" + token + "/"
            return render(request, "pages/register_and_change_password_page.html", context=self._form_context)

        self._context["title"] = "Password Not Changed"
        return render(request, "templates/user_data_template.html", context=self._context)


class MapView(View):
    """
    class MapView(View)
    """

    @staticmethod
    def get(request):
        """
        @staticmethod
        def get(request)
        """

        context = {
            "years": collections.OrderedDict(sorted(extract_available_years().items(), reverse=True)),
        }
        return render(request, "pages/map_page.html", context=context)


class GetClassifiedTilesView(View):
    """
    class GetClassifiedAsView(View)
    """

    @staticmethod
    def get(_, parameters):
        """
        @staticmethod
        def get(_, parameters)
        """

        year = json.loads(parameters).get("year")
        classifications_for_year = Classification.objects.filter(year__lte=year)

        if len(classifications_for_year) <= 0:
            return HttpResponseBadRequest("No tiles have been classified for the selected year.")

        distinct_ids = classifications_for_year.values("tile_id").distinct()
        distinct_tiles = Tile.objects.filter(tile_id__in=distinct_ids.values_list("tile_id", flat=True))
        transformer = Transformer.from_crs("EPSG:28992", "EPSG:4326")
        result = {}

        for tile in distinct_tiles:
            coordinates = transform_tile_to_coordinates(tile.x_coordinate, tile.y_coordinate)
            x_coordinate, y_coordinate = transformer.transform(coordinates["x_coordinate"], coordinates["y_coordinate"])
            result[tile.tile_id] = {
                "xmin": coordinates["xmin"],
                "ymin": coordinates["ymin"],
                "xmax": coordinates["xmax"],
                "ymax": coordinates["ymax"],
                "x_coordinate": x_coordinate,
                "y_coordinate": y_coordinate,
                "year": -1,
                "classified_by": "",
                "contains_greenery": False,
                "greenery_percentage": 0,
                "greenery_rounded": 0,
            }

        for classification in classifications_for_year.values():
            if result[classification["tile_id"]]["year"] < classification["year"]:
                result[classification["tile_id"]]["year"] = classification["year"]

                if classification["classified_by"] == -1:
                    result[classification["tile_id"]]["classified_by"] = "classifier"
                elif classification["classified_by"] == -2:
                    result[classification["tile_id"]]["classified_by"] = "training data"
                else:
                    result[classification["tile_id"]]["classified_by"] = "user"

                result[classification["tile_id"]]["contains_greenery"] = classification["contains_greenery"]
                result[classification["tile_id"]]["greenery_percentage"] = 100 * classification["greenery_percentage"]

                if classification["contains_greenery"] and classification["greenery_percentage"] == 0:
                    result[classification["tile_id"]]["greenery_rounded"] = 25
                else:
                    result[classification["tile_id"]]["greenery_rounded"] = \
                        int(25 * ceil(100 * classification["greenery_percentage"] / 25))

        return JsonResponse(list(result.values()), safe=False)


class TransformCoordinatesView(View):
    """
    class TransformCoordinatesView(View):
    """
    @staticmethod
    def get(_, parameters):
        """
        def get(_, parameters):
        """
        x_coordinate = json.loads(parameters).get("x_coordinate")
        y_coordinate = json.loads(parameters).get("y_coordinate")
        year = json.loads(parameters).get("year")
        x_tile = x_coordinate - 13328.546
        x_tile /= 406.40102300613496932515337423313

        y_tile = 619342.658 - y_coordinate
        y_tile /= 406.40607802340702210663198959688

        x_tile = floor(x_tile) + 75120
        y_tile = floor(y_tile) + 75032
        tile_id = x_tile * 75879 + y_tile
        try:
            classification_year = -1
            classifications = Classification.objects.filter(tile=tile_id, year__lte=year)
            for classification in classifications.values():
                if classification["year"] > classification_year:
                    classification_year = classification["year"]
            contains_greenery = Classification.objects.get(tile=tile_id, year=classification_year).contains_greenery
            greenery_percentage = Classification.objects.get(tile=tile_id, year=classification_year).greenery_percentage
        except ObjectDoesNotExist:
            contains_greenery = "Unknown"
            greenery_percentage = "Unknown"
        transformer = Transformer.from_crs("EPSG:28992", "EPSG:4326")
        result = {
            "x_tile": x_tile,
            "y_tile": y_tile,
            "tile_id": tile_id,
            "x_coordinate": transformer.transform(x_coordinate, y_coordinate)[0],
            "y_coordinate": transformer.transform(x_coordinate, y_coordinate)[1],
            "contains_greenery": contains_greenery,
            "greenery_percentage": greenery_percentage
        }
        return JsonResponse(result, safe=False)


class ManualClassificationView(View):
    """
    class ManualClassificationView(View):
    """
    @staticmethod
    def get(_, parameters):
        """
        def get(_, parameters):
        """
        x_coordinate = json.loads(parameters).get("latitude")
        y_coordinate = json.loads(parameters).get("longitude")
        x_tile, y_tile = transform_coordinates_to_tile(x_coordinate, y_coordinate)

        year = json.loads(parameters).get("year")
        user = json.loads(parameters).get("classified_by")
        greenery_percentage = json.loads(parameters).get("greenery_percentage")
        contains_greenery = json.loads(parameters).get("contains_greenery")
        coordinates = transform_tile_to_coordinates(x_tile, y_tile)
        manual_classify(x_coordinate, y_coordinate, year, user, greenery_percentage, contains_greenery)
        if contains_greenery == "True" and greenery_percentage == 0:
            contains_greenery = "true"
            greenery_rounded = 25
        elif contains_greenery == "False":
            contains_greenery = "false"
            greenery_rounded = 0
        else:
            contains_greenery = "true"
            greenery_rounded = int(25 * ceil(100 * float(greenery_percentage) / 25))
        print(greenery_rounded)
        result = {
            "xmin": coordinates["xmin"],
            "ymin": coordinates["ymin"],
            "xmax": coordinates["xmax"],
            "ymax": coordinates["ymax"],
            "contains_greenery": contains_greenery,
            "greenery_percentage": greenery_percentage,
            "greenery_rounded": greenery_rounded,
            "x_coordinate": x_coordinate,
            "y_coordinate": y_coordinate
        }
        return JsonResponse(result, safe=False)


class HowToUseView(View):
    """
    class HowToUseView(View)
    """

    @staticmethod
    def get(request):
        """
        @staticmethod
        def get(request)
        """

        return render(request, "pages/how_to_use.html")
