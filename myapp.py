from re import MULTILINE
import kivy
kivy.require('2.0.0')

import numpy as np
import re
import tensorflow as tf
import json


from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.storage.jsonstore import JsonStore
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty, ListProperty
from kivy.clock import Clock
import json
from kivy.storage.dictstore import DictStore
import os

from keras.models import model_from_json, load_model
import tensorflow as tf


from kivymd.uix.dropdownitem import MDDropDownItem
from kivymd.uix.list import OneLineListItem
from kivymd.icon_definitions import md_icons
from kivymd.uix.list import IRightBodyTouch, OneLineAvatarIconListItem
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.metrics import dp
from kivymd.uix.menu import MDDropdownMenu
import threading


def update_answer(value_given1,value_given2,value_given3,value_given4,value_given5,value_given6,eleseven):
    
        if value_given1 is not None and value_given2 is not None and value_given3 is not None and value_given4 is not None and value_given5 is not None and value_given6 is not None:
            
            """
            #Following part is if there is tflite model to load and use for predictions
            #import tflite_runtime.interpreter as tflite
            # Load TFLite model and allocate tensors.
            interpreter = tf.lite.Interpreter(model_path=r'path_to_model.tflite')#allocate the tensors
            allow_custom_ops = True
            interpreter.allocate_tensors()


            #get input and output tensors
            input_details = interpreter.get_input_details()
            output_details = interpreter.get_output_details()


            var1 = ([value_given1]) #element1
            var1 = np.expand_dims(var1, axis=0)
            var2 = ([value_given5]) #element2
            var2 = np.expand_dims(var2, axis=0)
            var3 = ([value_given6]) #element3
            var3 = np.expand_dims(var3, axis=0)
            var4 = ([value_given4]) #element4
            var4 = np.expand_dims(var4, axis=0)
            var5 = ([value_given3]) #element5
            var5 = np.expand_dims(var5, axis=0)
            var6 = ([value_given2]) #element6
            var6 = np.expand_dims(var6, axis=0)
            var7 = ([eleseven]) #element7
            var7 = np.expand_dims(var7, axis=0)
            input_shape = input_details[0]['shape']
            input_data = [1,22,60,25,15,98,'last_item'] 
            interpreter.set_tensor(input_details[0]['index'], np.int64(var1))
            interpreter.set_tensor(input_details[1]['index'], np.float32(var2))
            interpreter.set_tensor(input_details[2]['index'], np.float32(var3))
            interpreter.set_tensor(input_details[3]['index'], np.float32(var4))
            interpreter.set_tensor(input_details[4]['index'], np.float32(var5))
            interpreter.set_tensor(input_details[5]['index'], np.float32(var6))
            interpreter.set_tensor(input_details[6]['index'], var7)
            interpreter.invoke()

            output_data = interpreter.get_tensor(output_details[0]['index'])
           """
            output_data = 0.6597
            return ("{0:.2f} % probability for outcome".format( 
            100*float(output_data)))
        #else:
            #return ("Values not given")

class ScreenManager(ScreenManager):
    pass

class LoginScreen(Screen):
    def clear(self):
        self.ids.welcome_label.text = "WELCOME"
        self.ids.user.text = ""
        self.ids.password.text= ""

    def logger(self):
        self.ids.welcome_label.text = f'Bonjour {self.ids.user.text} :)'

    def switch_to_main(self, *args):
        app = App.get_running_app()
        app.root.current = "screen_one"

    def clocked_switch(self):
        Clock.schedule_once(self.switch_to_main, 2)


class ScreenOne(Screen):
    enabled = BooleanProperty(True)
    data_storage = ObjectProperty(None)
    def __init__(self,*args,**kwargs):
        super(Screen,self).__init__(*args,**kwargs)
        self.data_storage = JsonStore('data.json')

class ScreenTwo(Screen):
    enabled = BooleanProperty(True)
    def __init__(self,*args,**kwargs):
        super(Screen,self).__init__(*args,**kwargs)

    def on_enter(self):
        items_list = ['item1','item2','item3','item4','item5','item6']
        for i in items_list:
            self.ids.elementseven.add_widget(
                OneLineListItem(text=f"{i}", on_press=lambda x, item=i:self.data_storage_update(item))
            )
    
    def data_storage_update(self,item):
        a_file = open("data.json","r")
        json_object = json.load(a_file)
        a_file.close()
        json_object["mydata"]["elementseven"] = item
        a_file = open("data.json","w")
        json.dump(json_object,a_file)
        a_file.close()

class ScreenThree(Screen):
    enabled = BooleanProperty(True)
    global answer

    def start_background_task(self):
        threading.Thread(target=self.callFunction).start()

    def callFunction(self, *args):
        f = open("data.json")
        data = json.load(f)
        value_list = []

        for key in data["mydata"]:
            value_list.append(data["mydata"][key])
        result = update_answer(*value_list)

        if result != None:
            self.stopfunction(result)

    def stopfunction(self,result):
        self.ids.welcome_label.text = result
        self.ids.spinner.active = False
    
    def __init__(self,*args,**kwargs):
        super(Screen,self).__init__(*args,**kwargs)
        self.data_storage = JsonStore('data.json')
            
class ScreenFour(Screen):
    pass

class MyApp(MDApp):
    def __init__(self,**kwargs):    
        self.title = "Test App"
        super().__init__(**kwargs)

    def restart(self):
        self.root.clear_widgets()
        self.stop()
        return MyApp().run()
    #No need for next part as Kivy will load myapp.kv automatically
    #def build(self):
    #    return Builder.load_file('myapp.kv')
    

if __name__ == '__main__':
    MyApp().run()
