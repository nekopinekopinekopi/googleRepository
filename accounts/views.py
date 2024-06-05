from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, FormView
from django.views.generic.base import TemplateView, View
from .forms import RegistForm, UserLoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView





# ホーム画面表示
class HomeView(TemplateView):
    template_name = 'home.html'


# ユーザー登録
class RegistUserView(CreateView):
    template_name = 'regist.html'
    form_class = RegistForm
    

# ログイン処理
# class UserLoginView(FormView):
#     template_name = 'user_login.html'
#     form_class = UserLoginForm        # ここ２行でログイン画面に何を表示させるかを決めた 

#     def post(self, request, *args, **kwargs):
#         email = request.POST['email']
#         password = request.POST['password']
#         user = authenticate(email=email, password=password)
#         next_url = request.POST['next']
#         if user is not None and user.is_active:
#             login(request, user)
#         if next_url:
#             return redirect(next_url)
#         return redirect('accounts:home')
class UserLoginView(LoginView):
    template_name = 'user_login.html'
    authentication_form = UserLoginForm

    def form_valid(self, form):
        remember = form.cleaned_data['remember']
        if remember:
            self.request.session.set_expiry(1200000)
        return super().form_valid(form)



# ログアウト処理
# class UserLogoutView(View):
    
#     def get(self, request, *args, **kwargs):
#         logout(request)
#         return redirect('accounts:user_login')
class UserLogoutView(LogoutView):
    pass  # settings.pyにLOGOUT_REDIRECT_URLを定義しただけ！


# ログインしてないと見れない画面の表示
# @method_decorator(login_required, name='dispatch')  # dispatchメソッドにlogin_requiredがデコレーションされた
class UserView(LoginRequiredMixin, TemplateView):  # ここにLoginRequiredMixinをいれてもログインしてないとダメ設定ができる
    template_name = 'user.html'

    # @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):  # getやPOST等Httpメソッドであれば実行されるメソッド(?)
        return super().dispatch(*args, **kwargs)