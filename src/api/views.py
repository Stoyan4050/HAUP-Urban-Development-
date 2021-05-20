import collections
import json
import requests
from .email import send_email
from .forms import ChangePasswordForm, RegisterForm, LoginForm, NewPasswordForm
from .models import Classification, Tile, User
from .tile_to_coordinates_transformer import TileToCoordinatesTransformer
from .tokens import token_generator
from bs4 import BeautifulSoup
from django.contrib.auth import authenticate, login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Q
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import redirect, render
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.views import View
from pyproj import Transformer

class LoginView(View):
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
        self._context["form"] = LoginForm()
        return render(request, "pages/login_page.html", context=self._context)
    
    def post(self, request):
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

class RegisterView(View):
    _context = {
        "title": "Registration Page",
        "action": "/urban_development/register/",
        "hyperlinks": {
            "Click here to log in": "/urban_development/login/",
        },
        "button": "Register",
    }

    def get(self, request):
        self._context["form"] = RegisterForm()
        return render(request, "pages/register_and_change_password_page.html", context=self._context)

    def post(self, request):
        form = RegisterForm(data=request.POST)
        
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            return redirect("urban_development:send_activation_email_page", uid=user.id)
        
        self._context["form"] = form
        return render(request, "pages/register_and_change_password_page.html", context=self._context)

class SendActivationEmailView(View):
    _context = {
        "hyperlinks": {
            "Click here to log in": "/urban_development/login/",
        } ,
    }

    def get(self, request, uid):
        self._context["hyperlinks"] = {**{"Click here to resend the activation email": "/urban_development/send_activation_email/" + uid}, **self._context["hyperlinks"]}

        if send_email(uid, get_current_site(request).domain, "Activate your Urban Development account.", "pages/account_activation_email.html"):
            self._context["title"] = "Activation Email Sent"
            return render(request, "pages/register_and_change_password_page.html", context=self._context)

        self._context["title"] = "Activation Email Not Sent"
        return render(request, "templates/user_data_template.html", context=self._context)

class AccountActivatedView(View):
    _context = {
        "hyperlinks": {
            "Click here to log in": "/urban_development/login/",
        },
    }

    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            self._context["title"] = "Account Activated Successfully"
            return render(request, "templates/user_data_template.html", context=self._context)
    
        self._context["title"] = "Invalid Activation Link"
        return render(request, "templates/user_data_template.html", context=self._context)

class ChangePasswordView(View):
    _context = {
        "title": "Change Password",
        "action": "/urban_development/change_password/",
        "hyperlinks": {
            "Click here to log in": "/urban_development/login/",
        },
        "button": "Change Password",
    }

    def get(self, request):
        self._context["form"] = ChangePasswordForm()
        return render(request, "pages/register_and_change_password_page.html", context=self._context)

    def post(self, request):
        form = ChangePasswordForm(request.POST)
        
        if form.is_valid():
            email = form.cleaned_data.get("email")
            user = User.objects.get(email=email)
            return redirect("urban_development:send_change_password_email_page", uid=user.id)

        self._context["form"] = form
        return render(request, "pages/register_and_change_password_page.html", context=self._context)

class SendChangePasswordEmailView(View):
    _context = {
        "hyperlinks": {
            "Click here to log in": "/urban_development/login/",
        } ,
    }

    def get(self, request, uid):
        self._context["hyperlinks"] = {**{"Click here to resend the change password email": "/urban_development/send_change_password_email/" + uid}, **self._context["hyperlinks"]}

        if send_email(uid, get_current_site(request).domain, "Change the password for your Urban Development account.", "pages/change_password_email.html"):
            self._context["title"] = "Change Password Email Sent"
            return render(request, "pages/register_and_change_password_page.html", context=self._context)
        
        self._context["title"] = "Change Password Email Not Sent"
        return render(request, "templates/user_data_template.html", context=self._context)

class PasswordChangedView(View):
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
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
    
        if user is not None and token_generator.check_token(user, token):
            form = NewPasswordForm(user=user)
            self._form_context["form"] = form
            self._form_context["action"] = "/urban_development/password_changed/" + uidb64 + "/" + token + "/"
            return render(request, "pages/register_and_change_password_page.html", context=self._form_context)
    
        self._context["title"] = "Password Not Changed"
        return render(request, "templates/user_data_template.html", context=self._context)

    def post(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and token_generator.check_token(user, token):
            form = NewPasswordForm(data=request.POST, user=user)

            if form.is_valid():
                new_password = form.cleaned_data.get("new_password1")
                user.set_password(new_password)
                user.save()
                self._context["title"] = "Password Changed Successfully"
                return render(request, "templates/user_data_template.html", context=self._context)
            else:
                self._form_context["form"] = form
                self._form_context["action"] = "/urban_development/password_changed/" + uidb64 + "/" + token + "/"
                return render(request, "pages/register_and_change_password_page.html", context=self._form_context)

        self._context["title"] = "Password Not Changed"
        return render(request, "templates/user_data_template.html", context=self._context)

class MapView(View):
    _context = {
        "map_view": True,
    }

    def get(self, request):
        page = requests.get("https://tiles.arcgis.com/tiles/nSZVuSZjHpEZZbRo/arcgis/rest/services")
        soup = BeautifulSoup(page.content, 'html.parser')
        years = {}
        
        for hyperlink in soup.select("ol[id=serviceList] > li > a[id=l1]"):
            if hyperlink.text.startswith("Historische_tijdreis_"):
                reference = hyperlink.text[len("Historische_tijdreis_") : ]

                if "_" in reference:
                    for i in range(int(reference[ : reference.index("_")]), int(reference[reference.index("_") + 1 : ]) + 1):
                        years[i] = reference
                else:
                    years[int(reference)] = reference
        
        self._context["years"] = collections.OrderedDict(sorted(years.items(), reverse=True))
        return render(request, "pages/map_page.html", context=self._context)

class GetClassifiedAsView(View):
    def get(self, request, parameters):
        params = json.loads(parameters)
        classifications_for_year = Classification.objects.filter(year__lte=params.get("year"))

        if len(classifications_for_year) == 0:
            return HttpResponseBadRequest("No classified tiles for the selected year.")

        all_ids = classifications_for_year.values("tile_id").distinct()
        public_space_ids = classifications_for_year.filter(~Q(label="not a public space")).values("tile_id").distinct()
        not_public_space_ids = classifications_for_year.filter(label="not a public space").values("tile_id").distinct()

        all_tiles = Tile.objects.filter(tid__in=all_ids.values_list("tile_id", flat=True))
        public_space_tiles = Tile.objects.filter(tid__in=public_space_ids.values_list("tile_id", flat=True))
        not_public_space_tiles = Tile.objects.filter(tid__in=not_public_space_ids.values_list("tile_id", flat=True))

        result = {}

        tile_to_coordinates_transformer = TileToCoordinatesTransformer()
        coordinates_transformer = Transformer.from_crs("EPSG:28992", "EPSG:4326")
        
        for tile in all_tiles:
            coordinates = tile_to_coordinates_transformer.transform(tile.x_coordinate, tile.y_coordinate)
            center_coordinates = coordinates_transformer.transform(coordinates["x_coordinate"], coordinates["y_coordinate"])
            result[tile.tid] = {
                "xmin": coordinates["xmin"],
                "ymin": coordinates["ymin"],
                "xmax": coordinates["xmax"],
                "ymax": coordinates["ymax"],
                "x_coordinate": center_coordinates[0],
                "y_coordinate": center_coordinates[1],
                "public_space": False,
                "not_public_space": False,
            }

        for tile in public_space_tiles:
            result[tile.tid]["public_space"] = True

        for tile in not_public_space_tiles:
            result[tile.tid]["not_public_space"] = True

        return JsonResponse(list(result.values()), safe=False)

class GetClassifiedByView(View):
    def get(self, request, parameters):
        params = json.loads(parameters)
        classifications_for_year = Classification.objects.filter(year__lte=params.get("year"))

        if len(classifications_for_year) == 0:
            return HttpResponseBadRequest("No classified tiles for the selected year.")

        all_ids = classifications_for_year.values("tile_id").distinct()
        user_ids = classifications_for_year.filter(classified_by__gt=0).values("tile_id").distinct()
        classifier_ids = classifications_for_year.filter(classified_by=-1).values("tile_id").distinct()
        training_data_ids = classifications_for_year.filter(classified_by=-2).values("tile_id").distinct()

        all_tiles = Tile.objects.filter(tid__in=all_ids.values_list("tile_id", flat=True))
        user_tiles = Tile.objects.filter(tid__in=user_ids.values_list("tile_id", flat=True))
        classifier_tiles = Tile.objects.filter(tid__in=classifier_ids.values_list("tile_id", flat=True))
        training_data_tiles = Tile.objects.filter(tid__in=training_data_ids.values_list("tile_id", flat=True))

        result = {}

        tile_to_coordinates_transformer = TileToCoordinatesTransformer()
        coordinates_transformer = Transformer.from_crs("EPSG:28992", "EPSG:4326")

        for tile in all_tiles:
            coordinates = tile_to_coordinates_transformer.transform(tile.x_coordinate, tile.y_coordinate)
            center_coordinates = coordinates_transformer.transform(coordinates["x_coordinate"], coordinates["y_coordinate"])
            result[tile.tid] = {
                "xmin": coordinates["xmin"],
                "ymin": coordinates["ymin"],
                "xmax": coordinates["xmax"],
                "ymax": coordinates["ymax"],
                "x_coordinate": center_coordinates[0],
                "y_coordinate": center_coordinates[1],
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

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("urban_development:login_page")

class GuestView(View):
    def get(self, request):
        logout(request)
        return redirect("urban_development:map_page")

class BaseView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("urban_development:map_page")
        
        return redirect("urban_development:login_page")
