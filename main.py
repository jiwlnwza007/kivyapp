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

# เพิ่ม path ไปยังไฟล์ฟอนต์
resource_add_path('fonts')  # เปลี่ยน 'fonts' ให้เป็น path ที่ถูกต้อง

# ลงทะเบียนฟอนต์ที่ต้องการใช้
LabelBase.register(name='BoonJot-Italic', fn_regular='BoonJot-Italic.ttf')

# สร้างคลาส MinimalCheckBox ซึ่งจะปรับเปลี่ยนสีเมื่อเลือกหรือไม่เลือก
class MinimalCheckBox(CheckBox):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(active=self.update_canvas, pos=self.update_canvas, size=self.update_canvas)
        self.update_canvas()

    def update_canvas(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            if self.active:
                Color(0, 1, 0, 1)  # สีเขียวเมื่อถูกเลือก
            else:
                Color(0, 0, 0, 1)  # สีดำเมื่อไม่ถูกเลือก
            Line(width=1.5, rectangle=(self.x, self.y, self.width, self.height))

# คลาส TodoApp สำหรับสร้างแอพ ToDo list
class TodoApp(App):
    # กำหนดสีที่ใช้ในแอพ
    white = ListProperty(get_color_from_hex('#FFFFFF'))  # สีขาว
    black = ListProperty(get_color_from_hex('#000000'))  # สีดำ
    green = ListProperty(get_color_from_hex('#00FF00'))  # สีเขียว
    light_gray = ListProperty(get_color_from_hex('#E0E0E0'))  # สีเทาอ่อน

    def build(self):
        self.task_list = []  # รายการงานที่ต้องทำ
        return TodoLayout()

    # ฟังก์ชั่นเพิ่มงานลงในรายการ
    def add_task(self, task_text):
        if task_text.strip() == '':  # ถ้าข้อความเป็นค่าว่างจะไม่เพิ่มงาน
            return
        
        # สร้างกล่องแสดงงานใหม่
        task_box = BoxLayout(size_hint_y=None, height=60, padding=[10, 5], spacing=10)
        
        # สร้าง CheckBox สำหรับงานนั้นๆ
        task_checkbox = MinimalCheckBox(
            size_hint=(None, None), 
            width=40, 
            height=40,
            pos_hint={'center_y': 0.5}  
        )
        
        # สร้าง Label แสดงข้อความของงาน
        task_label = Label(
            text=task_text, 
            size_hint=(None, None), 
            width=300, 
            font_name='BoonJot-Italic', 
            color=self.black,  # สีข้อความเป็นสีดำ
            halign='left', 
            valign='middle',
            text_size=(300, None),
            font_size=16,
            pos_hint={'center_y': 0.5}  
        )
        
        # สร้างปุ่ม Edit และ Delete
        task_button_edit = Button(
            text='Edit', 
            size_hint=(None, None), 
            width=80, 
            height=40, 
            background_color=self.white, 
            color=self.black,  
            font_name='BoonJot-Italic',  
            font_size=14,
            pos_hint={'center_y': 0.5} 
        )
        task_button_delete = Button(
            text='Delete', 
            size_hint=(None, None), 
            width=80, 
            height=40, 
            background_color=self.white, 
            color=self.black,  
            font_name='BoonJot-Italic',  
            font_size=14,
            pos_hint={'center_y': 0.5}  
        )
        
        # เชื่อมต่อการคลิกปุ่ม Edit และ Delete กับฟังก์ชันที่ต้องการ
        task_button_edit.bind(on_press=self.edit_task)
        task_button_delete.bind(on_press=self.delete_task)
        
        # เชื่อมต่อการคลิก Checkbox กับฟังก์ชันที่เปลี่ยนสีข้อความ
        task_checkbox.bind(active=self.mark_task_completed)
        
        # เพิ่ม widget ทั้งหมดเข้าใน task_box
        task_box.add_widget(task_checkbox)
        task_box.add_widget(task_label)
        task_box.add_widget(task_button_edit)
        task_box.add_widget(task_button_delete)
        
        # เพิ่ม task_box เข้าไปใน layout
        self.root.ids.task_layout.add_widget(task_box)
        self.root.ids.task_input.text = ''  # เคลียร์ข้อความในช่องกรอก
        self.task_list.append(task_text)  # เพิ่มงานใหม่ลงในรายการ

    # ฟังก์ชั่นลบงาน
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

    # ฟังก์ชั่นแก้ไขงาน
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

    # ฟังก์ชั่นที่เปลี่ยนสีข้อความเมื่อทำเครื่องหมายเสร็จแล้ว
    def mark_task_completed(self, instance, value):
        task_box = instance.parent
        task_label = None
        for widget in task_box.children:
            if isinstance(widget, Label):
                task_label = widget
                break

        if task_label:
            if value:
                task_label.color = self.green  # เปลี่ยนเป็นสีเขียวเมื่อเสร็จ
            else:
                task_label.color = self.black  # เปลี่ยนกลับเป็นสีดำเมื่อยังไม่เสร็จ

    # ฟังก์ชั่นล้างงานทั้งหมด
    def clear_tasks(self, instance):
        self.root.ids.task_layout.clear_widgets()
        self.task_list.clear()

    # ฟังก์ชั่นสำหรับการจัดเรียงงาน
    def sort_tasks(self, instance, text):
        if text == "ชื่อ":
            self.task_list.sort()
        elif text == "วันที่":
            # ใส่ logic การเรียงงานตามวันที่
            pass
        self.root.ids.task_layout.clear_widgets()
        for task in self.task_list:
            self.add_task(task)

    # ฟังก์ชั่นเปิด/ปิดการแจ้งเตือน
    def toggle_notifications(self, instance, value):
        if value:
            print("Notifications enabled")
        else:
            print("Notifications disabled")


# สร้างเลย์เอาท์ของแอพ
class TodoLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'  # ตั้งค่า layout ให้เป็นแนวตั้ง
        with self.canvas.before:
            # ตั้งค่า background เป็นสีขาว
            Color(rgba=get_color_from_hex('#FFFFFF'))  
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


if __name__ == '__main__':
    TodoApp().run()
