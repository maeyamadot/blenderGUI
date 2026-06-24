"""
blender_gui.py の使用例。

【重要】Blender のテキストエディタで「実行」する場合、その Python コードは
.blend ファイル内のテキストデータブロックとして実行されるため、
__file__ が存在せず、自動でディレクトリを検出できません。
そのため、下の BLENDER_GUI_DIR に blender_gui.py が置かれている
"実際のフォルダパス" を直接書いてください。

例:
    BLENDER_GUI_DIR = r"E:\projects\experiments\blenderGUI"

このパスの中に blender_gui.py が存在している必要があります。
（このリポジトリを clone/ダウンロードしたフォルダを指定すればOK）
"""

import sys

# ↓↓↓ ここを blender_gui.py が置かれている実際のフォルダパスに書き換える ↓↓↓
BLENDER_GUI_DIR = r"E:\projects\experiments\blenderGUI"

if BLENDER_GUI_DIR not in sys.path:
    sys.path.append(BLENDER_GUI_DIR)

import blender_gui as bgui

# 念のため一度アンレジスターしてから登録する（再実行に強くするため）
try:
    bgui.unregister()
except Exception:
    pass
bgui.register()


def on_hello_click():
    print("Hello ボタンが押されました")


def on_remove_click():
    # remove_button 自身が呼ばれた後、このボタンも消す
    bgui.remove_button(remove_btn)
    print("Remove ボタンを削除しました")


# ボタンを2つ追加する
hello_btn = bgui.add_button(
    "Hello",
    x=50, y=50,
    on_click=on_hello_click,
)

remove_btn = bgui.add_button(
    "Remove me",
    x=50, y=100,
    on_click=on_remove_click,
    color=(0.5, 0.1, 0.1, 0.8),
    hover_color=(0.7, 0.2, 0.2, 0.9),
)

print("ボタンを追加しました。3D Viewport 上で確認してください。")
print("GUI を完全に終了するには bgui.unregister() を実行してください。")
