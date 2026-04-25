import zipfile
from os import path
import shutil
import tempfile


def set_mrpack_icon(mrpack_path:str, in_icon_path:str):

    # ZIPファイル内のアイコンを差し替え
    with zipfile.ZipFile(mrpack_path, 'r') as zin_file:

        print(f"アイコンを{in_icon_path}に差し替えます...")

        icon_path = "overrides/icon.png"

        # ZIPファイルを作成
        with tempfile.TemporaryDirectory('w', delete=True) as tmp_dir:
            ztmp_path = path.join(tmp_dir, 'tmp.zip')

            with zipfile.ZipFile(ztmp_path, 'w') as ztmp_file:
                for item in zin_file.infolist():

                    # アイコンを差し替え
                    if item.filename == icon_path:
                        ztmp_file.write(in_icon_path, icon_path)

                    # それ以外はそのままコピー
                    else:
                        file_data = zin_file.read(item.filename)
                        ztmp_file.writestr(item, file_data)

                # アイコンが存在しない場合、新規追加
                if icon_path not in ztmp_file.namelist():
                    ztmp_file.write(in_icon_path, icon_path)
                    print("アイコンが存在しなかったため、新規追加しました。")

            # 元ファイルを置き換える
            shutil.move(ztmp_path, mrpack_path)
