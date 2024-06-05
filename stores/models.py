from django.db import models
from accounts.models import Users


# 商品の種類を表す
class ProductTypes(models.Model):
    name = models.CharField(max_length=1000)

    class Meta:
        db_table = 'product_types'

    def __str__(self):
        return self.name
    

#　Manufacturers=製造者、メーカー
class Manufacturers(models.Model):
    name = models.CharField(max_length=1000)
    
    class Meta:
        db_table = 'manufacturers'

    def __str__(self):
        return self.name





# カートの商品の数だけ、ストックの数を減らす
class ProductsManager(models.Manager):
    
    def reduce_stock(self, cart):
        for item in cart.cartitems_set.all():
            update_stock = item.product.stock - item.quantity
            item.product.stock = update_stock
            item.product.save()



# 商品情報
class Products(models.Model):
    name = models.CharField(max_length=1000)
    price = models.IntegerField()
    stock = models.IntegerField()
    product_type = models.ForeignKey(
        ProductTypes, on_delete=models.CASCADE
    )
    manufacturer = models.ForeignKey(
        Manufacturers, on_delete=models.CASCADE
    )
    objects = ProductsManager()
    
    class Meta:
        db_table = 'products'

    def __str__(self):
        return self.name
    

# 商品写真  
class ProductPictures(models.Model):
    picture = models.FileField(upload_to='product_pictures/')
    product = models.ForeignKey(
        Products, on_delete=models.CASCADE
    )
    order = models.IntegerField()  # 写真が表示される順番を決めるためにorderがある

    class Meta:
        db_table = 'product_pictures'
        ordering = ['order']  # ProductPicturesテーブルからデータを取り出す際にどのカラムで並び替えるかを決められる。昇順なので、orderが最小のものから取り出すことができる

    def __str__(self):
        return self.product.name + ':' + str(self.order)



# 製品のかごを作ります。１アカウントにつき１個
class Carts(models.Model):
    user = models.OneToOneField(
        Users,
        on_delete=models.CASCADE,
        primary_key=True
    )
    
    class Meta:
        db_table = 'carts'
 
 
 
# save_itemメソッドを作りました
class CartItemsManager(models.Manager):
     
     def save_item(self, product_id, quantity, cart):
         c = self.model(quantity=quantity, product_id=product_id, cart=cart)        
         c.save()
        
        
        

# かごの中の製品を表す
class CartItems(models.Model):
    quantity = models.PositiveIntegerField()  # 実際に入れる製品の数
    product = models.ForeignKey(
        Products, on_delete=models.CASCADE
    )
    cart = models.ForeignKey(
        Carts, on_delete=models.CASCADE
    )
    objects = CartItemsManager()
    
    class Meta:
        db_table = 'cart_items'
        unique_together = [['product', 'cart']]  # 同じカートに同じ商品を入れないようにする




# 住所登録
class Addresses(models.Model):
    zip_code = models.CharField(max_length=8)     # 郵便番号
    prefecture = models.CharField(max_length=10)  # 都道府県
    address = models.CharField(max_length=200)    # 以下住所
    user = models.ForeignKey(
        Users, 
        on_delete=models.CASCADE,
    )
    
    class Meta:
        db_table = 'addresses'
        unique_together = [
            ['zip_code', 'prefecture', 'address', 'user']  # 3つ全ての値と同一のデータがあれば、それは登録できない(同じユーザーに対して同じ住所は一つしか登録できない)
        ]          

    def __str__(self):
        return f'{self.zip_code} {self.prefecture} {self.address}'




class OrdersManager(models.Manager):
    
    def insert_cart(self, cart: Carts, address, total_price):
        return self.create(  # createメソッドでデータベースに商品を追加することができる
            total_price=total_price,
            address=address,
            user=cart.user
        )



# 注文した商品の合計金額、注文した人の住所、注文した人のidをテーブルに格納する
class Orders(models.Model):
    total_price = models.PositiveIntegerField()  # 合計金額
    address = models.ForeignKey(  # 住所
        Addresses,
        on_delete=models.SET_NULL,  # addressが削除されたら、OrdersモデルのフィールドにはNULLが入る
        blank=True,
        null=True
    )
    user = models.ForeignKey(  # 人
        Users,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    objects = OrdersManager()
    
    class Meta:
        db_table = 'orders'





class OrderItemsManager(models.Manager):
    
    def insert_cart_items(self, cart, order):
        for item in cart.cartitems_set.all():  # カートの中に入ってる商品を全てインサートする(挿入という意味)
            self.create(
                quantity=item.quantity,
                product=item.product,
                order=order
            )


# 注文した個数、注文番号(?)(idみたいな)、注文した商品、
class OrderItems(models.Model):
    quantity = models.PositiveIntegerField()  # 個数
    product = models.ForeignKey(  # 製品
        Products,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    order = models.ForeignKey(
        Orders, on_delete=models.CASCADE
    )
    objects = OrderItemsManager()
    
    class Meta:
        db_table = 'order_items'
        unique_together = [['product', 'order']]