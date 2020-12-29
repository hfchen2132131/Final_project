from transitions.extensions import GraphMachine

from utils import send_text_message
from utils import send_image_message, push_text_message
import requests as rqs
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options



class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)
        

    def is_going_to_state1(self, event):
        text = event.message.text
        
        return text.lower() == "1"

    def is_going_to_state2(self, event):
        text = event.message.text
        return text.lower() == "2"
    
    def is_going_to_state3(self, event):
        text = event.message.text
        return text.lower() == "3"

    def is_going_to_help(self, event):
        text = event.message.text
        print(text.lower())
        return text.lower() == "help"

    def is_going_to_graph(self, event):
        text = event.message.text
        self.user = event.source.user_id
        print(text.lower())
        return text.lower() == "4"

    def on_enter_user(self, event=None):
        print("Enter user")
        
        push_text_message(self.user, "請選擇輸入模式：\n\t1 bin hex dec\n\t2 重量單位換算\n\t3 長度單位換算\n\t4 graph")

    def on_enter_graph(self, event):
        print("I'm entering graph")

        reply_token = event.reply_token
        
        
        send_image_message(reply_token, "")
        self.go_back()

    def on_enter_state1(self, event):
        print("I'm entering state1")

        reply_token = event.reply_token
        
        
        send_text_message(reply_token, "請依格式輸入\n\t被轉換的進制 數字\n\t例：bin 01001")
        
        #self.go_back()

    def on_exit_state1(self, event):
        print("Leaving state1")
        

    def on_enter_state3(self, event):
        print("I'm entering state2")

        reply_token = event.reply_token
        send_text_message(reply_token, "單位有：公分 公尺 英吋 英呎\n請依格式輸入：單位 數字")
        #self.go_back()

    def on_exit_state2(self, event):
        print("Leaving state2")


    def on_enter_state2(self, event):
        print("I'm entering state3")

        reply_token = event.reply_token
        send_text_message(reply_token, "單位有：公克 公斤 盎司 兩 台斤 磅\n請依格式輸入：單位 數字")
        #self.go_back()

    def on_exit_state3(self, event):
        print("Leaving state3")

    def on_enter_help(self, event):
        print("I'm entering help")

        reply_token = event.reply_token
        send_text_message(reply_token, "請選擇輸入模式：\n\t1 bin hex dec\n\t2 重量單位換算\n\t3 長度單位換算\n\t4 graph")
        self.go_back()

    def on_exit_help(self):
        print("Leaving state help")
    
    def check_state1(self, event):
        text = event.message.text
        text = text.lower()
        reply_token = event.reply_token
        to = event.source.user_id
        tp = text.split()
        if tp[0] == "bin":
            try:
                n = int(tp[1],2)
            except:
                return False
        elif tp[0] == "hex":
            try:
                n = int(tp[1],16)
            except:
                return False
        elif tp[0] == "dec":
            try:
                n = int(tp[1])
            except:
                return False
        else:
            return False

        
        send_text_message(reply_token, "bin:"+bin(n)+"\nhex:"+hex(n)+"\ndec:"+str(n))
            
        
        self.user = to        
        return True
    def check_state2(self, event):
        text = event.message.text
        text = text.lower()
        reply_token = event.reply_token
        to = event.source.user_id
        tp = text.split()
        print("jj")
        if tp[0] == "公克":
            try:
                n = int(tp[1])
                n = n / 1000
            except:
                return False
        elif tp[0] == "公斤":
            try:
                n = int(tp[1])
            except:
                return False
        elif tp[0] == "盎司":
            try:
                n = int(tp[1])
                n *= 0.0283495231
            except:
                return False
        elif tp[0] == "兩":
            try:
                n = int(tp[1])
                n = 0.6 * n / 16
            except:
                return False
        elif tp[0] == "台斤":
            try:
                n = int(tp[1])
                n = 0.6 * n
            except:
                return False
        elif tp[0] == "磅":
            try:
                n = int(tp[1])
                n = 0.45359237 * n
            except:
                return False
        else:
            return False

        s = "公克："+str(n*1000)+"\n公斤："+str(n)+"\n盎司："+str(n*35.2739619)+"\n兩："+str(n*1.666666666666667*16)+"\n台斤："+str(n*1.666666666666667)+"\n磅："+str(n*2.20462262)
        print(s)
        send_text_message(reply_token,s)
        self.user = to   
        return True

    def check_state3(self, event):
        text = event.message.text
        text = text.lower()
        reply_token = event.reply_token
        to = event.source.user_id
        tp = text.split()
        if tp[0] == "公分":
            try:
                n = int(tp[1])
                n = n / 100
            except:
                return False
        elif tp[0] == "公尺":
            try:
                n = int(tp[1])
            except:
                return False
        elif tp[0] == "英吋":
            try:
                n = int(tp[1])
                n *= 0.0254
            except:
                return False
        elif tp[0] == "英呎":
            try:
                n = int(tp[1])
                n = 0.3048 * n
            except:
                return False
        else:
            return False

        s = "公分："+str(n*100)+"\n公尺："+str(n)+"\n英吋："+str(n*39.37)+"\n英呎："+str(n*3.2808 )
        print(s)
        send_text_message(reply_token,s)
        self.user = to   
        return True