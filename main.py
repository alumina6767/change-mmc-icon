# MMCのアイコンを指定したファイルに変更する

import zipfile
import sys
from os import path
import tkinter.filedialog
import shutil
import tempfile


def get_file_path(file_type, title):

    # アプリケーションのパスを取得
    if getattr(sys, 'frozen', False):
        application_path = path.dirname(sys.executable)
    elif __file__:
        application_path = path.dirname(__file__)

    file_path = None
    file_path = tkinter.filedialog.askopenfilename(
        filetypes=[(file_type.upper() + "ファイル", "*." + file_type)],
        initialdir=path.abspath(application_path),
        title=title
    )

    # キャンセル時の処理
    if file_path == "":
        print("エラー: ファイルが選択されませんでした。")
        input()
        sys.exit()

    return file_path


# ZIPファイルの選択
print("MMCのZIPファイルを選択してください...")
ZIN_PATH = get_file_path("zip", "MMCのZIPファイルを選択してください")

# 画像ファイルの選択
print("差し替える画像ファイルを選択してください...")
IMG_PATH = get_file_path("png", "差し替える画像ファイルを選択してください")

# ZIPファイル内のアイコンを差し替え
with zipfile.ZipFile(ZIN_PATH, 'r') as zin_file:

    # 現在の指定アイコンを確認
    with zin_file.open('instance.cfg', 'r') as cfg_file:
        for l in cfg_file.readlines():
            ll = l.decode('utf-8').strip()
            if ll.startswith('iconKey='):
                icon_path = ll.split('=')[-1]
                break

    print("現在のアイコンは" + icon_path + "です。")
    print(f"アイコンを{IMG_PATH}に差し替えます...")

    icon_name = path.basename(IMG_PATH).split('.')[0]  # 拡張子なしのファイル名を使用

    # ZIPファイルを作成
    with tempfile.TemporaryDirectory('w', delete=True) as tmp_dir:
        ztmp_path = path.join(tmp_dir, 'tmp.zip')

        with zipfile.ZipFile(ztmp_path, 'w') as ztmp_file:
            for item in zin_file.infolist():

                # アイコンを差し替え
                if item.filename == icon_name:
                    ztmp_file.write(IMG_PATH, icon_name)

                # アイコンを差し替え
                elif item.filename == icon_name+'.png':
                    ztmp_file.write(IMG_PATH, icon_name+'.png')

                # instance.cfgを差し替え
                elif item.filename == 'instance.cfg':
                    with zin_file.open(item.filename, 'r') as cfg_file:
                        s = ''
                        for l in cfg_file.readlines():
                            ll = l.decode('utf-8')
                            if ll.startswith('iconKey='):
                                s += f'iconKey={icon_name}\n'
                            else:
                                s += ll
                    ztmp_file.writestr(item, s)
                    print("instance.cfgを更新しました。")

                # それ以外はそのままコピー
                else:
                    file_data = zin_file.read(item.filename)
                    ztmp_file.writestr(item, file_data)

            # アイコンが存在しない場合、新規追加
            if icon_name+'.png' not in ztmp_file.namelist():
                ztmp_file.write(IMG_PATH, icon_name+'.png')
                print("アイコンが存在しなかったため、新規追加しました。")

        # 元ファイルを置き換える
        shutil.move(ztmp_path, ZIN_PATH)

# 完了メッセージ
print("アイコンの差し替えが完了しました。Enterキーを押して終了してください。")
input()
