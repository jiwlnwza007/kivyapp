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

# เพิ่มฟอนต์ภาษาไทย
#resource_add_path('path_to_font_folder')  # กำหนด path ที่เก็บฟอนต์
LabelBase.register(name='Sarabun', fn_regular='THSarabun.ttf')

class TodoApp(App):
    def build(self):
        self.task_list = []
        return TodoLayout()

    def add_task(self, task_text):
        if task_text.strip() == '':
            return
        
        task_box = BoxLayout(size_hint_y=None, height=50, padding=[10, 5], spacing=10)
        task_checkbox = CheckBox(size_hint=(None, None), width=30, height=30, color=[0.64, 0.40, 0.67, 1])  # Purple
        task_label = Label(text=task_text, size_hint=(None, None), width=300, font_name='Sarabun', color=[0.29, 0.13, 0.25, 1])  # Dark purple
        task_button_edit = Button(text='Edit', size_hint=(None, None), width=60, background_color=[0.64, 0.40, 0.67, 1], color=[1, 1, 1, 1])  # Purple
        task_button_delete = Button(text='Delete', size_hint=(None, None), width=60, background_color=[0.64, 0.40, 0.67, 1], color=[1, 1, 1, 1])  # Purple
        
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
                task_label.color = [0.64, 0.40, 0.67, 1]  # Purple for completed tasks
            else:
                task_label.color = [0.29, 0.13, 0.25, 1]  # Dark purple for incomplete tasks

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
            Color(0.97, 0.91, 0.93, 1)  # Light pink background
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


if __name__ == '__main__':
    TodoApp().run()
