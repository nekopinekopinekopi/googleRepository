from django.core.management.base import BaseCommand

# settings.pyのINSTALLED_APPSに書かれてる順番の通りに優先順位が決まる。
# このcommandsディレクトリの中のファイル名を他のアプリのファイル名と同じ名前にした場合の話です

class Command(BaseCommand):
    help = 'ユーザ情報を表示するバッチです'
    # ↑の呼び出し方→python manage.py help sample_advanced
    # ターミナルに、変数と「help=〇〇」を付けたものが表示される。その内容を表すヒントになるものを入れたりする

    def add_arguments(self, parser):
        parser.add_argument('name', type=str, help='名前')  
        parser.add_argument('age', type=int, help='年齢')  
        parser.add_argument('--birthday', help='誕生日', default='2020-01-01')   # コマンド入力時に「--birthday 〇〇〇〇」を入れなくても初期値的な感じでdefaultが入ってる
        parser.add_argument('three_words', nargs=3)  # 今回だと、３つの変数をリスト化して表示するよ、っていう意味。
        # ↑の呼び出し方　python manage.py sample_advanced Taro 20 Hello Goodbye Hi
        # HelloとGoodbyeとHiが３つの変数と認識されてリスト化されてターミナルに表示される
        parser.add_argument('--active', action='store_true')  # 「action=」は、このカッコ内で指定した変数？引数？(今回だったら--active)がコマンドで入力されると、Trueを返すよ、という意味
        parser.add_argument('--color', choices=['Blue', 'Red', 'Yellow'])  # 「choices=」は、指定したものの中からしか選べないという意味。
    
    def handle(self, *args, **options):
        name = options['name']  
        age = options['age']  
        birthday = options['birthday']
        three_words = options['three_words']
        active = options['active']
        print(
            f'name = {name}, age = {age}, birthday = {birthday}, three_words = {three_words}'
        )
        print(active)# コマンドで「--active」を入力すれば「True」が返され、「--active」を入力しなければ「False」が返される

        color = options['color']
        if color == 'Blue':
            print('青')
        elif color == 'Red':
            print('赤')
        elif color == 'Yellow':
            print('黄')
        # ↑呼び出し方→「--color」に、「choices=」で指定したどれかをコマンドで入力すれば、printされます
    