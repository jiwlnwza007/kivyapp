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

# เพิ่มฟอนต์ภาษาไทย
#resource_add_path('path_to_font_folder')  # กำหนด path ที่เก็บฟอนต์
LabelBase.register(name='Sarabun', fn_regular='THSarabun.ttf')

class TodoApp(App):
    def build(self):
        self.task_list = []
        return TodoLayout()

    def add_task(self, task_text):
        # เพิ่มงานใหม่ลงใน task_layout
        if task_text.strip() == '':  # ตรวจสอบว่าไม่ใช่ข้อความว่าง
            return
        
        task_box = BoxLayout(size_hint_y=None, height=40)
        task_checkbox = CheckBox(size_hint=(None, None), width=40, height=40)
        task_label = Label(text=task_text, size_hint=(None, None), width=300, font_name='Sarabun')
        task_button_edit = Button(text='Edit', size_hint=(None, None), width=60)
        task_button_delete = Button(text='Delete', size_hint=(None, None), width=60)
        
        # ปุ่ม Edit และ Delete
        task_button_edit.bind(on_press=self.edit_task)
        task_button_delete.bind(on_press=self.delete_task)
        
        # เพิ่ม widget ไปที่ task_box
        task_box.add_widget(task_checkbox)
        task_box.add_widget(task_label)
        task_box.add_widget(task_button_edit)
        task_box.add_widget(task_button_delete)
        
        # เพิ่ม task_box ไปที่ task_layout
        self.root.ids.task_layout.add_widget(task_box)
        
        # reset text input
        self.root.ids.task_input.text = ''
        self.task_list.append(task_text)

    def delete_task(self, instance):
        task_box = instance.parent

        # ค้นหา Label ที่เก็บข้อความของงาน
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
        
        # ค้นหา Label ที่เก็บข้อความของงาน
        task_label = None
        for widget in task_box.children:
            if isinstance(widget, Label):
                task_label = widget
                break

        if task_label:
            task_text = task_label.text
            self.root.ids.task_input.text = task_text  # นำข้อความไปใส่ text input

            # ลบ task ออกจาก layout และ list
            if task_text in self.task_list:
                self.task_list.remove(task_text)
            self.root.ids.task_layout.remove_widget(task_box)
        else:
            print("Warning: Task label not found")

    def clear_tasks(self, instance):
        self.root.ids.task_layout.clear_widgets()
        self.task_list.clear()


class TodoLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'


if __name__ == '__main__':
    TodoApp().run()
