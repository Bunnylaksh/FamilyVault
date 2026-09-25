from pathlib import Path
from cryptography.fernet import Fernet, InvalidToken
from plyer import filechooser
import os 

from kivy.config import Config
Config.set('graphics','width','320')
Config.set('graphics','height','520')

from kivy.lang import Builder

from kivy.core.window import Window
from kivy.metrics import dp

from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.uix.behaviors import FocusBehavior
from kivymd.uix.list import MDListItem, MDListItemHeadlineText
from kivymd.uix.button import MDButton, MDButtonText, MDIconButton 
from kivymd.uix.label import MDLabel
from kivymd.uix.appbar import MDTopAppBar
from kivymd.uix.dialog import MDDialog, MDDialogHeadlineText, MDDialogSupportingText, MDDialogButtonContainer
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.graphics import StencilPush, StencilUse, StencilUnUse, StencilPop, Ellipse, Color, Rectangle
from kivy.factory import Factory


from Screen_handler import KV
from database_service import DatabaseService

FK="QI8i4E8eNCGnncfKmVq_e3oCCAmjh44KC58wMe4PtjQ="

class SetupScreen(Screen):
    pass
class HomeScreen(Screen):
    pass
class AddAccountScreen(Screen):
    pass   
class AccountDetailsScreen(Screen):
    pass  
class AddAccountDetailsScreen(Screen):
    pass
class EditAccountDetailsScreen(Screen):
    pass
class FocusableMDButton(FocusBehavior,MDButton):
    pass
    
class CircularImage(Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        with self.canvas.before:
            StencilPush()
            
            self.circle = Ellipse(pos=self.pos, size=self.size)
            StencilUse()
            
        with self.canvas.after:
            StencilUnUse()
            StencilPop()
            
        self.bind(pos=self.update_circle, size=self.update_circle)
    
    def update_circle(self, *args):
        self.circle.pos=self.pos
        self.circle.size=self.size
        
Factory.register("CircularImage",cls=CircularImage)
    
class FamilyVaultApp(MDApp):
    selected_account_id = None
    selected_acc_ln_id = None
    selected_bank_name = None
    selected_bank_account_number = None
    showing_secret_id= None
    e_u_type=None
    e_u_name=None
    e_u_password=None
    e_u_pin=None
    
    def build(self):
        self.db= DatabaseService()
        root=Builder.load_string(KV)
        return root
        
    def on_start(self):
        Window.bind(on_key_down=self.handle_tab)
        if self.create_master_password():
            self.root.current="setup"
            
    def handle_tab(self, window, key, scancode, codepoint, modifiers):
        screen=self.root.current_screen
        if key == 9:
            if self.root.current=="add":
                fields =[screen.ids.bank_name,screen.ids.account_number,screen.ids.IFSC_code,screen.ids.MICR_code,]
            elif self.root.current=="add_new_detail":
                fields =[screen.ids.u_type,screen.ids.u_name,screen.ids.u_password,screen.ids.u_pin,]
            elif self.root.current=="edit_detail":
                fields =[screen.ids.e_u_type,screen.ids.e_u_name,screen.ids.e_u_password,screen.ids.e_u_pin,]
            else:
                fields =[screen.ids.confirm_password, screen.ids.cv_button,]
                
            for i, field in enumerate(fields):
                if field.focus:
                    print( i, field, field.focus)
                    field.focus=False                   
                    if i< len(fields) -1:
                        print( i, field, field.focus)
                        fields[i+1].focus =True                  
                    return True                             
        return False
        
    def select_profile_image(self):
        filechooser.open_file(on_selection=self.profile_image_selected, filters=["*.png","*.jpg","*.jpeg"])
        
    def profile_image_selected(self, selection):
        if selection:
            image_path= selection[0]
            screen=self.root.get_screen("setup")
            
            screen.ids.profile_image.source = image_path
            screen.ids.profile_image.reload()
            
    def create_master_password(self):
        screen=self.root.get_screen("setup")
        confirm=screen.ids.confirm_password.text
        
        if not confirm:
            screen.ids.message.text="Enter the Vault Password:"
            return
        master_file=(Path(__file__).resolve().parent/"Abhaya.txt")
        
        if not master_file.exists():
            screen.ids.message.text=("Encrypted password file not found")
            return
        
        try:
            with open(master_file, "r", encoding="utf-8") as file:
                encrypted_password=file.read().strip()
            cipher=Fernet(FK)
            
            decrypted_password=cipher.decrypt(encrypted_password.encode("utf-8")).decode("utf-8")
            
            if confirm != decrypted_password:
                screen.ids.message.text="Password not matching:"
                return
            else:  
                self.root.current="home"
                screen.ids.confirm_password.text=""
                self.load_accounts()  
        except InvalidToken:
            screen.ids.message.text=("Unable to verify password")
        except Exception as e:
            screen.ids.message.text=("Error reading password file")
            print("password verification error",e)
    
    def child_account_details(self):
        screen=self.root.get_screen("add_new_detail")
        screen.ids.my_toolbar.text="Add Details for Bank: "+self.selected_bank_name+"\n"+self.selected_bank_account_number
        self.root.current = "add_new_detail"
        
    def load_accounts(self):
        account_list=self.root.get_screen("home").ids.account_lists
        account_list.clear_widgets()
        accounts= self.db.get_account()
        
        from kivymd.uix.list import (MDListItem, MDListItemLeadingIcon, MDListItemHeadlineText, MDListItemSupportingText)
        for account in accounts:
            id, bank_name, account_number, IFSC_code, MICR_code=account
            masked_account="****"+str(account_number)[-4:] 
            
            item=MDListItem(on_release=lambda x, account_id=id:self.show_account_details(account_id))
            headline=MDListItemHeadlineText(text=bank_name)
            supportline=MDListItemSupportingText(text=masked_account)
            icon=MDListItemLeadingIcon(icon="bank")
            
            item.add_widget(icon)
            item.add_widget(headline)
            item.add_widget(supportline)
            
            account_list.add_widget(item)
                   
            
    def save_account(self):
        Window.bind(on_key_down=self.handle_tab)
        screen=self.root.get_screen("add")
        
        self.db.add_account(
            screen.ids.bank_name.text,
            screen.ids.account_number.text,
            screen.ids.IFSC_code.text,
            screen.ids.MICR_code.text
        )
                    
        # Clear fields
        for field in ["bank_name", "account_number","IFSC_code","MICR_code"]:
            screen.ids[field].text=""
            
        self.load_accounts()
        self.root.current = "home"
        
    def save_account_details(self):
        Window.bind(on_key_down=self.handle_tab)
        screen=self.root.get_screen("add_new_detail")        
        
        self.db.add_account_details(
            self.selected_account_id,
            screen.ids.u_type.text,
            screen.ids.u_name.text,
            screen.ids.u_password.text,
            screen.ids.u_pin.text
        )
                    
        # Clear fields
        for field in ["u_type","u_name","u_password","u_pin"]:
            screen.ids[field].text=""
        
        self.load_account_details()
        self.root.current = "account_detail"        

    def show_account_details(self, account_id):
        self.selected_account_id = account_id
        
        account = self.db.get_account_by_id(account_id)
        
        self.selected_bank_name = str(account[1])
        self.selected_bank_account_number= "Account Number: "+str(account[2])

        if not account:
            print("Account Not Found: "+account_id)
            return
        
        screen = self.root.get_screen("account_detail")
        screen.selected_account_id = account_id
        #screen.ids.account_number.text=self.selected_bank_account_number
        
        
        self.root.current = "account_detail"        
            
        self.load_account_details()
        
    def load_account_details(self):
        screen = self.root.get_screen("account_detail")
        screen.ids.top_app_bar_account_details.text="Bank Name: "+self.selected_bank_name+"\n"+self.selected_bank_account_number
        table=screen.ids.details_table
        table.clear_widgets()
        
        details = self.db.get_account_details_by_id(self.selected_account_id)
        
        self.add_cell(table,"Type",150,2,True)
        self.add_cell(table,"User Name",150,2,True)
        self.add_cell(table,"Created Date",150,2,True)
        self.add_cell(table,"Updated Date",150,2,True)        
        self.add_cell(table,"Password",150,2,True)
        self.add_cell(table,"Pin",90,2,True)
        self.add_cell(table,"View",60,2,True)        
        self.add_cell(table,"Edit",60,2,True)
        self.add_cell(table,"Delete",60,2,True)
        r_no =0
        for detail in details:
            r_no += 1
            acc_line_id = detail[0]
            detail_id = detail[1]
            use_type= detail[3]
            username=detail[4]
            password=detail[5]
            pin=detail[6]
            crdt=detail[7].split("T")[0]
            updt=detail[8].split("T")[0]

            self.add_cell(table,use_type,150,r_no,False)
            self.add_cell(table,username,150,r_no,False)
            
            
            if self.showing_secret_id != acc_line_id:
                password_text="*******"
                pin_text="*******"
                
            else:
                password_text = str(password)
                pin_text = str(pin)
                
            self.add_cell(table,crdt,150,r_no,False)
            self.add_cell(table,updt,150,r_no,False)               
            self.add_cell(table,password_text,150,r_no,False)
            self.add_cell(table,pin_text,90,r_no,False)

            
            
            edit_button= MDIconButton(icon="pencil", size_hint_x=None, width=dp(10), halign="left", valign="middle", on_release=lambda x, did=acc_line_id:self.edit_detail(did))
            delete_button= MDIconButton(icon="delete", size_hint_x=None, width=dp(10), halign="left", valign="middle", on_release=lambda x, did=acc_line_id:self.delete_detail(did))           
            eye_button=MDIconButton(icon="eye-off" if self.showing_secret_id != acc_line_id else "eye", size_hint_x=None, width=dp(10), halign="center", valign="middle", on_release=lambda x, did=acc_line_id :self.toggle_secret(did))

            table.add_widget(eye_button)            
            table.add_widget(edit_button)
            table.add_widget(delete_button)

            
    def add_cell(self, table, text, width, row_number,b):
        if row_number % 2 == 0 :
            bg_color = (0.95,0.95,0.95, 1)
        else: 
            bg_color = (0.85,0.85,0.85, 1)
            
        if b:
            label = MDLabel(text=str(text), bold=True, size_hint_x=None, width=dp(width), halign="left", valign="middle")            
        else:
            label = MDLabel(text=str(text), size_hint_x=None, width=dp(width), halign="left", valign="middle")
            
            
        with label.canvas.before:
            Color(*bg_color)
            label.bg = Rectangle(pos=label.pos, size=label.size)
            
            label.bind(pos=lambda instance, value: setattr(instance.bg,"pos",value),size=lambda instance, value: setattr(instance.bg,"size",value))
            
        table.add_widget(label)
            
            
    def toggle_secret(self,acc_line_id):
        if self.showing_secret_id == acc_line_id:
            self.showing_secret_id = None
        else:
            self.showing_secret_id = acc_line_id
            
        self.load_account_details()        
        
    def update_account_details(self):
        screen_edit = self.root.get_screen("edit_detail")
        field_name=[]
        value_name=[]
        if (self.e_u_type!=screen_edit.ids.e_u_type.text or self.e_u_name!=screen_edit.ids.e_u_name.text or self.e_u_password!=screen_edit.ids.e_u_password.text or self.e_u_pin!=screen_edit.ids.e_u_pin.text):
                
            if self.e_u_type!=screen_edit.ids.e_u_type.text:
                field_name.append("use_type")
                value_name.append(screen_edit.ids.e_u_type.text)                
            if self.e_u_name!=screen_edit.ids.e_u_name.text:
                field_name.append("User_name")
                value_name.append(screen_edit.ids.e_u_name.text)
            if self.e_u_password!=screen_edit.ids.e_u_password.text:
                field_name.append("User_Password")
                value_name.append(screen_edit.ids.e_u_password.text)                
            if self.e_u_pin!=screen_edit.ids.e_u_pin.text:
                field_name.append("User_Pin")
                value_name.append(screen_edit.ids.e_u_pin.text)
            
            update_dialog=MDDialog(MDDialogHeadlineText(text="Updating Account Details"),MDDialogSupportingText(text="Fields: "+str(field_name)+" are getting updated !!!"),
            MDDialogButtonContainer(Widget(),MDButton(MDButtonText(text="Cancel"), style="text", on_release=lambda x:update_dialog.dismiss()), MDButton(MDButtonText(text="Confirm"), style="text", on_release=lambda x:self.close_update_dialog(update_dialog,self.selected_acc_ln_id,field_name,value_name)),spacing="8dp",))
            update_dialog.open()
                    
        else:
            no_update_dialog=MDDialog(MDDialogHeadlineText(text="Update Account Details"),MDDialogSupportingText(text="There are no updates to save !!!"),
            MDDialogButtonContainer(Widget(),MDButton(MDButtonText(text="Ok"), style="text", on_release=lambda x:no_update_dialog.dismiss()),spacing="8dp",))
            no_update_dialog.open()
                
        
        self.root.current = "account_detail"
        
        
    def edit_detail(self, acc_line_id):
        Window.bind(on_key_down=self.handle_tab)
        screen_edit = self.root.get_screen("edit_detail")
        screen_edit.ids.my_toolbar_edit.text="Bank Name: "+self.selected_bank_name+"\n"+self.selected_bank_account_number
        self.selected_acc_ln_id=acc_line_id
        home_details=self.db.get_account_line_details_by_id(self.selected_account_id, acc_line_id)
        
                    
        screen_edit.ids.e_u_type.text=home_details[0][1]
        screen_edit.ids.e_u_name.text=home_details[0][2]
        screen_edit.ids.e_u_password.text=home_details[0][3]
        screen_edit.ids.e_u_pin.text=home_details[0][4]
        
        self.e_u_type=home_details[0][1]
        self.e_u_name=home_details[0][2]
        self.e_u_password=home_details[0][3]
        self.e_u_pin=home_details[0][4]
        
        self.root.current="edit_detail" 

       
    def delete_detail(self,acc_line_id):   
        delete_dialog=MDDialog(MDDialogHeadlineText(text="Delete Account Details"),MDDialogSupportingText(text="Are you sure to delete the record ?"),
        MDDialogButtonContainer(Widget(),MDButton(MDButtonText(text="Cancel"), style="text", on_release=lambda x:delete_dialog.dismiss()), MDButton(MDButtonText(text="Confirm"), style="text", on_release=lambda x:self.close_delete_dialog(delete_dialog,acc_line_id)),spacing="8dp",))
        delete_dialog.open() 
    
    def close_delete_dialog(self,delete_dialog,acc_line_id):
        delete_dialog.dismiss()
        self.db.delete_account_by_id(acc_line_id)
        self.load_account_details()
        
    def close_update_dialog(self, update_dialog, acc_line_id, field_name, value_name):
        update_dialog.dismiss()
        self.db.update_acc_line_details(acc_line_id, field_name, value_name)
        self.root.current="account_detail" 
        self.load_account_details()
                               
if __name__=="__main__":
    FamilyVaultApp().run()
            
                 
                 