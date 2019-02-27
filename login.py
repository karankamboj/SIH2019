from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager,Screen,WipeTransition
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.accordion import Accordion, AccordionItem
from kivy.uix.dropdown import DropDown
from operator import itemgetter
import sqlite3

conn=sqlite3.connect("db.db")
c=conn.cursor()

AllLands=list(c.execute("Select * from land"))

class ConnectingSigninRegister(ScreenManager):
    pass
class CustomDropDown(Screen,BoxLayout):
    pass
class HomePage(BoxLayout,Screen):
    cur=-1;
    def showland(self):
        global AllLands
        self.cur=-1
        self.ids.acc.clear_widgets()

        if(len(AllLands)<4):
            self.cur=len(AllLands)-1
            for i in range(len(AllLands)):
                txt=str("")
                txt+="[b][color=87ceeb]"
                txt+=str(AllLands[i][0]+"\n "+AllLands[i][1]+"\n"+AllLands[i][2]+"\n"+AllLands[i][3])
                txt+='[/color][/b]'
                item = AccordionItem(title='Land %d' % (i+1),orientation='vertical')
                item.add_widget(Button(text=txt,markup=True))
                item.add_widget(Button(text="Bookmark",size_hint_x=0.2))

                self.ids.acc.add_widget(item)

        else:
            for i in range(4):
                txt=str("")
                txt+="[b][color=87ceeb]"
                txt+=str(AllLands[i][0]+"\n "+AllLands[i][1]+"\n"+AllLands[i][2]+"\n"+AllLands[i][3])
                txt+='[/color][/b]'
                item = AccordionItem(title='Land %d' % (i+1),orientation='vertical')
                item.add_widget(Button(text=txt,markup=True))
                item.add_widget(Button(text="Bookmark",size_hint_x=0.2))
                self.ids.acc.add_widget(item)
            self.cur+=4



    def nextland(self):
        global AllLands
        if(len(AllLands)==self.cur+1):
            popup = Popup(title='Error!',content=Label(text='No More Lands!!'),size_hint=(None, None), size=(200, 200))
            popup.open()
            return
        else:
            self.ids.acc.clear_widgets()
            if(len(AllLands)-1-self.cur>=4):
                for i in range(self.cur+1,self.cur+5):
                    txt=str("")
                    txt+="[b][color=87ceeb]"
                    txt+=str(AllLands[i][0]+"\n "+AllLands[i][1]+"\n"+AllLands[i][2]+"\n"+AllLands[i][3])
                    txt+='[/color][/b]'
                    item = AccordionItem(title='Land %d' % (i+1),orientation='vertical')
                    item.add_widget(Button(text=txt,markup=True))
                    item.add_widget(Button(text="Bookmark",size_hint_x=0.2))
                    self.ids.acc.add_widget(item)
                self.cur+=4
            else:
                for i in range(self.cur+1,len(AllLands)):
                    txt=str("")
                    txt+="[b][color=87ceeb]"
                    txt+=str(AllLands[i][0]+"\n "+AllLands[i][1]+"\n"+AllLands[i][2]+"\n"+AllLands[i][3])
                    txt+='[/color][/b]'
                    item = AccordionItem(title='Land %d' % (i+1),orientation='vertical')
                    item.add_widget(Button(text=txt,markup=True))
                    item.add_widget(Button(text="Bookmark",size_hint_x=0.2))
                    self.ids.acc.add_widget(item)
                self.cur=len(AllLands)-1



    def prevland(self):
        global AllLands
        if(self.cur<=3):
            popup = Popup(title='Error!',content=Label(text='No More Lands!!'),size_hint=(None, None), size=(200, 200))
            popup.open()
            return
        elif(self.cur>=3):
            self.cur-=4
            self.ids.acc.clear_widgets()
            for i in range(self.cur,self.cur+4):
                txt=str("")
                txt+="[b][color=87ceeb]"
                txt+=str(AllLands[i][0]+"\n "+AllLands[i][1]+"\n"+AllLands[i][2]+"\n"+AllLands[i][3])
                txt+='[/color][/b]'
                item = AccordionItem(title='Land %d' % (i+1),orientation='vertical')
                item.add_widget(Button(text=txt,markup=True))
                item.add_widget(Button(text="Bookmark",size_hint_x=0.2))
                self.ids.acc.add_widget(item)
        else:
            self.cur=0
            self.ids.acc.clear_widgets()
            for i in range(self.cur,self.cur+4):
                txt=str("")
                txt+="[b][color=87ceeb]"
                txt+=str(AllLands[i][0]+"\n "+AllLands[i][1]+"\n"+AllLands[i][2]+"\n"+AllLands[i][3])
                txt+='[/color][/b]'
                item = AccordionItem(title='Land %d' % (i+1),orientation='vertical')
                item.add_widget(Button(text=txt,markup=True))
                item.add_widget(Button(text="Bookmark",size_hint_x=0.2))
                self.ids.acc.add_widget(item)
            self.cur=3

    def gotofilter(self):
        self.ids.acc.clear_widgets()
        self.manager.current="filterpage"

    def clearbutton(self):
        global AllLands
        AllLands=list(c.execute("select * from land"))
        self.ids.acc.clear_widgets()


    def sort1(self):
        global AllLands
        self.ids.dropdown.select('Price')
        AllLands=list(c.execute("Select * from land order by Price asc"))


    def sort2(self):
        global AllLands
        self.ids.dropdown.select('Area')
        AllLands=list(c.execute("Select * from land order by Area asc"))


    def logout(self):
        self.ids.acc.clear_widgets()
        self.manager.current="login"
        self.cur=-1

    def closebutton(self):
        conn.commit()
        App.get_running_app().stop()




class FilterPage(BoxLayout,Screen):
    def filtersearchbutton(self):
        global AllLands
        price=int(self.ids.slider_id.value)-1+48 #48 is added due to ascii value of 0
        area=str(self.ids.area_filter.text)
        address="%"+str(self.ids.address_filter.text)+"%"
        AllLands=list(c.execute(''' SELECT * FROM land where Address like ? and Price<=? and Area=? ''',(address,price,area)))
        if(len(AllLands)==0):
            AllLands=list(c.execute(''' SELECT * FROM land '''))
            popup = Popup(title='Oops!',content=Label(text='No Such Lands!'),size_hint=(None, None), size=(200, 200))
            popup.open()
        else:
            self.ids.area_filter.text=""
            self.ids.address_filter.text=""
            self.ids.slider_id.value=1
            popup = Popup(title='Oops!',content=Label(text='Lands are filtered!! \n Click on show lands!!'),size_hint=(None, None), size=(200, 200))
            popup.open()
            AllLands=list(c.execute(''' SELECT * FROM land where Address like ? and Price<=? and Area=? ''',(address,price,area)))
            self.manager.current="homepage"



    def showland(self):
        self.manager.current="homepage"

    def nextland(self):
        popup = Popup(title='Oops!',content=Label(text='Go to main page first!'),size_hint=(None, None), size=(200, 200))
        popup.open()

    def prevland(self):
        popup = Popup(title='Oops!',content=Label(text='Go to main page first!'),size_hint=(None, None), size=(200, 200))
        popup.open()

    def gotofilter(self):
        popup = Popup(title='Oops!',content=Label(text='Already on Filter!'),size_hint=(None, None), size=(200, 200))
        popup.open()

    def clearbutton(self):
        self.manager.current="homepage"

    def logout(self):
        self.manager.current="login"
        self.cur=-1

    def closebutton(self):
        conn.commit()
        App.get_running_app().stop()



class SigninWindow(BoxLayout,Screen):
    def __init__(self, **kwargs):
       super().__init__(**kwargs)

    def validate_user(self):
        user = self.ids.username_field
        pwd = self.ids.pwd_field
        info = self.ids.infologin

        uname=user.text
        passw=pwd.text
        templist=(uname,passw)
        fetchlist=list(c.execute("select username,password from logindetails"))
        if(uname=="admin" and passw=="admin"):
            info.text=""
            user.text="" #Clearing Username and pass Feild
            pwd.text=""
            self.manager.current="addland"

        elif(templist in fetchlist):
            info.text=""
            user.text="" #Clearing Username and pass Feild
            pwd.text=""
            self.manager.current="homepage"
        else:
            info.text='[color=#FF0000]Wrong Username or password[/color]'

    def closebutton(self):
        conn.commit()
        App.get_running_app().stop()

class RegisterWindow(BoxLayout,Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def completeregister(self):
        name = self.ids.name_register.text
        email = self.ids.email_register.text
        user = self.ids.username_register.text
        pwd = self.ids.password_register.text
        info = self.ids.inforegister


        if(name=="" or email=="" or user=="" or pwd==""):
            info.text='[color=#FF0000]Please fill all the details![/color]'
        else:
            info.text='[color=#FF0000]Succesffully Succesfully Registered[/color]'
            templist=(name,email,user,pwd)
            c.execute("insert into logindetails values(?,?,?,?)",templist)


    def closebutton(self):
        conn.commit()
        App.get_running_app().stop()

class AddWindow(BoxLayout,Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def addland(self):
        name=self.ids.add_land_name.text
        price=self.ids.add_land_price.text
        address=self.ids.add_land_address.text
        area=self.ids.add_land_area.text
        info=self.ids.infoAdd
        if(name=="" or price=="" or address=="" or area==""):
            info.text='[color=#FF0000]Please fill all the details![/color]'
        else:
            info.text='[color=#FF0000]Land Added Succesfully[/color]'
            templist=(name,price,area,address)
            c.execute("insert into land values(?,?,?,?)",templist)

    def closebutton(self):
        conn.commit()
        App.get_running_app().stop()


kv=Builder.load_file("my1.kv")

class SigninApp(App):
    def build(self):
        return kv

obj=SigninApp()
obj.run()
