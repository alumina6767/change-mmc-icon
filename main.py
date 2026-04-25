# MMCやmrpackのアイコンを指定したファイルに変更する

import zipfile
import sys
from os import path
import tkinter.filedialog
import shutil
import tempfile
from mmc import set_mmc_icon
from mrpack import set_mrpack_icon


def get_file_path(file_types, title):
    
    # メッセージ
    print(title+"...")

    # アプリケーションのパスを取得
    if getattr(sys, 'frozen', False):
        application_path = path.dirname(sys.executable)
    elif __file__:
        application_path = path.dirname(__file__)

    file_path = None
    file_path = tkinter.filedialog.askopenfilename(
        filetypes=[("ファイル", ";".join(["*." + ft for ft in file_types]))],
        initialdir=path.abspath(application_path),
        title=title
    )

    # キャンセル時の処理
    if file_path == "":
        print("エラー: ファイルが選択されませんでした。")
        input()
        sys.exit()

    return file_path


def main():
    # ZIPファイルの選択
    archive_path = get_file_path(
        ["zip", "mrpack"], "MMCのZIPファイルもしくは、mrpackを選択してください")

    # 画像ファイルの選択
    icon_path = get_file_path(["png"], "差し替える画像ファイルを選択してください")

    # MMCのZIPファイルだった時
    if archive_path.endswith(".zip"):
        set_mmc_icon(archive_path, icon_path)

    # mrpackのZIPファイルだった時
    elif archive_path.endswith(".mrpack"):
        set_mrpack_icon(archive_path, icon_path)

    # 完了メッセージ
    print("アイコンの差し替えが完了しました。Enterキーを押して終了してください。")
    input()


if __name__ == "__main__":
    main()
