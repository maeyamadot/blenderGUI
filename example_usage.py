"""
blender_gui.py の使用例。

Blender のテキストエディタにこのファイルを開いて「実行」するか、
Python コンソールに貼り付けて実行してください。
このファイルと blender_gui.py は同じディレクトリに置くか、
sys.path に blender_gui.py のあるパスを追加してください。
"""

import sys
import os

# blender_gui.py が置かれているディレクトリを import パスに追加する例
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.append(SCRIPT_DIR)

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
