from django.core.management.base import BaseCommand

# settings.pyのINSTALLED_APPSに書かれてる順番の通りに優先順位が決まる。
# このcommandsディレクトリの中のファイル名を他のアプリのファイル名と同じ名前にした場合の話です


class Command(BaseCommand):
    
    def handle(self, *args, **kwargs):
        print('storeのバッチを実行')