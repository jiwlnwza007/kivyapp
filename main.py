from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.checkbox import CheckBox
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.switch import Switch
from kivy.uix.spinner import Spinner
from kivy.core.text import LabelBase
from kivy.resources import resource_add_path
from kivy.graphics import Color, Rectangle
from kivy.utils import get_color_from_hex
from kivy.properties import ListProperty

# Add the path to the font file
resource_add_path('fonts')  # Replace 'fonts' with the correct path to the folder containing the font file

# Register the font
LabelBase.register(name='BoonJot-Italic', fn_regular='BoonJot-Italic.ttf')

class CustomCheckBox(CheckBox):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(active=self.update_color)
        self.update_color()

    def update_color(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            if self.active:
                Color(0, 1, 0, 1)  # สีเขียวเมื่อถูกเลือก
            else:
                Color(1, 0, 0, 1)  # สีแดงเมื่อไม่ถูกเลือก
            Rectangle(pos=self.pos, size=self.size)

class TodoApp(App):
    # Define colors as properties
    pastel_pink = ListProperty(get_color_from_hex('#FFD1DC'))  # Pastel Pink
    pastel_blue = ListProperty(get_color_from_hex('#A2DDF0'))  # Pastel Blue
    pastel_green = ListProperty(get_color_from_hex('#B2F2BB'))  # Pastel Green
    pastel_gray = ListProperty(get_color_from_hex('#E0E0E0'))  # Pastel Gray
    dark_text = ListProperty(get_color_from_hex('#333333'))  # Dark Text

    def build(self):
        self.task_list = []
        return TodoLayout()

    def add_task(self, task_text):
        if task_text.strip() == '':
            return
        
        task_box = BoxLayout(size_hint_y=None, height=60, padding=[10, 5], spacing=10)
        task_checkbox = CustomCheckBox(
            size_hint=(None, None), 
            width=40, 
            height=40
        )
        task_label = Label(
            text=task_text, 
            size_hint=(None, None), 
            width=300, 
            font_name='BoonJot-Italic', 
            color=self.dark_text,  # Dark Text
            halign='left', 
            valign='middle',
            text_size=(300, None),
            font_size=16
        )
        task_button_edit = Button(
            text='Edit', 
            size_hint=(None, None), 
            width=80, 
            height=40, 
            background_color=self.pastel_blue,  # Pastel Blue
            color=self.dark_text,  # Dark Text
            font_name='BoonJot-Italic', 
            font_size=14
        )
        task_button_delete = Button(
            text='Delete', 
            size_hint=(None, None), 
            width=80, 
            height=40, 
            background_color=self.pastel_pink,  # Pastel Pink
            color=self.dark_text,  # Dark Text
            font_name='BoonJot-Italic',  
            font_size=14
        )
        
        task_button_edit.bind(on_press=self.edit_task)
        task_button_delete.bind(on_press=self.delete_task)
        task_checkbox.bind(active=self.mark_task_completed)
        
        task_box.add_widget(task_checkbox)
        task_box.add_widget(task_label)
        task_box.add_widget(task_button_edit)
        task_box.add_widget(task_button_delete)
        
        self.root.ids.task_layout.add_widget(task_box)
        self.root.ids.task_input.text = ''
        self.task_list.append(task_text)

    def delete_task(self, instance):
        task_box = instance.parent
        task_label = None
        for widget in task_box.children:
            if isinstance(widget, Label):
                task_label = widget
                break

        if task_label:
            task_text = task_label.text
            if task_text in self.task_list:
                self.task_list.remove(task_text)
            self.root.ids.task_layout.remove_widget(task_box)
        else:
            print("Warning: Task label not found")

    def edit_task(self, instance):
        task_box = instance.parent
        task_label = None
        for widget in task_box.children:
            if isinstance(widget, Label):
                task_label = widget
                break

        if task_label:
            task_text = task_label.text
            self.root.ids.task_input.text = task_text
            if task_text in self.task_list:
                self.task_list.remove(task_text)
            self.root.ids.task_layout.remove_widget(task_box)
        else:
            print("Warning: Task label not found")

    def mark_task_completed(self, instance, value):
        task_box = instance.parent
        task_label = None
        for widget in task_box.children:
            if isinstance(widget, Label):
                task_label = widget
                break

        if task_label:
            if value:
                task_label.color = self.pastel_green  # สีเขียวเมื่อเสร็จสิ้น
            else:
                task_label.color = self.dark_text  # สีเดิมเมื่อไม่เสร็จสิ้น

    def clear_tasks(self, instance):
        self.root.ids.task_layout.clear_widgets()
        self.task_list.clear()

    def sort_tasks(self, instance, text):
        if text == "ชื่อ":
            self.task_list.sort()
        elif text == "วันที่":
            # Implement date sorting logic here
            pass
        self.root.ids.task_layout.clear_widgets()
        for task in self.task_list:
            self.add_task(task)

    def toggle_notifications(self, instance, value):
        if value:
            print("Notifications enabled")
        else:
            print("Notifications disabled")


class TodoLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        with self.canvas.before:
            # Pastel Pink background
            Color(rgba=get_color_from_hex('#FFD1DC'))  # Pastel Pink
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


if __name__ == '__main__':
    TodoApp().run()
