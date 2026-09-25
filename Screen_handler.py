KV="""
ScreenManager:
    SetupScreen:
        name:"setup"
    HomeScreen:
        name:"home"
    AddAccountScreen:
        name:"add"
    AccountDetailsScreen:
        name:"account_detail" 
    AddAccountDetailsScreen:
        name:"add_new_detail"         
    EditAccountDetailsScreen:
        name:"edit_detail"     
        
<SetupScreen>:
    MDBoxLayout:
        orientation: "vertical"
        md_bg_color:255/255.0, 255/255.0, 252/255.0, 1
        padding: "10dp" 
        spacing: "10dp"
        
        MDTopAppBar:
            type:"small"
            size_hint_y:None
            height:"56dp"
            
            MDTopAppBarTitle:
                text:"Welcome !!! AABHAYA !!!"
                halign: "center"
                bold: True
                role: "medium"
                font_style: "Title"
        FloatLayout:
            size_hint_y: None
            height: "150dp"
            
            CircularImage:
                id: profile_image
                source: "assests/profile.jpg"
                size_hint:None, None
                size: "200dp", "200dp"
                pos_hint: {"center_x":0.5,"center_y":0.3}
                halign: "center"
                allow_stretch: True
                keep_ratio: True
                
            Button:
                size_hint: None, None
                size: "110dp", "110dp"
                pos_hint: {"center_x":0.5,"center_y":0.5}
                background_color:0,0,0,0
                on_release: app.select_profile_image()
                
        MDBoxLayout:
            orientation:"vertical"
            padding: "10dp"
            spacing: "10dp"

            Widget:
                size_hint_y: 1
              
            MDLabel:
                id: message
                text:"Confirm Master Password"
                halign: "center"
                bold: True
                role: "large"
                size_hint_y: None
                
                
            MDTextField:
                id: confirm_password
                hint_text: "Confirm Master Password"
                password: True           
                focus_next: root.ids.cv_button
                         
            FocusableMDButton:   
                id: cv_button 
                focusable: True
                pos_hint: {"center_x":0.5}            
                on_release: app.create_master_password()
                
                MDButtonText:
                    text: "Enter Vault"
                
<HomeScreen>:
    MDBoxLayout:
        orientation: "vertical"
        md_bg_color:255/255.0, 255/255.0, 252/255.0, 1        
        padding: "20dp"
        spacing: "10dp"
        
        MDTopAppBar:
            type:"small"
            
            MDTopAppBarTitle:
                text:"Family Bank Accounts"
                halign: "center"
                
        MDScrollView: 
            do_scroll_x: False
            do_scroll_y: True
            MDList:
                id:account_lists
                spacing: "5dp"
                padding: "5dp"
 
        MDBoxLayout:
            orientation:"horizontal"
            size_hint_y: None
            height: "60dp"
            padding: "10dp"
            spacing: "10dp"
            
        MDButton:
            pos_hint: {"center_x":0.5,"center_y":3.0}
            on_release:app.root.current = "add"
            MDButtonText:
                text: "[+] Add Accounts"
                     
        MDButton:
            pos_hint: {"center_x":0.5,"center_y":1.5}
            on_release: app.root.current="setup"          
            MDButtonText:
                text: "Logout"
            
<AddAccountScreen>:      
    MDBoxLayout:
        orientation: "vertical"
        md_bg_color:255/255.0, 255/255.0, 252/255.0, 1       
        padding: "20dp"
        spacing: "5dp"
        
        MDTopAppBar:
            type:"small"
            
            MDTopAppBarTitle:
                text:"Enter Bank Account Details"
                halign: "center"
                padding: "10dp"
                spacing: "10dp"  
                
        MDLabel:
            text:"Bank Name"
            size_hint_y: None
            height:"25dp"
            
        MDTextField:
            id: bank_name
            hint_text:"Bank Name" 
            
        MDLabel:
            text:"Account Number"
            size_hint_y: None
            height:"10dp"            
            
        MDTextField:
            id: account_number
            hint_text:"Account Number"  

        MDLabel:
            text:"IFSC Code"
            size_hint_y: None
            height:"10dp"
            
        MDTextField:
            id: IFSC_code
            hint_text:"IFSC Code" 

        MDLabel:
            text:"MICR Code"
            size_hint_y: None
            height:"10dp"
            
        MDTextField:
            id: MICR_code
            hint_text:"MICR Code"
        
        MDBoxLayout:
            orientation: "horizontal"
            height: "10dp"
            
            MDButton:
                y: "20dp"
                hlign: "center"
                on_release: app.root.current="home"          
                MDButtonText:
                    text: "Back"            
        
        MDBoxLayout:
            orientation: "horizontal"
            height: "10dp"
            
            MDButton:
                y: "20dp"
                on_release: app.save_account()         
                MDButtonText:
                    text: "Save Account"
            Widget:
            
            MDButton:
                y: "20dp"
                on_release: app.root.current="setup"          
                MDButtonText:
                    text: "Logout"
                
<AccountDetailsScreen>:
    MDBoxLayout:
        orientation: "vertical"
        md_bg_color:255/255.0, 255/255.0, 252/255.0, 1       
        padding: "20dp"
        spacing: "10dp"
        
        MDTopAppBar:
            type:"small"
            
            MDTopAppBarTitle:
                id: top_app_bar_account_details
                text:""
                bold: True
                font_style: "Title" 
                role: "small"
                halign: "center"           
                          
                
        MDBoxLayout:
            orientation: "vertical"
            size_hint_y: None
            height: "270dp"
            padding: "5dp"
            spacing: "5dp" 
            
            MDScrollView:
                do_scroll_x: True
                do_scroll_y: True
                
                GridLayout:
                    id: details_table
                    
                    cols:9
                    
                    size_hint: None, None
                    width: dp(1040)
                    height: self.minimum_height
                    
                    row_default_height: dp(60)
                    row_force_default: True
        
        
        MDBoxLayout:
            orientation: "horizontal"
            height: "10dp"            
            
            MDButton:
                y: "20dp"
                halign: "center"
                on_release: app.root.current="home"          
                MDButtonText:
                    text: "Back" 

                
        MDBoxLayout:
            orientation:"horizontal"
            height: "10dp"
            
            MDButton:
                y: "20dp"
                on_release:app.child_account_details()
                MDButtonText:
                    text: "[+] Details"
            Widget:
            
            MDButton:
                y: "20dp"
                on_release: app.root.current="setup"          
                MDButtonText:
                    text: "Logout" 
                
<AddAccountDetailsScreen>:
    MDBoxLayout:
        orientation: "vertical"
        md_bg_color:255/255.0, 255/255.0, 252/255.0, 1  
        height: "20dp"
        padding: "20dp"
        spacing: "10dp"
        
        MDTopAppBar:
            type:"small"
            
            MDTopAppBarTitle:
                id: my_toolbar
                text: ""
                bold: True
                font_style: "Title" 
                role: "small"
                halign: "center"                 
            
        MDLabel:
            text:"Use Type"
            size_hint_y: None
            height:"5dp"            
        MDTextField:
            id: u_type
            hint_text:"Use Type"   

        MDLabel:
            text:"User Name"
            size_hint_y: None
            height:"5dp"            
        MDTextField:
            id: u_name
            hint_text:"User Name" 

        MDLabel:
            text:"Password"
            size_hint_y: None
            height:"5dp"            
        MDTextField:
            id: u_password
            hint_text:"Password"   

        MDLabel:
            text:"Pin Number"
            size_hint_y: None
            height:"5dp"            
        MDTextField:
            id: u_pin
            hint_text:"Pin Number" 
        
        MDBoxLayout:
            orientation:"horizontal"
            height: "10dp"
            
            MDButton:
                y: "20dp"
                halign: "center"
                on_release: app.root.current="account_detail"          
                MDButtonText:
                    text: "Back"        

                
        MDBoxLayout:
            orientation:"horizontal"
            height: "20dp"
            
            MDButton:
                y: "20dp"
                on_release: app.save_account_details()         
                MDButtonText:
                    text: "Save Account Details"            
                      
            Widget:
                
            MDButton:
                y: "20dp"
                on_release: app.root.current="setup"          
                MDButtonText:
                    text: "Logout" 
                    
<EditAccountDetailsScreen>:
    MDBoxLayout:
        orientation: "vertical"
        md_bg_color:255/255.0, 255/255.0, 252/255.0, 1  
        height: "20dp"
        padding: "20dp"
        spacing: "10dp"
        
        MDTopAppBar:
            type:"small"
            
            MDTopAppBarTitle:
                id: my_toolbar_edit
                text: ""
                halign: "center"
                bold: True
                font_style: "Title"
                role: "small"
            
        MDLabel:
            text:"Use Type"
            size_hint_y: None
            height:"5dp"            
        MDTextField:
            id: e_u_type
            hint_text:"Use Type"   

        MDLabel:
            text:"User Name"
            size_hint_y: None
            height:"5dp"            
        MDTextField:
            id: e_u_name
            hint_text:"User Name" 

        MDLabel:
            text:"Password"
            size_hint_y: None
            height:"5dp"            
        MDTextField:
            id: e_u_password
            hint_text:"Password"   

        MDLabel:
            text:"Pin Number"
            size_hint_y: None
            height:"5dp"            
        MDTextField:
            id: e_u_pin
            hint_text:"Pin Number" 
        
        MDBoxLayout:
            orientation:"horizontal"
            height: "20dp"
            
            MDButton:
                y: "10dp"
                halign: "center"
                on_release: app.root.current="account_detail"          
                MDButtonText:
                    text: "Back"        

                
        MDBoxLayout:
            orientation:"horizontal"
            height: "20dp"
            
            MDButton:
                y: "10dp"
                on_release: app.update_account_details()         
                MDButtonText:
                    text: "Update Details"            
                      
            Widget:
                
            MDButton:
                y: "10dp"
                on_release: app.root.current="setup"          
                MDButtonText:
                    text: "Logout" 
                    
"""
