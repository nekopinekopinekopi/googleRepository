from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, Http404
from django.views.generic.base import TemplateView
from django.views.generic.edit import (
    UpdateView, DeleteView, CreateView
)
from django.urls import reverse_lazy
from django.core.cache import cache
from django.db import transaction

import os
from .models import (
    Products, Carts, CartItems, Addresses,
    Orders, OrderItems
)
from .forms import (
    CartUpdateForm, AddressInputForm, 
)

class ProductListView(LoginRequiredMixin, ListView):
    model = Products
    template_name = os.path.join('stores', 'product_list.html')

    # 商品タイプと商品名で絞り込めて値段の昇順降順を決められるメソッド
    def get_queryset(self):  # オーバーライドしてる
        query = super().get_queryset()
        product_type_name = self.request.GET.get('product_type_name', None)
        product_name = self.request.GET.get('product_name', None)
        if product_type_name:
            query = query.filter(
                product_type__name=product_type_name  # product_type__nameはnameカラムで絞り込むことを意味している
            )
        if product_name:
            query = query.filter(
                name=product_name
            )
        order_by_price = self.request.GET.get('order_by_price', 0)
        if order_by_price == '1':
            query = query.order_by('price')
        elif order_by_price == '2':
            query = query.order_by('-price')
        return query

    # 商品タイプの実行するボタン押した後に検索ワードがそのまま検索窓に残ってるようにする処理
    def get_context_data(self, **kwargs):  # そのtempleteで用いる変数を設定するメソッド
        context = super().get_context_data(**kwargs)
        context['product_type_name'] = self.request.GET.get('product_type_name', '')
        context['product_name'] = self.request.GET.get('product_name', '')
        order_by_price = self.request.GET.get('order_by_price', 0)
        if order_by_price == '1':
            context['ascending'] = True
        elif order_by_price == '2':
            context['descending'] = True
        return context


# 商品の詳細画面を表示する
class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Products
    template_name = os.path.join('stores', 'product_detail.html')

    # 同じ商品を再登録できないように、カートの中のデータを取得する
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_added'] = CartItems.objects.filter(
            cart_id=self.request.user.id,
            product_id=kwargs.get('object').id
        ).first()
        return context


# カートに商品を追加するメソッド
@login_required
def add_product(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':  # Udemyで使っているis_ajaxメソッドはdjango4で削除されてしまったため、代わりに使うものを入力してます
        product_id = request.POST.get('product_id')
        quantity = request.POST.get('quantity')
        product = get_object_or_404(Products, id=product_id)
        if int(quantity) > product.stock:
            response = JsonResponse({'message': '在庫数を超えています'})
            response.status_code = 403  # エラーを発生させたいから(?)こうやってstatus_codeを変更する必要がある
            return response
        if int(quantity) <= 0:
            response = JsonResponse({'message': '0より大きい値を入力してください'})
            response.status_code = 403
            return response
        cart = Carts.objects.get_or_create(
            user=request.user
        )  # get_or_createメソッドは、userに合ったcartが存在すれば存在しているものを返して、存在しなければuserを作る
        if all([product_id, cart, quantity]):
            CartItems.objects.save_item(
                quantity=quantity, product_id=product_id,
                cart=cart[0]
            )
            return JsonResponse({'message': '商品をカートに追加しました'})
        
        

# カートの中身を表示する
class CartItemsView(LoginRequiredMixin, TemplateView):
    template_name = os.path.join('stores', 'cart_items.html')  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.request.user.id
        query = CartItems.objects.filter(cart_id=user_id)
        total_price = 0                     
        items = []
        for item in query.all():
            total_price += item.quantity * item.product.price  # カート内商品の値段の合計をだす処理
            picture = item.product.productpictures_set.first()  # ProductPicturesモデルから逆にproductを引っ張ってきて、productについてる写真の一番最初のものを表示するという意味
            picture = picture.picture if picture else None
            in_stock = True if item.product.stock >= item.quantity else False  # 自身が入れた数をストックが超えていればTrue
            tmp_item = {
                'quantity': item.quantity,
                'picture': picture,
                'name': item.product.name,
                'id': item.id,
                'price': item.product.price,
                'in_stock': in_stock,
            }
            items.append(tmp_item)
        context['total_price'] = total_price
        context['items'] = items
        return context
        
        
        
# カートの中身を編集する
class CartUpdateView(LoginRequiredMixin, UpdateView):
    template_name = os.path.join('stores', 'update_cart.html')
    form_class = CartUpdateForm
    model = CartItems
    success_url = reverse_lazy('stores:cart_items')


# カートの中身のものを削除する
class CartDeleteView(LoginRequiredMixin, DeleteView):
    template_name = os.path.join('stores', 'delete_cart.html')
    model = CartItems
    success_url = reverse_lazy('stores:cart_items')


# 住所を入力する
class InputAddressView(LoginRequiredMixin, CreateView):
    template_name = os.path.join('stores', 'input_address.html')
    form_class = AddressInputForm
    success_url = reverse_lazy('stores:confirm_order')

    # カートに何も商品がなかった場合は、住所登録をさせないようにする
    def get(self, request, pk=None):  # この引数のpkはアドレスのpkを指している。(今まで入力した住所をクリックするだけでformに入力できる部分でこの引数を追加した)
        cart = get_object_or_404(Carts, user_id=request.user.id)
        if not cart.cartitems_set.all():
            raise Http404('商品が入っていません')
        return super().get(request, pk)


    # Templateに初期値で渡す値を記述する
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        address = cache.get(f'address_user_{self.request.user.id}')
        pk = self.kwargs.get('pk')
        address = get_object_or_404(Addresses, user_id=self.request.user.id, pk=pk) if pk else address
        if address:
            context['form'].fields['zip_code'].initial = address.zip_code
            context['form'].fields['prefecture'].initial = address.prefecture
            context['form'].fields['address'].initial = address.address
        context['addresses'] = Addresses.objects.filter(user=self.request.user).all()  # 住所一覧をcontextに追加する
        return context


    # formが送信された際にそのformのバリデーションを行うメソッド
    def form_valid(self, form):
        form.user = self.request.user  # AddressInputFormの中にuserを指定する
        return super().form_valid(form)

    
# 注文を行う
class ConfirmOrderView(LoginRequiredMixin, TemplateView):
    template_name = os.path.join('stores', 'confirm_order.html')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        address = cache.get(f'address_user_{self.request.user.id}')
        context['address'] = address
        cart = get_object_or_404(Carts, user_id=self.request.user.id)
        context['cart'] = cart
        total_price = 0
        items = []
        for item in cart.cartitems_set.all():
            total_price += item.quantity * item.product.price
            picture = item.product.productpictures_set.first()
            picture = picture.picture if picture else None
            tmp_item = {
                'quantity': item.quantity,
                'picture': picture,
                'name': item.product.name,
                'price': item.product.price,
                'id': item.id,
            }
            items.append(tmp_item)
        context['total_price'] = total_price
        context['items'] = items
        return context
    
    
    # 注文処理
    @transaction.atomic  # データベースの原子性のデコレータ(原子性とは、トランザクションの全ての操作が完全に成功するか、全てがロールバックされて失敗するかのどちらかであることを保証する性質)
    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        address = context.get('address')
        cart = context.get('cart')
        total_price = context.get('total_price')
        if (not address) or (not cart) or (not total_price):  # addressかcartかtotal_price、いずれかがなかった場合エラーになる
            raise Http404('注文処理でエラーが発生しました')
        for item in cart.cartitems_set.all():
            if item.quantity > item.product.stock:  # 注文の数がストックを超えていた場合、エラーになる
                raise Http404('注文処理でエラーが発生しました')
        order = Orders.objects.insert_cart(cart, address, total_price)
        OrderItems.objects.insert_cart_items(cart, order)  # OrderItemsに商品を追加する処理
        Products.objects.reduce_stock(cart)  # カートの商品の数だけ、ストックの数を減らす
        cart.delete()  # CartItemsでCASCADEにしているのでCartItemsも一緒に削除される
        return redirect(reverse_lazy('stores:order_success'))



# 注文が成功しました処理
class OrderSuccessView(LoginRequiredMixin, TemplateView):
    
    template_name = os.path.join('stores', 'order_success.html')
    
    
    