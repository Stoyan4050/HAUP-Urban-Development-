"""
views.py
"""

import collections
import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import redirect, render
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.views import View
from pyproj import Transformer
from .forms import ChangePasswordForm, RegisterForm, LoginForm, NewPasswordForm
from .models import Classification, Tile, User
from .tokens import TOKEN_GENERATOR
from .utils import extract_available_years, send_email, transform_tile_to_coordinates


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


class GetClassifiedAsView(View):
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

        all_ids = classifications_for_year.values("tile_id").distinct()
        public_space_ids = classifications_for_year.filter(~Q(label="not a public space")).values("tile_id").distinct()
        not_public_space_ids = classifications_for_year.filter(label="not a public space").values("tile_id").distinct()

        all_tiles = Tile.objects.filter(tid__in=all_ids.values_list("tile_id", flat=True))
        public_space_tiles = Tile.objects.filter(tid__in=public_space_ids.values_list("tile_id", flat=True))
        not_public_space_tiles = Tile.objects.filter(tid__in=not_public_space_ids.values_list("tile_id", flat=True))

        transformer = Transformer.from_crs("EPSG:28992", "EPSG:4326")
        result = {}

        for tile in all_tiles:
            coordinates = transform_tile_to_coordinates(tile.x_coordinate, tile.y_coordinate)
            x_coordinate, y_coordinate = transformer.transform(coordinates["x_coordinate"], coordinates["y_coordinate"])
            result[tile.tid] = {
                "xmin": coordinates["xmin"],
                "ymin": coordinates["ymin"],
                "xmax": coordinates["xmax"],
                "ymax": coordinates["ymax"],
                "x_coordinate": x_coordinate,
                "y_coordinate": y_coordinate,
                "public_space": False,
                "not_public_space": False,
            }

        for tile in public_space_tiles:
            result[tile.tid]["public_space"] = True

        for tile in not_public_space_tiles:
            result[tile.tid]["not_public_space"] = True

        return JsonResponse(list(result.values()), safe=False)


class GetClassifiedByView(View):
    """
    class GetClassifiedByView(View)
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

        all_ids = classifications_for_year.values("tile_id").distinct()
        user_ids = classifications_for_year.filter(classified_by__gt=0).values("tile_id").distinct()
        classifier_ids = classifications_for_year.filter(classified_by=-1).values("tile_id").distinct()
        training_data_ids = classifications_for_year.filter(classified_by=-2).values("tile_id").distinct()

        all_tiles = Tile.objects.filter(tid__in=all_ids.values_list("tile_id", flat=True))
        user_tiles = Tile.objects.filter(tid__in=user_ids.values_list("tile_id", flat=True))
        classifier_tiles = Tile.objects.filter(tid__in=classifier_ids.values_list("tile_id", flat=True))
        training_data_tiles = Tile.objects.filter(tid__in=training_data_ids.values_list("tile_id", flat=True))

        transformer = Transformer.from_crs("EPSG:28992", "EPSG:4326")
        result = {}

        for tile in all_tiles:
            coordinates = transform_tile_to_coordinates(tile.x_coordinate, tile.y_coordinate)
            x_coordinate, y_coordinate = transformer.transform(coordinates["x_coordinate"], coordinates["y_coordinate"])
            result[tile.tid] = {
                "xmin": coordinates["xmin"],
                "ymin": coordinates["ymin"],
                "xmax": coordinates["xmax"],
                "ymax": coordinates["ymax"],
                "x_coordinate": x_coordinate,
                "y_coordinate": y_coordinate,
                "user": False,
                "classifier": False,
                "training_data": False,
            }

        for tile in user_tiles:
            result[tile.tid]["user"] = True

        for tile in classifier_tiles:
            result[tile.tid]["classifier"] = True

        for tile in training_data_tiles:
            result[tile.tid]["training_data"] = True

        return JsonResponse(list(result.values()), safe=False)


class GetDataView(View):
    """
    class GetDataView(View)
    """

    @staticmethod
    def get(_, parameters):
        """
        @staticmethod
        def get(_, parameters)
        """

        year = json.loads(parameters).get("year")
        classifications_for_year = Classification.objects.filter(year__lte=year)

        total = classifications_for_year.values("tile_id").distinct()
        public_space = classifications_for_year.filter(
            ~Q(label="not a public space")).values("tile_id").distinct()
        not_public_space = classifications_for_year.filter(
            label="not a public space").values("tile_id").distinct()
        mixed = public_space.filter(
            tile_id__in=not_public_space.values_list("tile_id", flat=True))
        user = classifications_for_year.filter(
            classified_by__gt=0).values("tile_id").distinct()
        classifier = classifications_for_year.filter(
            classified_by=-1).values("tile_id").distinct()
        training_data = classifications_for_year.filter(
            classified_by=-2).values("tile_id").distinct()
        user_classifier = user.filter(
            tile_id__in=classifier.values_list("tile_id", flat=True)).values("tile_id").distinct()
        user_training_data = user.filter(
            tile_id__in=training_data.values_list("tile_id", flat=True)).values("tile_id").distinct()
        classifier_training_data = classifier.filter(
            tile_id__in=training_data.values_list("tile_id", flat=True)).values("tile_id").distinct()
        user_classifier_training_data = user_classifier.filter(
            tile_id__in=training_data.values_list("tile_id", flat=True)).values("tile_id").distinct()

        result = {
            "total": len(total),
            "public_space": len(public_space),
            "not_public_space": len(not_public_space),
            "mixed": len(mixed),
            "user": len(user),
            "classifier": len(classifier),
            "training_data": len(training_data),
            "user_classifier": len(user_classifier),
            "user_training_data": len(user_training_data),
            "classifier_training_data": len(classifier_training_data),
            "user_classifier_training_data": len(user_classifier_training_data),
        }

        return JsonResponse(result, safe=False)
