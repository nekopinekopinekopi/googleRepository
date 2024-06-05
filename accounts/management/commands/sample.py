from django.core.management.base import BaseCommand

# settings.pyのINSTALLED_APPSに書かれてる順番の通りに優先順位が決まる。
# このcommandsディレクトリの中のファイル名を他のアプリのファイル名と同じ名前にした場合の話です

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('name')  # 第１引数
        parser.add_argument('age')  # 第２引数
        parser.add_argument('--birthday')  # --を付ける意味とは？って思ったけど、--を付けると、コマンド入力するときに--の名前も指定したい引数と一緒に入力するから、コマンド文だけ見てもこの引数はなんの情報だっていうのが分かりやすい！
    
    # 呼び出し方
    # python manage.py sample Taro 20 --birthday 2000-01-01 
    def handle(self, *args, **options):
        name = options['name']  # add_argumentsで格納した値を取り出す
        age = options['age']  # add_argumentsで格納した値を取り出す
        birthday = options['birthday']
        print(f'name = {name}, age = {age}, birthday = {birthday}')
        
    