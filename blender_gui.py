"""
Blender の gpu モジュールを使った最小限の GUI ライブラリ。

- Button ウィジェットを 3D Viewport 上に描画する
- ボタンはあとから自由に追加・削除できる
- クリック判定はモーダルオペレーター経由のマウス座標で行う

使い方 (Blender の Python コンソール / テキストエディタで実行):

    import blender_gui as bgui
    bgui.register()

    btn = bgui.add_button("Hello", 50, 50, on_click=lambda: print("clicked!"))
    # ボタンを消す
    bgui.remove_button(btn)

    bgui.unregister()
"""

import bpy
import gpu
from gpu_extras.batch import batch_for_shader


class Button:
    """1個のクリック可能なボタン。座標は Viewport 左下原点のピクセル座標。"""

    def __init__(self, label, x, y, width=120, height=30,
                 on_click=None,
                 color=(0.2, 0.2, 0.2, 0.8),
                 hover_color=(0.35, 0.35, 0.35, 0.9),
                 text_color=(1.0, 1.0, 1.0, 1.0)):
        self.label = label
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.on_click = on_click
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.is_hovered = False

    def contains(self, mx, my):
        return (self.x <= mx <= self.x + self.width and
                self.y <= my <= self.y + self.height)

    def draw(self):
        shader = gpu.shader.from_builtin('UNIFORM_COLOR')
        verts = (
            (self.x, self.y),
            (self.x + self.width, self.y),
            (self.x + self.width, self.y + self.height),
            (self.x, self.y + self.height),
        )
        indices = ((0, 1, 2), (2, 3, 0))
        batch = batch_for_shader(shader, 'TRIS', {"pos": verts}, indices=indices)

        color = self.hover_color if self.is_hovered else self.color
        gpu.state.blend_set('ALPHA')
        shader.bind()
        shader.uniform_float("color", color)
        batch.draw(shader)
        gpu.state.blend_set('NONE')

        blf_draw_label(self.label, self.x, self.y, self.width, self.height, self.text_color)


def blf_draw_label(text, x, y, width, height, color):
    import blf
    font_id = 0
    blf.size(font_id, 14.0)
    text_width, text_height = blf.dimensions(font_id, text)
    blf.position(font_id, x + (width - text_width) / 2, y + (height - text_height) / 2, 0)
    blf.color(font_id, *color)
    blf.draw(font_id, text)


_widgets = []
_draw_handler = None


def add_button(label, x, y, width=120, height=30, on_click=None, **kwargs):
    """ボタンを生成して GUI に追加し、Button インスタンスを返す。"""
    btn = Button(label, x, y, width=width, height=height, on_click=on_click, **kwargs)
    _widgets.append(btn)
    _tag_redraw()
    return btn


def remove_button(btn):
    """指定したボタンを GUI から取り除く。"""
    if btn in _widgets:
        _widgets.remove(btn)
        _tag_redraw()


def clear_buttons():
    """すべてのボタンを取り除く。"""
    _widgets.clear()
    _tag_redraw()


def _tag_redraw():
    for area in bpy.context.window_manager.windows[0].screen.areas:
        area.tag_redraw()


def _draw_callback():
    for widget in _widgets:
        widget.draw()


class GUI_OT_modal(bpy.types.Operator):
    """マウス入力をボタンに渡すモーダルオペレーター。"""
    bl_idname = "gui.modal_input"
    bl_label = "Blender GUI Modal Input"

    _running = False

    def modal(self, context, event):
        if not GUI_OT_modal._running:
            return {'FINISHED'}

        if event.type == 'MOUSEMOVE':
            mx, my = event.mouse_region_x, event.mouse_region_y
            redraw = False
            for widget in _widgets:
                hovered = widget.contains(mx, my)
                if hovered != widget.is_hovered:
                    widget.is_hovered = hovered
                    redraw = True
            if redraw:
                context.area.tag_redraw()

        elif event.type == 'LEFTMOUSE' and event.value == 'PRESS':
            mx, my = event.mouse_region_x, event.mouse_region_y
            for widget in _widgets:
                if widget.contains(mx, my) and widget.on_click:
                    widget.on_click()
                    return {'RUNNING_MODAL'}

        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        GUI_OT_modal._running = True
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}


def register():
    global _draw_handler
    bpy.utils.register_class(GUI_OT_modal)
    _draw_handler = bpy.types.SpaceView3D.draw_handler_add(
        _draw_callback, (), 'WINDOW', 'POST_PIXEL')
    bpy.ops.gui.modal_input('INVOKE_DEFAULT')


def unregister():
    global _draw_handler
    GUI_OT_modal._running = False
    if _draw_handler is not None:
        bpy.types.SpaceView3D.draw_handler_remove(_draw_handler, 'WINDOW')
        _draw_handler = None
    clear_buttons()
    bpy.utils.unregister_class(GUI_OT_modal)
