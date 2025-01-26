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
from kivy.graphics import Color, Rectangle, Line
from kivy.utils import get_color_from_hex
from kivy.properties import ListProperty

# Add the path to the font file
resource_add_path('fonts')  # Replace 'fonts' with the correct path to the folder containing the font file

# Register the font
LabelBase.register(name='BoonJot-Italic', fn_regular='BoonJot-Italic.ttf')

class MinimalCheckBox(CheckBox):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(active=self.update_canvas, pos=self.update_canvas, size=self.update_canvas)
        self.update_canvas()

    def update_canvas(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            if self.active:
                Color(0, 1, 0, 1)  # Green when checked
            else:
                Color(0, 0, 0, 1)  # Black when unchecked
            Line(width=1.5, rectangle=(self.x, self.y, self.width, self.height))

class TodoApp(App):
    # Define colors as properties
    white = ListProperty(get_color_from_hex('#FFFFFF'))  # White
    black = ListProperty(get_color_from_hex('#000000'))  # Black
    green = ListProperty(get_color_from_hex('#00FF00'))  # Green
    light_gray = ListProperty(get_color_from_hex('#E0E0E0'))  # Light Gray

    def build(self):
        self.task_list = []
        return TodoLayout()

    def add_task(self, task_text):
        if task_text.strip() == '':
            return
        
        task_box = BoxLayout(size_hint_y=None, height=60, padding=[10, 5], spacing=10)
        task_checkbox = MinimalCheckBox(
            size_hint=(None, None), 
            width=40, 
            height=40
        )
        task_label = Label(
            text=task_text, 
            size_hint=(None, None), 
            width=300, 
            font_name='BoonJot-Italic', 
            color=self.black,  # Black Text
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
            background_color=self.white,  # White
            color=self.black,  # Black Text
            font_name='BoonJot-Italic', 
            font_size=14
        )
        task_button_delete = Button(
            text='Delete', 
            size_hint=(None, None), 
            width=80, 
            height=40, 
            background_color=self.white,  # White
            color=self.black,  # Black Text
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
                task_label.color = self.green  # Green when completed
            else:
                task_label.color = self.black  # Black when incomplete

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
            # White background
            Color(rgba=get_color_from_hex('#FFFFFF'))  # White
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


if __name__ == '__main__':
    TodoApp().run()
