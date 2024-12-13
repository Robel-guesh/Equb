import sqlite3
from tkinter import *
from tkinter import ttk 
from tkinter import messagebox
from tkinter import filedialog,simpledialog
from time import strftime
from datetime import datetime
from datetime import date
import shutil
import os
import bcrypt
from PIL import Image,ImageTk,ImageFont
import random
from calanders import *
from scan_qrcode import scan_qrcode
from create_pdf import create_pdf
from functools import partial

#**************************************variables**************************************************
customer_name=''
company_title='MOYA '
# company_name='moya-equb'
role=['user','admin','super_admin']
current_user=''
user_role='user'
window_icon='./image/icon.ico'
Tera=ImageFont.truetype('./font/Tera-Regular.ttf')
equb_type=[]
equb_type_list=[]
customer_list=[]
customer_id_list=[]
enrolled_customer_list=[]
enrolled_equb_type=[]
user_account_list=[]
all_equb_list=[]
punishmet_list=[]
equb_state=['not_finished','finished']
expire_date_list=['no']
database_name='db/db.db'
profile_photo_name=['./image/profile/clock.png']
error={"user_name_error":'',"password_error":''}

default_profile_photo='./image/login.png'
drawn_customer_list=[]
drawn_warrant_list=[]
drawn_equb_type=[]
undrawn_customer_list=[]
# *****************clock function*****************************************************************
def todays():
    # ethiopian_date=Gergorian_to_Ethiopian(int(strftime('%d')),int(strftime('%m')),int(strftime('%Y')))
    # return(strftime(ethiopian_date))
    return(strftime('%d/%m/%Y'))
clock=todays()
def fetch_data(query,table_name):
    db = sqlite3.connect(database_name)
    cursor = db.cursor()
    cursor.execute(f'select {query} from {table_name} order by oid desc ')
    result=cursor.fetchall()
    return result
    cursor.close()
    db.commit()
    db.close()


company_name=fetch_data("company_name","company_name")[0][0]
def fetch_data_like(query,table_name,filter_by,like_value):
    db = sqlite3.connect(database_name)
    cursor = db.cursor()
    cursor.execute(f"select {query} from {table_name}  where {filter_by} like '%"+like_value+"%' order by oid desc")
    result=cursor.fetchall()
    return result
    cursor.close()
    db.commit()
    db.close()
def fetch_data_by_id(query,table_name,given_id):
    try:
        db = sqlite3.connect(database_name)
        cursor = db.cursor()
        cursor.execute((f'select {query} from {table_name} where id=?'),[given_id])
        result=cursor.fetchone()
        return result
        cursor.close()
        db.commit()
        db.close()  
    except:
        pass
def fill_punishment_list():
    all_punishment_list=fetch_data('*','punishment')
    punishmet_list.clear()
    
    for i in all_punishment_list:
        if i not in punishmet_list:
            punishmet_list.append(i[0])
    
fill_punishment_list()
def return_current_round(equb_type):
    
    db = sqlite3.connect(database_name)
    cursor = db.cursor()
    
    cursor.execute("select current_round from round where equb_type_id=(select id from equb_type where equb_type=?)",[equb_type])
    result=cursor.fetchone()
    return result
    cursor.close()
    db.commit()
    db.close()

def display_profile_picture(photo_name,container,size=(152, 152)):
        try:      
            if photo_name!=default_profile_photo:
                image=Image.open(photo_name)
                image = image.resize(size)
                photo = ImageTk.PhotoImage(image)
                container.config(image=photo)
                container.image = photo  
            else:
                container.config(image=None)
                container.config(text='')  
                container.image= None
                container.update()
        except:
            pass  
def display_logged_user_profile_picture(photo_name,container):
    try:      
        if photo_name!=default_profile_photo:
            image=Image.open(photo_name)
            image = image.resize((45, 45))
            photo = ImageTk.PhotoImage(image)
            container.config(image=photo)
            container.image = photo  
        else:
            container.config(image=None)
            container.config(text='')  
            container.image= None
            container.update()
    except:
        pass  
def clear_image(container):
    container.config(image=None)
    container.config(text='')  
    container.update()    
def fill_date(date_entry_name):
        date_entry_name.delete(0,END)
        date_entry_name.insert(END,clock)
def refresh_all():
    fill_payment_customer_list()
    fill_drawn_customer_list()            
#****************************************control close window*****************************************
def close_about_window():
    home_page.state('normal')
    about_window.destroy()
def close_main_window():
    home_page.deiconify()
    # home_page.state('normal')
    main_window.destroy()

#******************************************** main page******************************************

# def check_user_name_and_password():
#     db = sqlite3.connect(database_name)
#     cursor = db.cursor()
#     cursor.execute(('select * from customer where user_name=? and password=?'),[user_name_entry.get(),password_entry.get()])
#     result=cursor.fetchone()
#     cursor.close()
#     db.commit()
#     db.close()
#     if result:
#         logged_user_role=result[4]
#         display_main_window()
def display_main_window():
    company_name=fetch_data("company_name","company_name")[0][0]
    def refresh():
        
        clear_registration_form()
        fetch_customer_and_insert_into_table()
        
    def clear_registration_form():
        id_entry.delete(0,END)
        name_entry.delete(0,END)
        phone_number_entry.delete(0,END)
        
        date_entry.delete(0,END)
        photo_entry.delete(0,END)
        customer_adress_entry.delete(0,END)
        
        display_profile_picture(default_profile_photo,customer_photo_info_label)
    def clear_information_label():
        information_label.config(text='')
    def search_customer_and_fill_event(event):
        search_customer_and_fill()
        check_cusotmer_modification()
     
    def search_customer_and_fill():
        db = sqlite3.connect(database_name)
        cursor = db.cursor()
        cursor.execute(('select * from customer where id=?'),[search_customer.get()])
        result=cursor.fetchone()
        cursor.close()
        db.commit()
        db.close()
        
        # clear_registration_form()   
        if result :
            # i=[]
            # i.clear()
            # for j in result:
            #     i.append(j)
            id_entry.delete(0,END)
            id_entry.insert(END,result[0])
            name_entry.delete(0,END)
            name_entry.insert(END,result[1])
            phone_number_entry.delete(0,END)
            phone_number_entry.insert(END,result[2])
            customer_adress_entry.delete(0,END)
            customer_adress_entry.insert(END,result[3])
            date_entry.delete(0,END)
            date_entry.insert(END,result[4])
            photo_entry.delete(0,END)
            photo_entry.insert(END,result[5])
            
            display_profile_picture(result[5],customer_photo_info_label)  
                
        else:
            display_profile_picture(default_profile_photo,customer_photo_info_label)
            clear_registration_form()
            refresh()
    
    def register_customer():
        def profile_Photo():
            
            if (len(photo_entry.get())>0) :
                photo=photo_entry.get()
            else: photo="./image/profile/logo.png"
            
            return photo
        
        profile_to_pdf()

        id_num=id_entry.get()
        name=name_entry.get()
        phone=phone_number_entry.get()
        date=date_entry.get()
        photo=profile_Photo()
        db = sqlite3.connect(database_name)
        cursor = db.cursor()
        table_name='customer'
        next_id=(int(id_entry.get())+1)
        
        cursor.execute(f"insert into  {table_name} values (?,?,?,?,?,?)", (
            [id_num,name,phone,customer_adress_entry.get(),date,str(photo)]))
        cursor.execute("update  id_register SET reached_id = ? where id=?",(next_id,1))
        cursor.close()
        db.commit()
        db.close()
        clear_registration_form()
        refresh()
        refresh_combo()
        fill_customer_list()
        clear_information_label()
        information_label.config(text='ዓሚል ብትክክል ተመዝጊቡ')
        information_label.after('4000',clear_information_label)
        fill_id()
        fill_date(date_entry)
        fill_drawn_customer_list()
        fill_customer_names()
        # clear_customer_info_lables()
    def update_customer():
        def profile_Photo():
            
            if (len(photo_entry.get())>0) :
                photo=photo_entry.get()
            else: photo="./image/profile/logo.png"
            
            return photo
        profile_to_pdf()
        id_num=id_entry.get()
        name=name_entry.get()
        phone=phone_number_entry.get()
        date=date_entry.get()
        photo=profile_Photo()
        customer_id=search_customer.get()
        db = sqlite3.connect(database_name)
        cursor = db.cursor()
        table_name='customer'
        next_id=(int(id_entry.get())+1)
        
        cursor.execute(f"update  {table_name} set customer_name=? ,phone_number=?,customer_adress=? ,registration_date=? ,photo=?  where id=?", (
            [name,phone,customer_adress_entry.get(),date,str(photo),customer_id]))
        cursor.close()
        db.commit()
        db.close()
        clear_registration_form()
        refresh()
        refresh_combo()
        fill_customer_list()
        clear_information_label()
        information_label.config(text='መዝገብ ዓሚል ብትትክል ተመሓይሹ')
        information_label.after('4000',clear_information_label)
        fill_id()
        fill_date(date_entry)
        fill_drawn_customer_list()
        refresh_all()
    def delete_customer():
        customer_id=search_customer.get()
        db = sqlite3.connect(database_name)
        cursor = db.cursor()
        table_name='customer'
        next_id=(int(id_entry.get())+1)
        
        cursor.execute(f"delete from  {table_name}   where id=?", (
            [customer_id]))
        cursor.execute(f"delete from  pay_list  where customer_id=?", (
            [customer_id]))
        cursor.execute(f"delete from  drawn_list  where customer_id=?", (
            [customer_id]))
        cursor.execute(f"delete from  equb_enrollment  where customer_id=?", (
            [customer_id]))
        cursor.close()
        db.commit()
        db.close()
        clear_registration_form()
        refresh()
        refresh_combo()
        fill_customer_list()
        clear_information_label()
        information_label.config(text='ዓሚል ካብ መዝገብ ጠፊኡ')
        information_label.after('4000',clear_information_label)
        fill_id()
        fill_date(date_entry)
        fill_drawn_customer_list()
        refresh_all()
    global main_window
    styles=ttk.Style()
    main_window=Toplevel(home_page)
    home_page.state('withdrawn')
    main_window.title(company_title)
    main_window.configure(background='white')
    main_window.geometry(f"{screen_height}x{screen_width}+0+0")
    main_window.minsize(screen_width,screen_height)
    main_window.state('normal')
    main_window.iconbitmap(window_icon)
    main_window_menu=Menu(main_window)
    main_window.config(menu=main_window_menu)
    main_window_submenu=Menu(main_window_menu)
    main_window_menu.add_cascade(label='ፋይል',menu=main_window_submenu)
    main_window_submenu.add_command(label='መሐለውታ ፋይል ኣቐምጥ',command=create_backup_file)
    # main_window_submenu.add_command(label='መለለዪ ካርዲ ኣሕትም',command=print)
    main_window_submenu.add_command(label='ዕፆ',command=close_main_window)
    search_photo=PhotoImage(file='./image/search.png')
    close_photo=PhotoImage(file='./image/close.png')
    def edit_profile():
        main_notebook.select(3)
        profile_frame.grid(row=0,column=0,padx=20,sticky='n')
        if logged_user_role=='super_admin':
            
            search_user_entry.delete(0,END)
            search_user_entry.insert(END,logged_user_id)
            search_user_entry.focus()
        else:
            full_name_entry.delete(0,END)
            full_name_entry.insert(END,logged_user_full_name)
            register_user_name_entry.delete(0,END)
            register_user_name_entry.insert(END,logged_user_name)
            role_entry.delete(0,END)
            role_entry.insert(END,logged_user_role)
            user_profile_photo_entry.delete(0,END)
            updated_photo=fetch_data_by_id('photo', 'user', logged_user_id)
            if updated_photo!=None:
                user_profile_photo_entry.insert(END,updated_photo[0])
                display_profile_picture(updated_photo[0], user_profile_photo_label)
    header_frame=Frame(main_window,width=screen_width,height=screen_height*0.1,background='darkblue')
    header_frame.grid(row=0,column=0)
    logo_label = ttk.Label(header_frame, image=small_equb_logo,background='darkblue')
    logo_label.place(x=0,y=0)
    title_label=Label(header_frame,text=company_name,foreground='yellow',background='darkblue',font=('bold',48)).place(x=int(0.4*screen_width),y=5)
    
    logged_profile_photo_label = ttk.Label(header_frame, image=small_equb_logo,background='darkblue')
    logged_profile_photo_label.place(x=int(screen_width-85),y=2)
    display_logged_user_profile_picture(logged_user_photo,logged_profile_photo_label)
    edit_profile_button=ttk.Button(header_frame,text='መለለዪ ኣመሓይሽ',command=edit_profile)
    edit_profile_button.place(x=int(screen_width-92),y=50)
    body_frame=Frame(main_window,width=screen_width,height=screen_height*0.7,background='pink')
    body_frame.grid(row=1,column=0)
    # footer_frame=Frame(main_window,width=screen_width,height=50,background='white')
    # footer_frame.grid(row=2,column=0)
    # clock_label=ttk.Label(footer_frame,text=clock,font=('bold',18))
    # clock_label.grid(row=0,column=0,padx=5,pady=5)
    
    footer_frame = Frame(main_window,height=screen_height*0.1,width=screen_width,background='white')
    footer_frame.grid(row=2,column=0)

    clock_label=ttk.Label(footer_frame,text=clock,font=('bold',18),background='white')
    clock_label.grid(row=1,column=1,padx=5,pady=10,sticky='e')
    
    
#*******************************************************************************
    main_notebook=ttk.Notebook(body_frame,width=int(screen_width),height=515)
    main_notebook.pack()
    
    registration_container_frame=ttk.Frame(main_notebook,width=screen_width,height=515)
    registration_container_frame.pack()
    registration_frame=ttk.Frame(registration_container_frame,width=int(screen_width*0.25),height=515)
    # registration_frame.pack(side=LEFT,anchor='n',padx=30,pady=10)
    

    drawn_container_frame=ttk.Frame(main_notebook,width=int(screen_width*0.3),height=515)
    drawn_container_frame.pack(side=LEFT,anchor='n',padx=100,pady=10)
   
    drawn_frame=ttk.Frame(drawn_container_frame,width=int(screen_width*0.3),height=515)
    drawn_frame.pack(side=LEFT,anchor='n',padx=20,pady=10)
    
    drawn_profile_photo_frame=ttk.Frame(drawn_container_frame,width=int(screen_width*0.50),height=515)
    drawn_profile_photo_frame.pack(side=LEFT,anchor='n',padx=100,pady=10)
    
    drawn_info_label=ttk.Label(drawn_profile_photo_frame,text='ስእሊ ናይ ዕጫ ዝበፅሖ ዓሚል')
    drawn_info_label.grid(row=4,column=0 ,padx=5,pady=10,sticky='w')
    drawn_profile_photo_label=ttk.Label(drawn_profile_photo_frame)
    drawn_profile_photo_label.grid(row=5,column=0,padx=5,pady=10)
    
    drawn_warrant_info_label=ttk.Label(drawn_profile_photo_frame,text='ናይ ወሓስ ስእሊ ')
    drawn_warrant_info_label.grid(row=4,column=1 ,padx=10,pady=10,sticky='w')
    drawn_warrant_profile_photo_label=ttk.Label(drawn_profile_photo_frame)
    drawn_warrant_profile_photo_label.grid(row=5,column=1,padx=10,pady=10)
    
    
    # drawn_counter_label=ttk.Label(drawn_profile_photo_frame,text="analog_clock")
    # drawn_counter_label.grid(row=2,column=0)
    def display_detailed_information(event,equb_info,customer_id):
        payment_customer_name_entry.delete(0,END)
        payment_customer_name_entry.insert(END,customer_id)
        payment_equb_type_entry.delete(0,END)
        payment_equb_type_entry.insert(END,equb_info)
        payment_amount_entry.focus()
        payment_equb_type_entry.focus()
        payment_customer_name_entry.focus()
        find_and_fill_payment_entries_from_enrollment()
    def fill_unpaid_lister():
        unpaid_customers=fetch_data('*','equb_enrollment')
        # print('before')
        # for widget in unpaid_lister_main_frame.winfo_children():
        #     print(widget)
            # widget.destroy()
        for i,customer_name in enumerate(unpaid_customers):
            
            unpaid_lister_child_frame=ttk.Frame(unpaid_lister_main_frame,width=int(screen_width*0.25)-50,height=90)
            unpaid_lister_child_frame.grid(row=i,column=1,padx=5,pady=3)
            customer_info=fetch_data_by_id("*","customer",customer_name[1])
            customer_equb_info=fetch_data_by_id("*","equb_type",customer_name[2])
            unpaid_lister_child_frame.bind('<Button-1>',partial(display_detailed_information , equb_info=customer_equb_info[1],customer_id=f'{customer_info[0]} / {customer_info[1]} '))
            
            unpaid_photo_label=ttk.Label(unpaid_lister_child_frame)
            unpaid_photo_label.grid(row=1,column=1,rowspan=4,padx=5,pady=3)
            display_profile_picture(customer_info[5],unpaid_photo_label,size=(50,70))
            unpaid_photo_label.bind('<Button-1>',partial(display_detailed_information , equb_info=customer_equb_info[1],customer_id=f'{customer_info[0]} / {customer_info[1]} '))
            
            unpaid_name_label=ttk.Label(unpaid_lister_child_frame,text=f'{customer_info[0]} / {customer_info[1]} ',width=30)
            unpaid_name_label.grid(row=1,column=2,padx=5,pady=3)
            unpaid_name_label.bind('<Button-1>',partial(display_detailed_information , equb_info=customer_equb_info[1],customer_id=f'{customer_info[0]} / {customer_info[1]} '))
            
            unpaid_phone_number_label=ttk.Label(unpaid_lister_child_frame,text=f'{customer_info[2]} ',width=30)
            unpaid_phone_number_label.grid(row=2,column=2,padx=5,pady=3)
            unpaid_phone_number_label.bind('<Button-1>',partial(display_detailed_information , equb_info=customer_equb_info[1],customer_id=f'{customer_info[0]} / {customer_info[1]} '))
            
            unpaid_equb_type_label=ttk.Label(unpaid_lister_child_frame,text=f'{customer_equb_info[1]} ',width=30)
            unpaid_equb_type_label.grid(row=3,column=2,padx=5,pady=3)
            unpaid_equb_type_label.bind('<Button-1>',partial(display_detailed_information , equb_info=customer_equb_info[1],customer_id=f'{customer_info[0]} / {customer_info[1]} '))
            
            unpaid_amount_label=ttk.Label(unpaid_lister_child_frame,text=f'{customer_name[3]} ',width=30)
            unpaid_amount_label.grid(row=4,column=2,padx=5,pady=3)
            unpaid_amount_label.bind('<Button-1>',partial(display_detailed_information , equb_info=customer_equb_info[1],customer_id=f'{customer_info[0]} / {customer_info[1]} '))
            
    enrollment_frame=ttk.Frame(registration_container_frame,width=screen_width*0.25,height=515)
    # enrollment_frame.pack(side=LEFT,anchor='n',padx=25,fill=Y,pady=10)
    
    payment_frame=ttk.Frame(registration_container_frame,width=screen_width*0.25,height=515)
    # payment_frame.pack(side=LEFT,anchor='n',padx=25,fill=Y,pady=10)
    
    profile_picture_frame=ttk.Frame(registration_container_frame,width=screen_width*0.25,height=515)
    # profile_picture_frame.pack(side=LEFT,anchor='n',padx=25,fill=Y,pady=10)
    unpaid_lister_main_frame=Frame(registration_container_frame,width=screen_width*0.25,height=515)
    # unpaid_lister_main_frame.pack(side=LEFT,anchor='n',padx=25,fill=Y,pady=10)
    unpaid_lister_veritca_scroll_bar=ttk.Scrollbar(registration_container_frame,orient=VERTICAL)
    unpaid_lister_veritca_scroll_bar.pack(side='right',fill='y')                                          #    ,command=unpaid_lister_main_frame.yview)
    # unpaid_lister_veritca_scroll_bar.place(relheight=1,relx=0.97,rely=0)
    
    fill_unpaid_lister()
    # unpaid_lister_main_frame.configure(yscrollcommand=unpaid_lister_veritca_scroll_bar.set)

    
    # list_of_customers.configure(yscrollcommand=vsbs.set)
    customer_list_frame=ttk.Frame(main_notebook,width=screen_width,height=515)
    customer_list_frame.pack()
    equb_management_frame=ttk.Frame(main_notebook,width=screen_width,height=515)
    equb_management_frame.pack()
    main_notebook.add(registration_container_frame,text='    ዓሚል መመዝገቢ ፣ መኽፈሊ ቕጥዒ  ')
    main_notebook.add(drawn_container_frame,text='     ዕጫ መውደቕን መመዝገብን    ')
    main_notebook.add(customer_list_frame,text='       ዝርዝር ሓበሬታ      ')
    main_notebook.add(equb_management_frame,text='    መመሓየሺ   ')
#customer information lables *************************************************
    global clear_customer_info_lables
    def clear_customer_info_lables():
        display_profile_picture(default_profile_photo,customer_photo_info_label)
        customer_name_info_label.config(text='')
        customers_selected_equb_label.config(text='')
        selected_equb_reached_round.config(text='')
        have_customer_equb_label.config(text='')
        taken_amount_label.config(text='')
        has_paid_last_round_label.config(text='')
        past_unpaid_status_label.config(text='')
        past_unpaid_round_label.config(text='')
        past_unpaid_amount_label.config(text='')
        current_round_unpaid_quetion_label.config(text='')
        current_round_unpaid_label.config(text='')
        total_paid_amount_till_now_label.config(text='')
        total_punished_amount_label.config(text='')
        total_punished_money_label.config(text='')
    customer_photo_info_label=ttk.Label(profile_picture_frame)
    customer_photo_info_label.grid(row=1,column=1,padx=3,pady=1,sticky='w',rowspan=5)

    customer_name_info_label=ttk.Label(profile_picture_frame,text='',font=('bold',14))
    customer_name_info_label.grid(row=1,column=2,padx=3,pady=1,sticky='w')
    
    customers_selected_equb_label=ttk.Label(profile_picture_frame,text='',font=('bold',14))
    customers_selected_equb_label.grid(row=2,column=2,padx=3,pady=1,sticky='nsew')

    selected_equb_reached_round=ttk.Label(profile_picture_frame,text='',font=('bold',16),foreground='blue')
    selected_equb_reached_round.grid(row=3,column=2,padx=3,pady=1,sticky='w')

    have_customer_equb_label=ttk.Label(profile_picture_frame,text='',font=('bold',14),foreground='blue')
    have_customer_equb_label.grid(row=4,column=2,padx=3,pady=1,sticky='w')

    taken_amount_label=ttk.Label(profile_picture_frame,text='',font=('bold',14))
    taken_amount_label.grid(row=5,column=2,padx=3,pady=1,sticky='w')

    has_paid_last_round_label=ttk.Label(profile_picture_frame,text='',font=('bold',14),foreground='blue')
    has_paid_last_round_label.grid(row=6,column=1,padx=3,pady=1,sticky='w')

    past_unpaid_status_label=ttk.Label(profile_picture_frame,text='',font=('bold',14))
    past_unpaid_status_label.grid(row=7,column=1,padx=3,pady=1,sticky='w')

    past_unpaid_round_label=ttk.Label(profile_picture_frame,text='',font=('bold',14))
    past_unpaid_round_label.grid(row=8,column=1,padx=3,pady=1,sticky='w')

    past_unpaid_amount_label=ttk.Label(profile_picture_frame,text=' ',font=('bold',14))
    past_unpaid_amount_label.grid(row=9,column=1,padx=3,pady=1,sticky='w',columnspan=2)

    current_round_unpaid_quetion_label=ttk.Label(profile_picture_frame,text='',font=('bold',14),foreground='blue')
    current_round_unpaid_quetion_label.grid(row=6,column=2,padx=3,pady=3,sticky='w')

    current_round_unpaid_label=ttk.Label(profile_picture_frame,text='',font=('bold',14))
    current_round_unpaid_label.grid(row=7,column=2,padx=3,pady=3,sticky='w')

    total_paid_amount_till_now_label=ttk.Label(profile_picture_frame,text='',font=('bold',14),foreground='green')
    total_paid_amount_till_now_label.grid(row=10,column=1,padx=3,pady=7,columnspan=2,sticky='w')

    total_punished_amount_label=ttk.Label(profile_picture_frame,text='',font=('bold',14),foreground='green')
    total_punished_amount_label.grid(row=11,column=1,padx=3,pady=3,columnspan=2,sticky='w')

    total_punished_money_label=ttk.Label(profile_picture_frame,text='',font=('bold',14),foreground='green')
    total_punished_money_label.grid(row=12,column=1,padx=3,pady=3,columnspan=2,sticky='w')
    def clear_customer_and_enrollment_frame():
        enrollment_frame.pack_forget()
        registration_frame.pack_forget()
        payment_frame.pack_forget()
        profile_picture_frame.pack_forget()
        clear_customer_info_lables()
        unpaid_lister_main_frame.pack_forget()
    def display_profile_picture_frame():
        profile_picture_frame.pack(side=LEFT,anchor='n',padx=25,fill=Y,pady=10)
        
        # display_profile_picture(default_profile_photo,customer_photo_info_label)
    
    def display_payment_frame():
        clear_customer_and_enrollment_frame()
        unpaid_lister_main_frame.pack(side=LEFT,anchor='n',padx=25,fill=Y,pady=10)
        payment_frame.pack(side=LEFT,anchor='n',padx=25,fill=Y,pady=10)
        display_profile_picture_frame()
        # payment_customer_name_entry.focus()
    def display_register_customer_frame():
        clear_customer_and_enrollment_frame()
        registration_frame.pack(side=LEFT,anchor='n',padx=30,pady=10)
        display_profile_picture_frame()
        # search_customer.focus()
    def display_enrollment_frame():
        clear_customer_and_enrollment_frame()
        enrollment_frame.pack(side=LEFT,anchor='n',padx=25,fill=Y,pady=10)
        display_profile_picture_frame()
        # enrollment_search_entry.focus()
    

#************************************setting form **************************************************
    global profile_frame
    profile_frame=ttk.Frame(equb_management_frame,width=int(screen_width*0.25),height=515)
    if logged_user_role=='super_admin':
        profile_frame.grid(row=0,column=0,padx=20,sticky='n')
    else:
        profile_frame.grid_forget()
    user_profile_photo_frame=ttk.Frame(equb_management_frame,width=int(screen_width*0.25),height=515)
    user_profile_photo_frame.grid(row=0,column=3,padx=20,sticky='n')
    equb_settings_frame=ttk.Frame(equb_management_frame,width=int(screen_width*0.25),height=515)
    equb_settings_frame.grid(row=0,column=1,padx=20,sticky='n')
    
    expire_date_frame=ttk.Frame(equb_management_frame,width=int(screen_width*0.25),height=515)
    
    if logged_user_role=='super_admin':
        expire_date_frame.grid(row=0,column=2,padx=20,pady=30,sticky='n')
    else:
        expire_date_frame.grid_forget()
    user_registration_label=ttk.Label(profile_frame,text='ሰራሕተኛ መመዝገቢ',font=('arial',14,'bold') ,foreground='blue')
    user_registration_label.grid(row=0,column=0,pady=10,padx=5)
    # *********************************************************************************
    def clear_user_registration_notification_label():
        user_registration_notification_label.config(text='')
    def clear_profile_entries():
        # search_user_entry.delete(0,END)
        full_name_entry.delete(0,END)
        register_user_name_entry.delete(0,END)
        user_password_entry.delete(0,END)
        user_profile_photo_entry.delete(0,END)
        # role_entry.set(role[0])
        display_profile_picture(default_profile_photo,user_profile_photo_label)
        user_registration_notification_label.after('3000',clear_user_registration_notification_label)
    global find_all_users_and_fill_list
    def find_all_users_and_fill_list():
        db=sqlite3.connect(database_name)
        cursor=db.cursor()
        cursor.execute(("""select id , full_name
                        from user
                        order by id desc"""))
        result=cursor.fetchall()
        cursor.close()
        db.commit()
        db.close()
        user_account_list.clear()
        if (result ):
            if logged_user_role=='super_admin':

                for i in result:
                    if f"{i[0]} / {i[1]}" not in user_account_list:
                        user_account_list.append(f"{i[0]} / {i[1]}")
                # search_user_entry.config(state='active')
                search_user_entry.config(values=user_account_list)
                # search_user_entry.delete(0,END)
                # search_user_entry.insert(END,logged_user_id)   
            # else :
                # user_account_list.clear()
                # search_user_entry.config(values=user_account_list)
                # search_user_entry.delete(0,END)
                # search_user_entry.insert(END,logged_user_id)
                # search_user_entry.focus()
                # search_user_entry.config(state='disabled')
        else :
            user_account_list.clear()
    def generate_user_name():
        db = sqlite3.connect(database_name)
        cursor = db.cursor()
        cursor.execute("""select count(user_name) from user where full_name=?""",[full_name_entry.get()])
        username=cursor.fetchone()
        company_name=fetch_data("company_name","company_name")[0][0]
        if username :
            if username[0]==0 :
                
                myusername=str(full_name_entry.get())+'@'+'equb'
                register_user_name_entry.delete(0,END)
                register_user_name_entry.insert(END, myusername)
            elif username[0]>0:
                myusername=str(full_name_entry.get())+str(int(username[0]+1))+'@'+'equb'
                register_user_name_entry.delete(0,END)
                register_user_name_entry.insert(END, myusername)
        
        db.commit()
        db.close()
    def generate_user_name_event(event):
        generate_user_name()
    def find_and_fill_user_entries():
        clear_profile_entries()
        user_info=fetch_data_by_id('*','user',(search_user_entry.get()).split('/')[0])
        
        if user_info:
            full_name_entry.insert(END,user_info[1])
            register_user_name_entry.insert(END,user_info[2])
            # user_password_entry.insert(END,user_info[3])
            role_entry.set(user_info[4])
            
            if user_info[5]!=None:
                user_profile_photo_entry.insert(END,user_info[5])
                display_profile_picture(user_info[5],user_profile_photo_label)
            else:
                display_profile_picture(default_profile_photo,user_profile_photo_label)
    def find_and_fill_user_entries_event(event):
        find_and_fill_user_entries()

    def create_profile():
        encrypted_password=bcrypt.hashpw(user_password_entry.get().encode('utf-8'), bcrypt.gensalt())
        db = sqlite3.connect(database_name)
        cursor = db.cursor()
        cursor.execute(('insert into user (full_name,user_name,password,role,photo) values (?,?,?,?,?)'),
                       (full_name_entry.get(),
                        register_user_name_entry.get(),
                        encrypted_password,
                        role_entry.get(),
                        user_profile_photo_entry.get()
                        ))
        
        db.commit()
        db.close()
        user_registration_notification_label.config(text='user registerd',foreground='green')
        clear_profile_entries()
        find_all_users_and_fill_list()
    def update_profile():
        if logged_user_role=='super_admin':
            user_id=search_user_entry.get().split('/')[0]
            users_role=role_entry.get()
        else:
            user_id=logged_user_id
            users_role=logged_user_role
        encrypted_password=bcrypt.hashpw(user_password_entry.get().encode('utf-8'), bcrypt.gensalt())
        db = sqlite3.connect(database_name)
        cursor = db.cursor()
        cursor.execute(('update user set full_name=?,user_name=?,password=?,role=?,photo=? where id=?'),
                       (full_name_entry.get(),
                        register_user_name_entry.get(),
                        encrypted_password,
                        users_role,
                        user_profile_photo_entry.get(),
                        user_id
                        ))
        
        db.commit()
        db.close()
        user_registration_notification_label.config(text='user updated',foreground='black')
        
        if int(user_id)==int(logged_user_id):
            display_logged_user_profile_picture(user_profile_photo_entry.get(),logged_profile_photo_label)
        
        clear_profile_entries()
        if logged_user_role!='super_admin':
            profile_frame.grid_forget()
            display_profile_picture(default_profile_photo,user_profile_photo_label)
        find_all_users_and_fill_list()
    def remove_profile():
        db = sqlite3.connect(database_name)
        cursor = db.cursor()
        cursor.execute(('delete from user where id=?'),
                       [
                        search_user_entry.get().split('/')[0]
                        ])
        
        db.commit()
        db.close()
        user_registration_notification_label.config(text='user deleted',foreground='black')
        clear_profile_entries()
        find_all_users_and_fill_list()
    search_user_label=ttk.Label(profile_frame,image=search_photo)
    global search_user_entry
    search_user_entry=ttk.Combobox(profile_frame,width=22,values=user_account_list)
    
    search_user_entry.bind('<Down>',lambda e:full_name_entry.focus())
    search_user_entry.bind('<KeyRelease>',find_and_fill_user_entries_event)
    search_user_entry.bind('<FocusIn>',find_and_fill_user_entries_event)
    find_all_users_and_fill_list()
    global full_name_entry
    full_name_label=ttk.Label(profile_frame,text='ሙሉእ ሽም')
    full_name_label.grid(row=2,column=0,sticky='w',padx=5,pady=5)
    full_name_entry=ttk.Entry(profile_frame,width=30)
    full_name_entry.grid(row=3,column=0,sticky='e',padx=5,pady=5)
    full_name_entry.bind('<Up>',lambda e:search_user_entry.focus())
    full_name_entry.bind('<Down>',lambda e:register_user_name_entry.focus())
    
    # full_name_entry.focus()
    # full_name_entry.bind('<KeyRelease>',generate_user_name_event)
    # full_name_entry.bind('<FocusIn>',generate_user_name_event)
    global register_user_name_entry
    register_user_name_label=ttk.Label(profile_frame,text='መጥቀሚ ሽም')
    register_user_name_label.grid(row=4,column=0,sticky='w',padx=5,pady=5)
    register_user_name_entry=ttk.Entry(profile_frame,width=22)
    register_user_name_entry.grid(row=5,column=0,sticky='w',padx=5,pady=5)
    register_user_name_entry.bind('<Up>',lambda e:full_name_entry.focus())
    register_user_name_entry.bind('<Down>',lambda e:user_password_entry.focus())
    
    fill_user_name_button=ttk.Button(profile_frame,width=5,text='🔍',command=generate_user_name)
    fill_user_name_button.grid(row=5,column=0,padx=2,pady=5,sticky='e')
    user_password_label=ttk.Label(profile_frame,text='መሕለፊ ቃል')
    user_password_label.grid(row=6,column=0,sticky='w',padx=5,pady=5)
    user_password_entry=ttk.Entry(profile_frame,width=30,show='*')
    user_password_entry.grid(row=7,column=0,sticky='e',padx=5,pady=5)
    user_password_entry.bind('<Up>',lambda e:register_user_name_entry.focus())
    user_password_entry.bind('<Down>',lambda e:role_entry.focus())
    role_label=ttk.Label(profile_frame,text='ሓላፍነት')
    global role_entry
    role_entry=ttk.Combobox(profile_frame,width=28)
    
    
    role_entry.bind('<Up>',lambda e:user_password_entry.focus())
    role_entry.bind('<Down>',lambda e:choose_photo_button.focus())
    select_photo_label=ttk.Label(profile_frame,text='ስእሊ ')
    select_photo_label.grid(row=10,column=0,sticky='w',padx=5,pady=5)
    def choose_profile_picture():
        selected_profile_photo=filedialog.askopenfilename(filetypes=[("select photo", "*.png;*.jpg;*.jpeg")])
        # filedialog.askopenfilename(title='ስእሊ ምረፅ')
        destination = './image/profile/'
        source=selected_profile_photo
        if source:
            
            user_profile_picture = './image/profile/' + str((selected_profile_photo.split('/')[-1]))
            
            try:
                shutil.copy(source, destination)
            except:
                pass
            user_profile_photo_entry.delete(0,END)
            user_profile_photo_entry.insert(END,user_profile_picture)
            display_profile_picture(user_profile_picture,user_profile_photo_label)
    
    choose_photo_button=ttk.Button(profile_frame,width=12,command=choose_profile_picture,text='browse')
    choose_photo_button.grid(row=11,column=0,sticky='e',padx=2,pady=5)
    global user_profile_photo_entry
    user_profile_photo_entry=ttk.Entry(profile_frame,width=16)
    user_profile_photo_entry.grid(row=11,column=0,sticky='w',padx=2,pady=5)
    
    save_user_button=ttk.Button(profile_frame,width=8,command=create_profile,text='መዝግብ')
    
    
    update_user_button=ttk.Button(profile_frame,width=8,command=update_profile,text='ኣመሓይሽ',style='update.TButton')
    update_user_button.grid(row=12,column=0,padx=2,pady=5)
    
    delete_user_button=ttk.Button(profile_frame,width=8,command=remove_profile,style='delete.TButton',text='ደምስስ')
    
    global user_profile_photo_label
    user_profile_photo_label=ttk.Label(user_profile_photo_frame)
    user_profile_photo_label.grid(row=1,column=0,sticky='w',padx=2,pady=10)
    
    
    user_registration_notification_label=ttk.Label(profile_frame,text='')
    user_registration_notification_label.grid(row=13,column=0,padx=5,pady=5)
    
    if logged_user_role=='super_admin':
        
        role_label.grid(row=8,column=0,sticky='w',padx=5,pady=5)
        role_entry.grid(row=9,column=0,sticky='e',padx=5,pady=5)
        role_entry.config(values=role)
        role_entry.set(role[0])
        search_user_label.grid(row=1,column=0,sticky='e',padx=5,pady=5)
        search_user_entry.grid(row=1,column=0,sticky='w',padx=5,pady=5)
        save_user_button.grid(row=12,column=0,sticky='w',padx=2,pady=5)
        delete_user_button.grid(row=12,column=0,sticky='e',padx=2,pady=5)
        update_user_button.config(width=8)
    else :
        
        search_user_label.grid_forget()
        search_user_entry.grid_forget()
        role_label.grid_forget()
        role_entry.grid_forget()
        save_user_button.grid_forget()
        delete_user_button.grid_forget()
        update_user_button.config(width=30)
    #***************************************equb settings ******************************
    
    def clear_equb_registration_entries():
        equb_id_entry.delete(0,END)
        equb_name_entry.delete(0,END)
        equb_types_entry.set(equb_type_list[0])
        equb_amount_of_money_entry.delete(0,END)
        # total_members_entry.delete(0,END)
        time_entry.delete(0,END)
        total_members_entry.delete(0,END)
        # state_entry.delete(0,END)
        # state_entry.set(equb_state[0])
    def clear_equb_registration_label():
        equb_registration_notfication_label.config(text='')
    def  fill_equb_registration_entries():
        clear_equb_registration_entries()
        
    def fill_equb_registration_entries_event(event):
        fill_equb_registration_entries()
        check_equb_qualification()
        eid=search_equb_entry.get().split('/')[0]
        equb_info=fetch_data_by_id('*','equb_type',eid)
        if equb_info:
            registered_equb_type=equb_info[1].split('-')[-1]
            registered_equb_name=equb_info[1].split('-')[0]
            equb_id_entry.insert(END,equb_info[0])
            equb_name_entry.insert(END,registered_equb_name)
            equb_types_entry.set(registered_equb_type)
            equb_amount_of_money_entry.insert(END,equb_info[2])
            total_members_entry.insert(END,equb_info[4])
            time_entry.insert(END,equb_info[3])
        # state_entry.set(equb_info[5])
        
    def create_equb():
        equb_name_and_type=f'{equb_name_entry.get()}-{equb_types_entry.get()}'
        db = sqlite3.connect(database_name)
        cursor = db.cursor()
        cursor.execute("""insert into equb_type (id,equb_type,amount_of_money,time,total_round) values (?,?,?,?,?)""",
                       (
                        equb_id_entry.get(),
                        equb_name_and_type,
                        equb_amount_of_money_entry.get(),
                        
                        time_entry.get(),
                        total_members_entry.get()
        
        ))
        cursor.execute("""insert into round (equb_type_id,current_round) values (?,'1')""",
                       (
                        equb_id_entry.get()
                        
        
        ))
        
        cursor.close()
        db.commit()
        db.close()
        equb_registration_notfication_label.config(text='ዕቑብ ብትክክል ተመዝጊቡ',foreground='green',font=('bold',14))
        equb_registration_notfication_label.after('3000',clear_equb_registration_label)
        clear_equb_registration_entries()
        
        fill_type_list()
        refresh_combo ()
        refresh_table_list()
        fill_table_equb_type()
        fill_available_equb()
        search_equb_entry.delete(0,END)
        search_equb_entry.set(available_equb[-1])
    def update_equb():
        equb_name_and_type=f'{equb_name_entry.get()}-{equb_types_entry.get()}'
        db = sqlite3.connect(database_name)
        cursor = db.cursor()
        cursor.execute("""update equb_type  set equb_type=?,amount_of_money=?,time=?,total_round=? where id=? """,
                       (
                        equb_name_and_type,
                        equb_amount_of_money_entry.get(),
                        
                        time_entry.get(),
                        total_members_entry.get(),
                        search_equb_entry.get().split('/')[0]
        ))
        
        cursor.close()
        db.commit()
        db.close()
        equb_registration_notfication_label.config(text='ዕቑብ ብትክክል ተመሓይሹ',foreground='green',font=('bold',14))
        equb_registration_notfication_label.after('3000',clear_equb_registration_label)
        clear_equb_registration_entries()
        
        fill_type_list()
        refresh_combo ()
        refresh_table_list()
        fill_table_equb_type()
        fill_available_equb()
        search_equb_entry.delete(0,END)
        search_equb_entry.set(available_equb[-1])
    def finish_equb():
        equb_name_and_type=f'{equb_name_entry.get()}-{equb_types_entry.get()}'
        db = sqlite3.connect(database_name)
        cursor = db.cursor()
        
        cursor.execute("""insert into pay_list_history (id,customer_id,equb_type_id,amount,number_of_paid_lot,paid_round,paid_date) 
                        select id,customer_id,equb_type_id,amount,number_of_paid_lot,paid_round,paid_date from pay_list where equb_type_id=? """,
                       [equb_id_entry.get()]
                        )
        
        cursor.execute("""insert into drawn_list_history (id,customer_id,equb_type_id,drawn_date,amount_of_money,warrant_id,drawn_round,drawn_tax)
                       select id,customer_id,equb_type_id,drawn_date,amount_of_money,warrant_id,drawn_round,drawn_tax from drawn_list where drawn_list.equb_type_id=? """,
                        [
                        equb_id_entry.get()])
        cursor.execute("""insert into equb_enrollment_history (id,customer_id,equb_type,amount,number_of_paid_lot,paid_date,reg_number_of_paid_lot) 
                       select id,customer_id,equb_type,amount,number_of_paid_lot,paid_date,reg_number_of_paid_lot from equb_enrollment where equb_enrollment.equb_type=? """,
                        [
                        equb_id_entry.get()])
        cursor.execute(""" update round set current_round=1 where equb_type_id=? """,
                        (
                        equb_id_entry.get()))
        cursor.execute("delete  from pay_list where equb_type_id=?",[equb_id_entry.get()])
        cursor.execute("delete  from equb_enrollment where equb_type=?",[equb_id_entry.get()])
        cursor.execute("delete  from drawn_list where equb_type_id=?",[equb_id_entry.get()])
        cursor.close()
        db.commit()
        db.close()
        equb_registration_notfication_label.config(text='ዕቁብ ተወዲኡ !',foreground='red')
        equb_registration_notfication_label.after('3000',clear_equb_registration_label)
        clear_equb_registration_entries()
        fill_type_list()
        refresh_combo ()
        refresh_table_list()
        fill_table_equb_type()
        fill_available_equb()
    def remove_equb():
        
        db = sqlite3.connect(database_name)
        cursor = db.cursor()
        cursor.execute("delete  from equb_type where id=?",(search_equb_entry.get().split('/')[0]))
        cursor.execute("delete  from pay_list where equb_type_id=?",(search_equb_entry.get().split('/')[0]))
        cursor.execute("delete  from drawn_list where equb_type_id=?",(search_equb_entry.get().split('/')[0]))
        cursor.execute("delete  from round where equb_type_id=?",(search_equb_entry.get().split('/')[0]))
        cursor.execute("delete  from equb_enrollment where equb_type=?",(search_equb_entry.get().split('/')[0]))
        cursor.close()
        db.commit()
        db.close()
        equb_registration_notfication_label.config(text='ዕቑብ ብትክክል ተደምሲሱ !',foreground='red',font=('bold',14))
        equb_registration_notfication_label.after('3000',clear_equb_registration_label)
        clear_equb_registration_entries()
        fill_type_list()
        refresh_combo ()
        refresh_table_list()
        fill_table_equb_type()
        fill_available_equb()
        search_equb_entry.delete(0,END)
        search_equb_entry.set(available_equb[-1])
    def fill_types_list():
        result=fetch_data('*','equb_types')
        equb_type_list.clear()
        if result:
            for i in result:
                equb_type_list.append(i[1])
            equb_types_entry.config(values=equb_type_list)
            equb_types_entry.set(equb_type_list[1])
    def fill_equb_id_entry(event):
        db=sqlite3.connect(database_name)
        cursor=db.cursor()
        cursor.execute('select count(id) from equb_type')
        last_equb_id=cursor.fetchall()
        
        if last_equb_id:
            equb_id_entry.delete(0,END)
            equb_id_entry.insert(END,int(last_equb_id[0][0])+1)
        
        cursor.close()
        db.commit()
        db.close()
    available_equb=[] 
    def fill_available_equb():
        available_equb_result=fetch_data("*", "equb_type")
        available_equb.clear()
        for i in available_equb_result:
            ids=str(i[0])
            name=str(i[1])
            available_equb.append(f'{ids}/{name}')
            search_equb_entry.config(values=available_equb)
            
    equb_label=ttk.Label(equb_settings_frame,text='ዕቑብ መመዝገቢ',font=('arial',14,'bold') ,foreground='blue')
    equb_label.grid(row=0,column=0,sticky='w',padx=5,pady=5)
    # search_photo=PhotoImage(file='./image/search.png')
    search_equb_label=ttk.Label(equb_settings_frame,image=search_photo)
    search_equb_label.grid(row=1,column=0,sticky='e',padx=5,pady=5)
    search_equb_entry=ttk.Combobox(equb_settings_frame,width=21,values=available_equb)
    search_equb_entry.grid(row=1,column=0,sticky='w',padx=5,pady=5)
    search_equb_entry.bind('<Down>',lambda e:equb_id_entry.focus())
    search_equb_entry.bind('<KeyRelease>',fill_equb_registration_entries_event)
    search_equb_entry.bind('<FocusIn>',fill_equb_registration_entries_event)
    fill_available_equb()
    equb_id_label=ttk.Label(equb_settings_frame,text='መለለዪ ቁፅሪ')
    equb_id_label.grid(row=2,column=0,sticky='w',padx=5,pady=5)
    equb_id_entry=ttk.Entry(equb_settings_frame,width=30)
    equb_id_entry.grid(row=3,column=0,sticky='e',padx=5,pady=5)
    equb_id_entry.bind('<Up>',lambda e:search_equb_entry.focus())
    equb_id_entry.bind('<Down>',lambda e:equb_name_entry.focus())
    equb_id_entry.bind('<FocusIn>',fill_equb_id_entry)
    
    equb_name_label=ttk.Label(equb_settings_frame,text='ሽም ዕቁብ')
    equb_name_label.grid(row=4,column=0,sticky='w',padx=5,pady=5)
    equb_name_entry=ttk.Entry(equb_settings_frame,width=30)
    equb_name_entry.grid(row=5,column=0,sticky='e',padx=5,pady=5)
    equb_name_entry.bind('<Up>',lambda e:equb_id_entry.focus())
    equb_name_entry.bind('<Down>',lambda e:equb_types_entry.focus())
    
    equb_types_label=ttk.Label(equb_settings_frame,text='ዓይነት ዕቁብ')
    equb_types_label.grid(row=6,column=0,sticky='w',padx=5,pady=5)
    equb_types_entry=ttk.Combobox(equb_settings_frame,width=27,values=equb_type_list)
    equb_types_entry.grid(row=7,column=0,sticky='e',padx=5,pady=5)
    equb_types_entry.bind('<Up>',lambda e:equb_name_entry.focus())
    equb_types_entry.bind('<Down>',lambda e:equb_amount_of_money_entry.focus())
    fill_types_list()
    equb_amount_of_money_label=ttk.Label(equb_settings_frame,text='መጠን ገንዘብ')
    equb_amount_of_money_label.grid(row=8,column=0,sticky='w',padx=5,pady=5)
    equb_amount_of_money_entry=ttk.Entry(equb_settings_frame,width=30)
    equb_amount_of_money_entry.grid(row=9,column=0,sticky='e',padx=5,pady=5)
    equb_amount_of_money_entry.bind('<Up>',lambda e:equb_name_entry.focus())
    equb_amount_of_money_entry.bind('<Down>',lambda e:total_members_entry.focus())
    
    total_members_label=ttk.Label(equb_settings_frame,text='በዝሒ ዙር / ኣባላት')
    total_members_label.grid(row=10,column=0,sticky='w',padx=5,pady=5)
    total_members_entry=ttk.Entry(equb_settings_frame,width=30)
    total_members_entry.grid(row=11,column=0,sticky='e',padx=5,pady=5)
    total_members_entry.bind('<Up>',lambda e:equb_amount_of_money_entry.focus())
    total_members_entry.bind('<Down>',lambda e:time_entry.focus())
    
    time_label=ttk.Label(equb_settings_frame,text='ዕጫ ዝወድቀሉ ሰዓት  ')
    time_label.grid(row=12,column=0,sticky='w',padx=5,pady=5)
    time_entry=ttk.Entry(equb_settings_frame,width=30)
    time_entry.grid(row=13,column=0,sticky='e',padx=5,pady=5)
    
    time_entry.bind('<Up>',lambda e:total_members_entry.focus())
    # tax_entry.bind('<Down>',lambda e:choose_photo_button.focus())
    # state_label=ttk.Label(equb_settings_frame,text='current state')
    # state_label.grid(row=12,column=0,sticky='w',padx=5,pady=5)
    # state_entry=ttk.Combobox(equb_settings_frame,width=28,values=equb_state)
    # state_entry.grid(row=13,column=0,sticky='w',padx=5,pady=5)
    # state_entry.set(equb_state[0])
    save_equb_button=ttk.Button(equb_settings_frame,width=8,command=create_equb,text='መዝግብ')
    
    
    update_equb_button=ttk.Button(equb_settings_frame,width=8,command=update_equb,text='ኣመሓይሽ',style='update.TButton')
    
    
    delete_equb_button=ttk.Button(equb_settings_frame,width=8,command=remove_equb,style='delete.TButton',text='ደምስስ')
    
    equb_finished_button=ttk.Button(equb_settings_frame,width=30,command=finish_equb,text='ዕቁብ ተወዲኡ')
    equb_finished_button.grid(row=15,column=0,sticky='w',padx=2,pady=5)
    equb_registration_notfication_label=ttk.Label(equb_settings_frame,text='')
    equb_registration_notfication_label.grid(row=16,column=0,padx=5,pady=1)
    def check_equb_qualification():

        if len(search_equb_entry.get())==0:
            save_equb_button.config(width=30)
            save_equb_button.grid(row=14,column=0,sticky='w',padx=2,pady=5)
            update_equb_button.grid_forget()
            delete_equb_button.grid_forget()
        else:
            save_equb_button.grid_forget()
            update_equb_button.config(width=14)
            update_equb_button.grid(row=14,column=0,padx=2,sticky='w',pady=5)
            delete_equb_button.config(width=14)
            delete_equb_button.grid(row=14,column=0,sticky='e',padx=2,pady=5)
    check_equb_qualification()
    # ********************************* expiry date ************************************************
    def fetch_expiry_date():
        expire_date_length=fetch_data('length','expiry_date')[0]
        expire_date_entry.delete(0,END)
        expire_date_entry.insert(END,expire_date_length)
    
    
    def update_expire_date():
        db = sqlite3.connect(database_name)
        cursor = db.cursor()
        cursor.execute("update expiry_date set length=?",[expire_date_entry.get()])
        cursor.close()
        db.commit()
        db.close()
    def update_company_name():
        db = sqlite3.connect(database_name)
        cursor = db.cursor()
        cursor.execute("update company_name set company_name=?",[company_name_entry.get()])
        cursor.close()
        db.commit()
        db.close()
        # title_label.config(text='')
        # title_label.config(text=company_name_entry.get())
    expire_date_label=ttk.Label(expire_date_frame,text='ኣገልግሎት ግዘ')
    expire_date_label.grid(row=0,column=0, padx=30, pady=5,sticky='w')
    expire_date_entry=ttk.Combobox(expire_date_frame,values=expire_date_list,width=28)
    expire_date_entry.grid(row=1,column=0, padx=30, pady=5)
    # expire_date_entry.set(expire_date_list[0])
    expire_date_update_button=ttk.Button(expire_date_frame,text='ኣመሓይሽ ',style='update.TButton',width=30,command=update_expire_date)
    expire_date_update_button.grid(row=2,column=0, padx=30, pady=5)
    fetch_expiry_date()
    company_name_label=ttk.Label(expire_date_frame,text='ናይ ድርጅት ሽም')
    company_name_label.grid(row=3,column=0, padx=30, pady=5,sticky='w')
    company_name_entry=ttk.Entry(expire_date_frame,width=30)
    company_name_entry.grid(row=4,column=0, padx=30, pady=5)
    company_name_entry.delete(0,END)
    company_name_entry.insert(END,company_name)
    company_name_update_button=ttk.Button(expire_date_frame,text='ሽም ኣመሓይሽ',style='update.TButton',width=30,command=update_company_name)
    company_name_update_button.grid(row=5,column=0, padx=30, pady=5)
#******************************************register form********************************************
    def fill_id_event(event):
        fill_id()
    def fill_id():
        customer_id=fetch_data('max(id)','customer')
        if customer_id[0][0]!= None:
            
            id_entry.delete(0,END)
            id_entry.insert(END,int(customer_id[0][0])+1)
        else:
            id_entry.delete(0,END)
            id_entry.insert(END,1)
    all_customer_names=[]
    def fill_customer_names():
        all_names=fetch_data('customer_name','customer')
        all_customer_names.clear()
        
        for i in all_names:
            all_customer_names.append(f'{i[0]}')
        name_entry.config(values=all_customer_names)
    def fill_customer_name_like(event):
        all_names=fetch_data_like('customer_name','customer','customer_name',str(name_entry.get()))
        all_customer_names.clear()
        for i in all_names:
            all_customer_names.append(i)
        name_entry.config(values=all_customer_names)
    regitration_title=ttk.Label(registration_frame,text='ሓድሽ ዓሚል መመዝገቢ',font=('arial',14,'bold') ,foreground='blue')
    regitration_title.grid(row=0,column=0,padx=3,pady=5,sticky='w')
    
    # search_photos=PhotoImage(file='./image/search.png')
    search_label=ttk.Label(registration_frame,image=search_photo)
    search_label.grid(row=1,column=0,padx=3,pady=5,sticky='e')
    search_customer=ttk.Entry(registration_frame,width=30)
    search_customer.grid(row=1,column=0,padx=3,pady=10,sticky='w')
    search_customer.bind('<KeyRelease>',search_customer_and_fill_event)
    search_customer.bind('<FocusIn>',search_customer_and_fill_event)
    
    
    id_label=ttk.Label(registration_frame,text='መለለዪ ቁፅሪ')
    id_label.grid(row=3,column=0,padx=3,pady=2,sticky='w')
    id_entry=ttk.Entry(registration_frame,width=35)
    id_entry.grid(row=4,column=0,padx=3,pady=2,sticky='w')
    id_entry.bind('<FocusIn>',lambda e: fill_id())
    # fill_id_button=ttk.Button(registration_frame,width=20,text='መለለዪ ስርሓለይ',command=fill_id)
    # fill_id_button.grid(row=4,column=0,padx=3,pady=2,sticky='e')
    fill_id()
    # def name_event(event):
    #      cutomer_name_info.config(text=name_entry.get())
    global name_entry
    name_label=ttk.Label(registration_frame,text='ሙሉእ ሽም')
    name_label.grid(row=5,column=0,padx=3,pady=2,sticky='w')
    name_entry=ttk.Combobox(registration_frame,width=32,values=all_customer_names)
    name_entry.grid(row=6,column=0,padx=3,pady=2)
    name_entry.bind('<Up>',lambda e: search_customer.focus())
    name_entry.bind('<Down>',lambda e: phone_number_entry.focus())
    fill_customer_names()
    name_entry.bind('<KeyRelease>',fill_customer_name_like)
    phone_number_label=ttk.Label(registration_frame,text='ስልኪ ቁፅሪ')
    phone_number_label.grid(row=7,column=0,padx=3,pady=2,sticky='w')
    phone_number_entry=ttk.Entry(registration_frame,width=35)
    phone_number_entry.grid(row=8,column=0,padx=3,pady=2)
    phone_number_entry.bind('<Up>',lambda e:name_entry.focus())
    phone_number_entry.bind('<Down>',lambda e:customer_adress_entry.focus())
    # phone_number_entry.bind("<KeyRelease>",lambda  e: (cutomer_mobile_info.config(text=phone_number_entry.get())))
    
        # cutomer_date_info.config(text='')
        # cutomer_date_info.config(text=clock)
    customer_adress_label=ttk.Label(registration_frame,text='ኣድራሻ')
    customer_adress_label.grid(row=9,column=0,padx=3,pady=2,sticky='w')
    customer_adress_entry=ttk.Entry(registration_frame,width=35)
    customer_adress_entry.grid(row=10,column=0,padx=3,pady=2)
    customer_adress_entry.bind('<Up>',lambda e:phone_number_entry.focus())
    date_label=ttk.Label(registration_frame,text='ዝተመዝገበሉ ዕለት')
    date_label.grid(row=11,column=0,padx=3,pady=2,sticky='w')
    date_entry=ttk.Entry(registration_frame,width=30)
    date_entry.grid(row=12,column=0,padx=3,pady=2,sticky='w')
    fill_date(date_entry)
    
    fill_date_button=ttk.Button(registration_frame,text='⏱️',width=3,command=lambda : fill_date(date_entry))
    fill_date_button.grid(row=12,column=0,padx=3,pady=2,sticky='e')


    def select_photo():
        destination = './image/profile/'
        source = filedialog.askopenfilename(filetypes=[("ናይ ዓሚል ፎቶ ምረፅ", "*.png;*.jpg;*.jpeg")])
    
        if source:
            profile_photo_name.clear()
            profile_photo_name.append(source)
            profile_picture = './image/profile/' + str((profile_photo_name[0].split('/'))[-1])
            try:
                shutil.copy(source, destination)
                photo_entry.delete(0,END)
                photo_entry.insert(END,profile_picture)
                # customer_photo=PhotoImage(file=f'{profile_picture}')
                display_profile_picture(profile_picture,customer_photo_info_label)
            except:
                pass
            # customer_photo_info_label.grid_forget()
            #customer_photo_info_label.config(image=customer_photo)
    def profile_to_pdf():
        try:
            if company_name and len(id_entry.get())>0  and len(name_entry.get())>0 and  len(phone_number_entry.get())>0 and  len(photo_entry.get())>0:
                create_pdf(company_name, id_entry.get(), name_entry.get(), phone_number_entry.get(), photo_entry.get())
                pdf_source='./badge.pdf'
                saved_file_name=(str(name_entry.get())+'.pdf')
                pdf_destination=filedialog.askdirectory()
                joined_path=os.path.join(pdf_destination,saved_file_name)
                if pdf_source and pdf_destination:
                    shutil.copy(pdf_source, joined_path)
                    # filedialog.showinfo('success','መለለዪ ብትክክል ተመዝጊቡ')
                        
        except:
            pass
    photo_label = ttk.Label(registration_frame, text='ስእሊ ዓሚል  ምረፅ:')
    photo_label.grid(row=13, column=0, padx=3, pady=2, sticky='w')

    photo_entry = ttk.Entry(registration_frame, width=23)
    photo_entry.grid(row=14, column=0, padx=3, pady=2, sticky='w')
    
    browse_button=ttk.Button(registration_frame, width=10, text='ስእሊ ኣልሽ', command=select_photo)
    browse_button.grid(row=14, column=0, padx=3, pady=2, sticky='e')

    information_label=ttk.Label(registration_frame,text='')
    information_label.grid(row=15,column=0,padx=3,pady=2,sticky='w')
    
    register_button=ttk.Button(registration_frame,width=10,text='መዝግብ',command=register_customer,style='save.TButton')
    
    
    update_button=ttk.Button(registration_frame,width=10,text='ኣመሓይሽ',style='update.TButton',command=update_customer)
    
    
    delete_button=ttk.Button(registration_frame,width=10,text='ኣጥፍእ',style='delete.TButton',command=delete_customer)
    
   
    register_next_button=ttk.Button(registration_frame,width=10,text=' ቀፅል >>',command=display_enrollment_frame)
    register_next_button.grid(row=17,column=0,padx=3,pady=12,sticky='e')

    register_back_button=ttk.Button(registration_frame,width=10,text=' << ተመለስ ',command=display_payment_frame)
    register_back_button.grid(row=17,column=0,padx=3,pady=12,sticky='w')
    # print_button=ttk.Button(registration_frame,width=35,text='መለለዪ ኣሕትም',style='save.TButton',command=profile_to_pdf)
    # print_button.grid(row=15,column=0,padx=3,pady=2,sticky='e')
    # global customer_photo_info_label
    global check_cusotmer_modification
    def check_cusotmer_modification():
        if len(search_customer.get())>0:
            delete_button.config(width=16)
            delete_button.grid(row=16,column=0,padx=3,pady=2,sticky='e')
            update_button.config(width=16)
            update_button.grid(row=16,column=0,padx=3,pady=2,sticky='w')
            register_button.grid_forget()
        else:

            delete_button.grid_forget()
            update_button.grid_forget()
            register_button.config(width=35)
            register_button.grid(row=16,column=0,padx=2,pady=2,sticky='w')
    check_cusotmer_modification()
#******************************************enrollment******************************
    def find_and_fill_enrollment_entries(event):
        check_enrollment()
        find_and_fill_enrollment_entries_after()
    def find_and_fill_enrollment_entries_after():
        try:
            db=sqlite3.connect(database_name)
            cursor=db.cursor()
            cursor.execute(("""select customer.customer_name ,equb_type.equb_type,amount,
                            reg_number_of_paid_lot,paid_date,customer.photo,
                            equb_enrollment.customer_id
                            from equb_enrollment 
                            JOIN customer ON equb_enrollment.customer_id=customer.id 
                            JOIN equb_type ON equb_enrollment.equb_type=equb_type.id
                            where equb_enrollment.id=?"""),([enrollment_search_entry.get()]))
            result=cursor.fetchone()
            cursor.close()
            db.commit()
            db.close()
            
            clear_enrollment_entries()
            
            if result:
                customer_name_entry.insert(END, f'{result[6]} / {result[0]}')
                equb_type_entry.insert(END,result[1])
                amount_entry.insert(END,result[2])
                # no_lot_entry.insert(END,result[3])
                enrollment_date_entry.insert(END,result[4])
                total_label_info.config(text='')
                total_label_info.config(text=(float(result[2])*int(result[3])))
                display_profile_picture(result[5],customer_photo_info_label)
            else:
                total_label_info.config(text='')
                display_profile_picture(default_profile_photo,customer_photo_info_label)
            # print(float(result[2])*int(result[3]))
            # clear_enrollment_entries()
        except:
            pass    
    def fill_type_list():
        result=fetch_data('*','equb_type')
        equb_type.clear()
        if result:
            for i in result:
                equb_type.append(i[1])
            equb_type_entry.config(values=equb_type)
            equb_type_entry.delete(0,END)
            equb_type_entry.insert(END,equb_type[0])
    def fill_enrollment_customer_photo():
        
        customers_photo=fetch_data_by_id('photo','customer',customer_name_entry.get().split('/')[0])
        
        if customers_photo:
            display_profile_picture(customers_photo[0],customer_photo_info_label)
        else:
            display_profile_picture(default_profile_photo,customer_photo_info_label)
    def fill_customer_list_like():
        try:
            db=sqlite3.connect(database_name)
            cursor=db.cursor()
            cursor.execute("select * from customer where customer_name like '%"+customer_name_entry.get()+"%' or id=? order by id desc",[customer_name_entry.get()])
            result=cursor.fetchall()
            cursor.close()
            db.commit()
            db.close()
            customer_list.clear()
            if result:
                for i in result:
                    if f"{i[0]} / {i[1]}" not in customer_list:
                        customer_list.append(f"{i[0]} / {i[1]}")
                    #customer_list.append([i[0],'/',i[1]])
                
                fill_enrollment_customer_photo()
                customer_name_entry.config(values=customer_list)
            
            # fill_amount()
            # fill_type_list()
        except:
            pass
    def fill_customer_list():  
        try:  
            result=fetch_data('*','customer')
            customer_list.clear()
            if result:
                for i in result:
                    if f"{i[0]} / {i[1]}" not in customer_list:
                        customer_list.append(f"{i[0]} / {i[1]}")
                    #customer_list.append([i[0],'/',i[1]])
                
                customer_name_entry.config(values=customer_list)
                customer_name_entry.delete(0,END)
                customer_name_entry.insert(END,customer_list[0])
            else:
                customer_list.clear()
                customer_name_entry.config(values=customer_list)
        except:
            pass
    def fill_amount(event):
        try:
            db=sqlite3.connect(database_name)
            cursor=db.cursor()
            cursor.execute(('select amount_of_money from equb_type where equb_type=?'),[(equb_type_entry.get())])
            result=cursor.fetchone()
            cursor.close()
            db.commit()
            db.close()
            # total_label_info.config(text='')
            if result:
                amount_entry.delete(0,END)
                amount_entry.insert(END,result)
                # total_price()
        except:
            pass
    def refresh_combo ():
        fill_type_list()
        fill_customer_list()
    def clear_total_label():
        total_label.config(text='')
        total_label_info.config(text='')
    def clear_enrollment_entries():
        customer_name_entry.delete(0,END),
        equb_type_entry.delete(0,END),
        amount_entry.delete(0,END),
        # no_lot_entry.delete(0,END),
        enrollment_date_entry.delete(0,END)
    def clear_enrollment():
        clear_enrollment_entries()
        total_label.config(text='')
        total_label_info.config(text='ኣብ ማህደር ሰፊሩ')
        total_label.after('3000',clear_total_label)
        total_label_info.after('3000',clear_total_label)
    
    def register_enrollment():
        try:
            customer_id=(customer_name_entry.get()).split('/')[0]
            db=sqlite3.connect(database_name)
            cursor=db.cursor()
            cursor.execute('select id from equb_type where equb_type=?',[equb_type_entry.get()])
            equb_id=cursor.fetchall()
            cursor.execute('insert into equb_enrollment (customer_id,equb_type,amount,number_of_paid_lot,paid_date,reg_number_of_paid_lot) values (?,?,?,?,?,?)',(
                [(customer_id),
                equb_id[0][0],
                amount_entry.get(),
                # no_lot_entry.get(),
                1 ,
                enrollment_date_entry.get(),
                # no_lot_entry.get()
                1
                ]
            ))
            cursor.close()
            db.commit()
            db.close()
            clear_enrollment()
            total_label.config(text='')
            total_label_info.config(text='ብትክክል ሰፊሩ')
            total_label.after('3000',clear_total_label)
            total_label_info.after('3000',clear_total_label)
            payment_customer_name_entry.focus()
            clear_customer_info_lables()
        except:
            pass
        fill_payment_customer_list()
        fill_payment_type_list()
        fill_date(enrollment_date_entry)
        fill_drawn_customer_list()
        refresh_combo()
        clear_customer_info_lables()
    def update_enrollment():
        if len(enrollment_search_entry.get())>0:
            try:
                db=sqlite3.connect(database_name)
                cursor=db.cursor()
                cursor.execute('select id from equb_type where equb_type=?',[equb_type_entry.get()])
                equb_id=cursor.fetchall()
                cursor.execute('update equb_enrollment set equb_type=?,amount=?,number_of_paid_lot=?,paid_date=? ,reg_number_of_paid_lot=? where id=?',(
                    [
                    equb_id[0][0],
                    amount_entry.get(),
                    # no_lot_entry.get(),
                    1 ,
                    enrollment_date_entry.get(),
                    # no_lot_entry.get(),
                    1 ,
                    enrollment_search_entry.get()
                    ]
                ))
                cursor.close()
                db.commit()
                db.close()
                clear_enrollment()
                total_label.config(text='')
                total_label_info.config(text='ብትክክል ተመሓይሹ')
                total_label.after('3000',clear_total_label)
                total_label_info.after('3000',clear_total_label)
            except:
                pass
        fill_payment_customer_list()
        fill_payment_type_list()
        fill_date(enrollment_date_entry)
        fill_drawn_customer_list()
        refresh_combo()
    def delete_enrollment():
        if len(enrollment_search_entry.get())>0:
            try:
                db=sqlite3.connect(database_name)
                cursor=db.cursor()
                cursor.execute('delete from equb_enrollment  where id=?',(
                    [
                    enrollment_search_entry.get()
                    ]
                ))
                cursor.close()
                db.commit()
                db.close()
                clear_enrollment()
                total_label.config(text='')
                total_label_info.config(text='ካብ መዝገብ ጠፊኡ')
                total_label.after('3000',clear_total_label)
                total_label_info.after('3000',clear_total_label)
            except:
                pass
        fill_payment_customer_list()
        fill_payment_type_list()
        fill_date(enrollment_date_entry)
        fill_drawn_customer_list()
        refresh_combo()
    enrollment_title=ttk.Label(enrollment_frame,text='ዓሚል ናብ ዕቁብ መመዝገቢ ',font=('arial',12,'bold') ,foreground='green')
    enrollment_title.grid(row=0,column=0,padx=3,pady=5,sticky='w')
    
    enrollment_search_label=ttk.Label(enrollment_frame,image=search_photo)
    enrollment_search_label.grid(row=1,column=0,padx=3,pady=3,sticky='e')
    enrollment_search_entry=ttk.Entry(enrollment_frame,width=30)
    enrollment_search_entry.grid(row=1,column=0,padx=3,pady=3,sticky='w')
    enrollment_search_entry.bind('<KeyRelease>',find_and_fill_enrollment_entries)
    enrollment_search_entry.bind('<FocusIn>',find_and_fill_enrollment_entries)
    enrollment_search_entry.bind('<Down>',lambda e:customer_name_entry.focus())
    enrollment_search_entry.bind('<Up>',lambda e: enrollment_date_entry.focus())
    
    # def genterate_id(event):
    #    print(customer_name_entry.get())
    global customer_name_entry 
    customer_name_label=ttk.Label(enrollment_frame,text='ሽም ዓሚል')
    customer_name_label.grid(row=2,column=0,padx=3,pady=3,sticky='w')
    customer_name_entry=ttk.Combobox(enrollment_frame,width=32,values=customer_list)
    customer_name_entry.grid(row=3,column=0,padx=3,pady=3)
    customer_name_entry.bind('<Up>',lambda e: enrollment_search_entry.focus())
    customer_name_entry.bind('<Down>',lambda e: equb_type_entry.focus())
    customer_name_entry.bind('<KeyRelease>',lambda e:fill_customer_list_like())
    customer_name_entry.bind('<FocusIn>',lambda e:fill_enrollment_customer_photo())
    # customer_name_entry.bind('<FocusIn>',lambda e:fill_customer_list())
    customer_name_entry.focus()
    
    # def calculate_total(event):
    #     total_price()
    # def total_price():
    #     try:
    #         total_label_info.config(text=(float(amount_entry.get())* float(no_lot_entry.get())))
    #     except:
    #         total_label_info.config(text='')
        
    equb_type_label=ttk.Label(enrollment_frame,text='ዓይነት ዕቑብ')
    equb_type_label.grid(row=4,column=0,padx=3,pady=3,sticky='w')
    equb_type_entry=ttk.Combobox(enrollment_frame,width=32,values=equb_type)
    equb_type_entry.grid(row=5,column=0,padx=3,pady=3)
    equb_type_entry.bind('<Up>',lambda e:customer_name_entry.focus())
    equb_type_entry.bind('<Down>',lambda e:amount_entry.focus())
    equb_type_entry.bind('<FocusIn>',fill_amount)
    equb_type_entry.bind('<KeyRelease>',fill_amount)
    refresh_combo()
    
    amount_label=ttk.Label(enrollment_frame,text='መጠን ገንዘብ')
    amount_label.grid(row=6,column=0,padx=3,pady=3,sticky='w')
    amount_entry=ttk.Entry(enrollment_frame,width=35)
    amount_entry.grid(row=7,column=0,padx=3,pady=3)
    amount_entry.bind('<Up>',lambda e:equb_type_entry.focus())
    amount_entry.bind('<Down>',lambda e:enrollment_date_entry.focus())
    # amount_entry.bind('<KeyRelease>',calculate_total)
    # amount_entry.bind('<FocusIn>',calculate_total)
    
    # no_lot_label=ttk.Label(enrollment_frame,text='ዝኣተዎ በዝሒ ዕጫ')
    # no_lot_label.grid(row=8,column=0,padx=3,pady=3,sticky='w')
    # no_lot_entry=ttk.Entry(enrollment_frame,width=40)
    # no_lot_entry.grid(row=9,column=0,padx=3,pady=3)
    # no_lot_entry.bind('<KeyRelease>',calculate_total)
    # no_lot_entry.bind('<FocusIn>',calculate_total)
    # no_lot_entry.bind('<Up>',lambda e:amount_entry.focus())
    # no_lot_entry.bind('<Down>',lambda e:enrollment_date_entry.focus())
    
    total_label=ttk.Label(enrollment_frame,text='')
    total_label.grid(row=10,column=0,padx=3,pady=3,sticky='w')
    
    total_label_info=ttk.Label(enrollment_frame,text='')
    total_label_info.grid(row=10,column=0,padx=3,pady=3,sticky='e')
    
    enrollment_date_label=ttk.Label(enrollment_frame,text='ዕቑብ ዝኣተወሉ ዕለት')
    enrollment_date_label.grid(row=11,column=0,padx=3,pady=3,sticky='w')
    enrollment_date_entry=ttk.Entry(enrollment_frame,width=30)
    enrollment_date_entry.grid(row=12,column=0,padx=3,pady=3,sticky='w')
    enrollment_date_entry.bind('<Up>',lambda e:amount_entry.focus())
    enrollment_date_entry.bind('<Down>',lambda e:enrollment_search_entry.focus())
    fill_date(enrollment_date_entry)
    # def fill_date_event():
    #     enrollment_date_entry.delete(0,END)
    #     enrollment_date_entry.insert(END,clock)
    enrollment_fill_date_button=ttk.Button(enrollment_frame,text='⏱️',width=3,command=lambda : fill_date(enrollment_date_entry))
    enrollment_fill_date_button.grid(row=12,column=0,padx=3,pady=3,sticky='e')
    
    enrollment_register_button=ttk.Button(enrollment_frame,width=10,text='መዝግብ',command=register_enrollment,style='save.TButton')
    
    
    enrollment_update_button=ttk.Button(enrollment_frame,width=10,text='ኣመሓይሽ',style='update.TButton',command=update_enrollment)
    
    
    enrollment_delete_button=ttk.Button(enrollment_frame,width=10,text='ኣጥፍእ',style='delete.TButton',command=delete_enrollment)
    
    
    enrollment_back_button=ttk.Button(enrollment_frame,width=10,text='<< ተመለስ',command=display_register_customer_frame)
    enrollment_back_button.grid(row=14,column=0,padx=3,pady=3,sticky='w')
    enrollment_next_button=ttk.Button(enrollment_frame,width=10,text='ቀፅል >>',command=display_payment_frame)
    enrollment_next_button.grid(row=14,column=0,padx=3,pady=12,sticky='e')
    def check_enrollment():
        if len(enrollment_search_entry.get())>0:
            enrollment_register_button.grid_forget()
            enrollment_update_button.config(width=16)
            enrollment_update_button.grid(row=13,column=0,padx=3,pady=3,sticky='w')
            enrollment_delete_button.config(width=16)
            enrollment_delete_button.grid(row=13,column=0,padx=3,pady=3,sticky='e')
        else:
            enrollment_register_button.config(width=34)
            enrollment_register_button.grid(row=13,column=0,padx=3,pady=3,sticky='w')
            enrollment_update_button.grid_forget()
            enrollment_delete_button.grid_forget()
    check_enrollment()
# ************************************* payment form **********************************************************
    def clear_customer_and_type():
        payment_customer_name_entry.delete(0,END)
        payment_equb_type_entry.delete(0,END)
    def clear_payment_derived_entries():
        payment_amount_entry.delete(0,END)
        unpaid_amount.config(state='normal')
        unpaid_amount.delete(0,END)
        unpaid_amount.config(state='disabled')
        payment_round_entry.delete(0,END)
        payment_date_entry.delete(0,END)
        payment_punishment_entry.delete(0,END)
        payment_total_label_info.config(text='')
    def clear_payment_entries():
        clear_customer_and_type()
        clear_payment_derived_entries()
    def find_and_fill_payment_entries_from_enrollment_event(event):
        find_and_fill_payment_entries_from_enrollment()
    def find_and_fill_payment_entries_from_enrollment():
        if len(payment_search_entry.get())==0 :
            try:

                reached_round=return_current_round(payment_equb_type_entry.get())[0]
            except:
                pass
            customer_id=(payment_customer_name_entry.get()).split('/')[0]
            equb_type=payment_equb_type_entry.get()
            
            db = sqlite3.connect(database_name)
            cursor = db.cursor()
            try:
                cursor.execute(f'select id  from equb_type where equb_type=?',[payment_equb_type_entry.get()])
                id_result=cursor.fetchall()
                
                if id_result:
                    # cursor.execute(f'select current_round  from round where equb_type_id=?',[id_result[0][0]])
                    # round_result=cursor.fetchall()
                    round_result=fill_reached_paid_round()
                    
                    cursor.execute(('select amount,reg_number_of_paid_lot from equb_enrollment where customer_id=? and equb_type=?'),[customer_id,id_result[0][0]])
                    amount_result=cursor.fetchall()
                    
                    clear_payment_derived_entries()
                    cursor.execute(('select sum(amount) from pay_list where customer_id=? and equb_type_id=?'),[customer_id,id_result[0][0]])
                    total_saved_money_of_customer=cursor.fetchall()
                    cursor.execute(('select count(punished_amount) from pay_list where customer_id=? and equb_type_id=? and punished_amount>0'),[customer_id,id_result[0][0]])
                    punishment_result_amount=cursor.fetchall()
                    cursor.execute(('select  sum(punished_amount) from pay_list where customer_id=? and equb_type_id=? and punished_amount>0'),[customer_id,id_result[0][0]])
                    punishment_result_money=cursor.fetchall()
                    cursor.execute(('select amount_of_money from drawn_list where customer_id=? and equb_type_id=?'),[customer_id,id_result[0][0]])
                    customer_got_money_back=cursor.fetchall()
                    
                    if (amount_result):
                        payment_amount_entry.delete(0,END)
                        payment_amount_entry.insert(END,amount_result[0][0])
                        unpaid_amount.config(state='normal')
                        unpaid_amount.delete(0,END)
                        unpaid_amount.insert(END,0)
                        unpaid_amount.config(state='disabled')
                        fill_reached_round()
                        # def total_price():
                        #     try:
                        #         total=float(amount_result[0][0])-float(payment_amount_entry.get())
                        #         return total
                        #     except:
                        #         pass
                    
                    if round_result and reached_round: 
                        cursor.execute(('select  id from pay_list where customer_id=? and equb_type_id=? and unpaid_amount>0 and paid_round=?'),[customer_id,id_result[0][0],int(round_result)-1])
                        half_money=cursor.fetchall()
                        
                        if half_money:
                            payment_search_entry.delete(0,END)
                            payment_search_entry.insert(END,half_money[0][0])
                            payment_search_entry.focus()
                        payment_round_entry.delete(0,END)
                        payment_round_entry.insert(END,round_result)
                        
                        if customer_got_money_back:
                            have_customer_equb_label.config(text='')
                            have_customer_equb_label.config(text='ዕቁብ በፂሕዎ ዶ ? ')
                            taken_amount_label.config(text='')
                            taken_amount_label.config(text=f'✔ እወ {customer_got_money_back[0][0]}',foreground='green')
                        else:
                            have_customer_equb_label.config(text='')
                            have_customer_equb_label.config(text='ዕቁብ በፂሕዎ ዶ ? ')
                            taken_amount_label.config(text='')
                            taken_amount_label.config(text=f'❌ ኣይበፅሖን',foreground='red')
                        
                        if (int(round_result)>int(reached_round)):
                            has_paid_last_round_label.config(text='')
                            has_paid_last_round_label.config(text='ዝሓለፈ ከፊሉ ዶ ? ')
                            past_unpaid_status_label.config(text='')
                            past_unpaid_status_label.config(text='✔ እወ',foreground='green')
                            past_unpaid_round_label.config(text='')
                            past_unpaid_amount_label.config(text='')
                            current_round_unpaid_quetion_label.config(text='')
                            current_round_unpaid_quetion_label.config(text=f'{reached_round}ይ ዙር ከፊሉ ዶ?')
                            current_round_unpaid_label.config(text='')
                            current_round_unpaid_label.config(text='✔ እወ',foreground='green')
                        elif (int(round_result)==int(reached_round)):
                            if reached_round!=1:
                                has_paid_last_round_label.config(text='')
                                has_paid_last_round_label.config(text='ዝሓለፈ ከፊሉ ዶ ? ')
                                past_unpaid_status_label.config(text='')
                                past_unpaid_status_label.config(text='✔ እወ',foreground='green')
                            else:
                                has_paid_last_round_label.config(text='')
                                past_unpaid_status_label.config(text='')
                            past_unpaid_round_label.config(text='')
                            past_unpaid_amount_label.config(text='')
                            current_round_unpaid_quetion_label.config(text='')
                            current_round_unpaid_quetion_label.config(text=f'{reached_round}ይ ዙር ከፊሉ ዶ?')
                            current_round_unpaid_label.config(text='')
                            current_round_unpaid_label.config(text='❌ ኣይከፈለን',foreground='red')
                        # elif (int(reached_round)>int(round_result)):
                            
                        #     has_paid_last_round_label.config(text='')
                        #     has_paid_last_round_label.config(text='ዝሓለፈ ከፊሉ ዶ ? ')
                        #     past_unpaid_status_label.config(text='')
                        #     past_unpaid_status_label.config(text='✔ እወ',foreground='green')
                        #     past_unpaid_round_label.config(text='')
                        #     past_unpaid_amount_label.config(text='')
                        #     current_round_unpaid_quetion_label.config(text='')
                        #     current_round_unpaid_quetion_label.config(text=f'{reached_round}ይ ዙር ከፊሉ ዶ?')
                        #     current_round_unpaid_label.config(text='')
                        #     current_round_unpaid_label.config(text='❌ ኣይከፈለን',foreground='red')
                        elif (int(reached_round)>int(round_result)):
                            has_paid_last_round_label.config(text='')
                            has_paid_last_round_label.config(text='ዝሓለፈ ከፊሉ ዶ ? ')
                            past_unpaid_status_label.config(text='')
                            past_unpaid_status_label.config(text='❌ ኣይከፈለን',foreground='red')
                            past_unpaid_round_label.config(text='')
                            past_unpaid_round_label.config(text=f'ዘይተኸፈለ ዙር : {round_result}-{reached_round} ',foreground='red')
                            past_unpaid_amount_label.config(text='')
                            past_unpaid_amount_label.config(text=f'ዘይተከፈለ ገንዘብ : {((int(reached_round)-int(round_result))+1)*int(amount_result[0][0])}',foreground='red')
                            current_round_unpaid_quetion_label.config(text='')
                            current_round_unpaid_quetion_label.config(text=f'{reached_round}ይ ዙር ከፊሉ ዶ?')
                            current_round_unpaid_label.config(text='')
                            current_round_unpaid_label.config(text='❌ ኣይከፈለን',foreground='red')
                    else:
                        clear_customer_info_lables()
                        # has_paid_last_round_label.config(text='')
                        # past_unpaid_status_label.config(text='')
                        # past_unpaid_round_label.config(text='')
                        # past_unpaid_amount_label.config(text='')
                        # current_round_unpaid_quetion_label.config(text='')
                        # current_round_unpaid_label.config(text='')
                    if total_saved_money_of_customer[0][0]!=None :
                        total_paid_amount_till_now_label.config(text='')
                        total_paid_amount_till_now_label.config(text=f'ዝዓቖሮ ገንዘብ : {total_saved_money_of_customer[0][0]}')  
                    else:
                        total_paid_amount_till_now_label.config(text='ዝዓቖሮ ገንዘብ : 0')
                    if punishment_result_amount[0][0]!=None :
                        total_punished_amount_label.config(text='')
                        total_punished_amount_label.config(text=f'በዝሒ ቅፅዓት : {punishment_result_amount[0][0]}')
                        
                    else:
                        total_punished_amount_label.config(text='')
                        
                    # if punishment_result_money:
                    #     total_punished_money_label.config(text='')
                    if punishment_result_money[0][0]!=None:
                        total_punished_money_label.config(text=f'ዝተቐፅዖ ገንዘብ : {punishment_result_money[0][0]}')
                    else:
                        total_punished_money_label.config(text=f'ዝተቐፅዖ ገንዘብ : 0')
                    # else:
                    #     total_punished_money_label.config(text='')
                    # total_price=total_price()
                    # payment_total_label_info.config(text='')
                    # payment_total_label_info.config(text=total_price)
                    payment_punishment_entry.delete(0,END)
                    payment_punishment_entry.insert(END,'0')
                    payment_date_entry.delete(0,END)
                    payment_date_entry.insert(END,clock)
                else:
                    payment_equb_type_entry.delete(0,END)
                    enrolled_equb_type.clear()
            
            except:
                pass
            
            
            cursor.close()
            db.commit()
            db.close()
    def register_payment():
        try:
            customer_id=(payment_customer_name_entry.get()).split('/')[0]
            db=sqlite3.connect(database_name)
            cursor=db.cursor()
            cursor.execute('select id from equb_type where equb_type=?',[payment_equb_type_entry.get()])
            equb_id=cursor.fetchall()
            cursor.execute('insert into pay_list (customer_id,equb_type_id,amount,unpaid_amount,paid_round,punished_amount,paid_date) values (?,?,?,?,?,?,?)',(
                [(customer_id),
                equb_id[0][0],
                payment_amount_entry.get(),
                unpaid_amount.get(),
                payment_round_entry.get(),
                payment_punishment_entry.get(),
                payment_date_entry.get()
                ]
            ))
            cursor.close()
            db.commit()
            db.close()
            
            payment_total_label.config(text='ብትክክል ተመዝጊቡ')
            # payment_total_label.config(text='')
            def clear_payment_total_label(): 
                payment_total_label.config(text='')
                payment_total_label_info.config(text='')
            payment_total_label.after('3000',clear_payment_total_label)
            payment_total_label_info.after('3000',clear_payment_total_label)
        
            fill_payment_customer_list()
            fill_payment_type_list()
            # clear_payment_entries()
            # payment_punishment_entry.insert(END,'0')
            fill_date(payment_date_entry)
            display_profile_picture(default_profile_photo,customer_photo_info_label)
            clear_customer_info_lables()
        except:
            pass
    def update_payment():
        try:
            customer_id=payment_search_entry.get()
            db=sqlite3.connect(database_name)
            cursor=db.cursor()
            cursor.execute("""update  pay_list  set   amount=? , 
                        unpaid_amount=? , paid_round=? ,punished_amount=?, paid_date=? where id=?  """,(
                [
                payment_amount_entry.get(),
                unpaid_amount.get(),
                payment_round_entry.get(),
                payment_punishment_entry.get(),
                payment_date_entry.get(),
                payment_search_entry.get()
                ]
            ))
            cursor.close()
            db.commit()
            db.close()
            
            payment_total_label.config(text='ብትክክል ተመሓይሹ')
            # payment_total_label.config(text='')
            def clear_payment_total_label():
                payment_total_label.config(text='')
                payment_total_label_info.config(text='')
            payment_total_label.after('3000',clear_payment_total_label)
            payment_total_label_info.after('3000',clear_payment_total_label)
        
            fill_payment_customer_list()
            fill_payment_type_list()
            clear_payment_entries()
            payment_punishment_entry.insert(END,'0')
            fill_date(payment_date_entry)
            display_profile_picture(default_profile_photo,customer_photo_info_label)
            clear_customer_info_lables()
            payment_search_entry.delete(0,END)
        except:
            pass
    def delete_payment():
        try:

            customer_id=payment_search_entry.get()
            db=sqlite3.connect(database_name)
            cursor=db.cursor()
            cursor.execute("""delete from  pay_list  where id=?  """,(
                [
                payment_search_entry.get()
                ]
            ))
            cursor.close()
            db.commit()
            db.close()
            
            payment_total_label.config(text='ብትክክል ጠፊኡ')
            # payment_total_label.config(text='')
            def clear_payment_total_label():
                payment_total_label.config(text='')
                payment_total_label_info.config(text='')
            payment_total_label.after('3000',clear_payment_total_label)
            payment_total_label_info.after('3000',clear_payment_total_label)
            clear_payment_entries()
            payment_punishment_entry.insert(END,'0')
            fill_date(payment_date_entry)
            display_profile_picture(default_profile_photo,customer_photo_info_label)
            clear_customer_info_lables()
            payment_search_entry.delete(0,END)
        except:
            pass
    def find_and_fill_payment_entries(event):
        payment_reached_round_label.config(text='')
        clear_customer_info_lables()
        find_and_fill_payment_entries_after()
        check_payment_qualification()
    def find_and_fill_payment_entries_after():
        try:
            if len(payment_search_entry.get())==0:
                payment_update_button.config(state='disable')
                payment_delete_button.config(state='disable')
            else:
                payment_update_button.config(state='active')
                payment_delete_button.config(state='active')
            clear_payment_entries()
            db=sqlite3.connect(database_name)
            cursor=db.cursor()
            cursor.execute("""select pay_list.customer_id as paylist_id,customer.customer_name,equb_type.equb_type,amount,
                        unpaid_amount,paid_round,punished_amount,paid_date, customer.photo from pay_list 
                        JOIN customer ON pay_list.customer_id=customer.id
                        JOIN equb_type ON pay_list.equb_type_id=equb_type.id 
                        where pay_list.id=?""",[payment_search_entry.get()])
            result=cursor.fetchone()
            cursor.close()
            db.commit()
            db.close()
            if result:
                payment_customer_name_entry.insert(END,f'{result[0]} / {result[1]}')
                payment_equb_type_entry.insert(END,result[2])
                payment_amount_entry.insert(END,result[3])
                unpaid_amount.config(state='normal')
                unpaid_amount.insert(END,result[4])
                unpaid_amount.config(state='disabled')
                payment_round_entry.insert(END,result[5])
                payment_punishment_entry.insert(END,result[6])
                payment_date_entry.insert(END,result[7])
                display_profile_picture(result[8],customer_photo_info_label)
            else:
                display_profile_picture(default_profile_photo,customer_photo_info_label)
        except:
            pass
    def fill_payment_type_list_event(event):
        if len(payment_search_entry.get())==0:
            fill_payment_type_list()
            fill_payment_customer_list_like()
            # fill_reached_round()
    def fill_payment_type_list():
        try:
            customer_id=(payment_customer_name_entry.get()).split('/')[0]
            db=sqlite3.connect(database_name)
            cursor=db.cursor()
            
            cursor.execute(("""select equb_type.equb_type from equb_enrollment
                            JOIN equb_type ON equb_enrollment.equb_type=equb_type.id
                            where equb_enrollment.customer_id=?
                            
                            """),[customer_id])
            result=cursor.fetchall()
            cursor.close()
            db.commit()
            db.close()
            enrolled_equb_type.clear()
            
            if result:
                for i in result:
                    enrolled_equb_type.append(i[0])
                payment_equb_type_entry.config(values=enrolled_equb_type)
                payment_equb_type_entry.delete(0,END)
                payment_equb_type_entry.insert(END,enrolled_equb_type[0])
                customers_selected_equb_label.config(text='')
                customers_selected_equb_label.config(text=enrolled_equb_type[0])
                find_and_fill_payment_entries_from_enrollment()
                # payment_punishment_entry.delete(0,END)
                # payment_punishment_entry.insert(END,'0')
            else:
                clear_payment_derived_entries()
                clear_customer_info_lables()
        except:
            pass
    global fill_payment_customer_list
    def fill_payment_customer_list_like():
        
        try:
            db=sqlite3.connect(database_name)
            cursor=db.cursor()
            cursor.execute("""select customer_id , customer.customer_name ,photo
                            from equb_enrollment 
                            JOIN customer ON equb_enrollment.customer_id=customer.id  
                            where customer.customer_name 
                            like '%"""+payment_customer_name_entry.get()+"""%'
                            or customer_id=? order by customer_id desc""",[payment_customer_name_entry.get().split('/')[0]])
            result=cursor.fetchall()
            cursor.close()
            db.commit()
            db.close()
            
            enrolled_customer_list.clear()
            
            if result:
                for i in result:
                    #enrolled_customer_list.append([i[0],'/',i[1]])
                    if f"{i[0]} / {i[1]}" not in enrolled_customer_list:
                            enrolled_customer_list.append(f"{i[0]} / {i[1]}")
                payment_customer_name_entry.config(values=enrolled_customer_list)
                # payment_customer_name_entry.set(enrolled_customer_list[-1])
                if len(payment_customer_name_entry.get())==0:
                    display_profile_picture(default_profile_photo,customer_photo_info_label)
                    customer_name_info_label.config(text='')
                else:
                    display_profile_picture(result[0][2],customer_photo_info_label)
                    customer_name_info_label.config(text=f'{result[0][0]} / {result[0][1]}')
            else:
                display_profile_picture(default_profile_photo,customer_photo_info_label)
                clear_customer_info_lables()
        except:
            
            pass
    def fill_payment_customer_list():
        try:
            db=sqlite3.connect(database_name)
            cursor=db.cursor()
            cursor.execute(("""select customer_id , customer.customer_name
                            from equb_enrollment 
                            JOIN customer ON equb_enrollment.customer_id=customer.id 
                            order by customer_id desc"""))
            result=cursor.fetchall()
            cursor.close()
            db.commit()
            db.close()
            enrolled_customer_list.clear()
            if result:
                for i in result:
                    if f"{i[0]} / {i[1]}" not in enrolled_customer_list:
                        enrolled_customer_list.append(f"{i[0]} / {i[1]}")
                    # enrolled_customer_list.append([i[0],'/',i[1]])
                
                payment_customer_name_entry.config(values=enrolled_customer_list)
                payment_customer_name_entry.delete(0,END)
                payment_customer_name_entry.insert(END,enrolled_customer_list[0])  
                # payment_customer_name_entry.focus()
                
            else:
                enrolled_customer_list.clear()
                payment_customer_name_entry.config(values=enrolled_customer_list)
        except:
            pass
    def scan_and_fill_customer():
        scanned_value=scan_qrcode()
        payment_customer_name_entry.delete(0,END)
        payment_customer_name_entry.insert(END,scanned_value)
        payment_customer_name_entry.focus()
    def fill_reached_round():
        reached_round=return_current_round(payment_equb_type_entry.get())[0]
        if reached_round:
            payment_reached_round_label.config(text='')
            payment_reached_round_label.config(text=f'ዕቑብ ሕዚ ዝበፅሖ ዙር  :  {str(reached_round)}ይ',foreground='blue')
            selected_equb_reached_round.config(text='')
            selected_equb_reached_round.config(text=f'ሕዚ ዘሎ ዙር : {reached_round}ይ ዙር')
            customers_selected_equb_label.config(text='')
            customers_selected_equb_label.config(text=payment_equb_type_entry.get())
        else:
            selected_equb_reached_round.config(text='')
            payment_reached_round_label.config(text='')
    def fill_reached_paid_round():
        
        customers_id=payment_customer_name_entry.get().split('/')[0]
        
        db=sqlite3.connect(database_name)
        cursor=db.cursor()
        cursor.execute("select id from equb_type where equb_type=?",[payment_equb_type_entry.get()])
        equbs_id=cursor.fetchone()
        
        cursor.execute("""select max(paid_round) from pay_list where customer_id=? and equb_type_id=?""",(customers_id,equbs_id[0]))
        result=cursor.fetchall()
        if result[0][0]!=None:
            return int(result[0][0])+1
        else:
            return '1'
        cursor.close()
        db.commit()
        db.close()
    
    
    
    
    
    # def toggle_search(event):
    #     if (payment_search_entry.winfo_ismapped()):
              
    #         # payment_search_label.config(image=close_photo)
    #         payment_search_entry.grid_forget()
            

    #     else:
    #         payment_search_label.config(image=search_photo)
    #         payment_search_entry.grid(row=1,column=0,padx=3,pady=3,sticky='e')
            
    payment_title=ttk.Label(payment_frame,text='ክፍሊት መፈፀሚ ቕጥዒ',font=('arial',14,'bold') ,foreground='blue')
    payment_title.grid(row=0,column=0,padx=3,pady=5,sticky='w')
    payment_search_label=ttk.Label(payment_frame,image=search_photo)
    payment_search_label.grid(row=1,column=0,padx=3,pady=3,sticky='w')
    # payment_search_label.bind('<Button-1>',toggle_search)
    payment_search_entry=ttk.Entry(payment_frame,width=30)
    payment_search_entry.grid(row=1,column=0,padx=3,pady=3,sticky='e')
    
    payment_search_entry.bind('<KeyRelease>',find_and_fill_payment_entries)
    payment_search_entry.bind('<FocusIn>',find_and_fill_payment_entries)
    payment_search_entry.bind('<Down>',lambda e:payment_customer_name_entry.focus())
    payment_search_entry.bind('<Up>',lambda e: payment_date_entry.focus())
    
    global payment_customer_name_entry
    payment_customer_name_label=ttk.Label(payment_frame,text='ሽም ዓሚል')
    payment_customer_name_label.grid(row=2,column=0,padx=3,pady=3,sticky='w')
    payment_customer_name_entry=ttk.Combobox(payment_frame,width=20,values=customer_list)
    payment_customer_name_entry.grid(row=3,column=0,padx=3,pady=3,sticky='w')
    payment_customer_name_entry.bind('<Up>',lambda e: payment_search_entry.focus())
    payment_customer_name_entry.bind('<Down>',lambda e: payment_equb_type_entry.focus())
    payment_customer_name_entry.bind('<FocusIn>',fill_payment_type_list_event)
    payment_customer_name_entry.bind('<KeyRelease>',fill_payment_type_list_event)
    
    # payment_customer_name_entry.bind('<KeyRelease>',lambda e:fill_payment_customer_list_like())
    # qr_image=ImageTk.PhotoImage(Image.open('./image/qr_code.png'))
    display_payment_frame()
    scan_customer_name=ttk.Button(payment_frame,text='Qr Code',command=scan_and_fill_customer,width=10)
    scan_customer_name.grid(row=3,column=0,padx=3,pady=3,sticky='e')
    fill_payment_customer_list()
    # customer_name_entry.bind('<FocusIn>',genterate_id)
    global payment_equb_type_entry
    payment_equb_type_label=ttk.Label(payment_frame,text='ዓይነት ዕቑብ')
    payment_equb_type_label.grid(row=4,column=0,padx=3,pady=3,sticky='w')
    payment_equb_type_entry=ttk.Combobox(payment_frame,width=32,values=enrolled_equb_type)
    payment_equb_type_entry.grid(row=5,column=0,padx=3,pady=3)
    payment_equb_type_entry.bind('<Up>',lambda e:payment_customer_name_entry.focus())
    payment_equb_type_entry.bind('<Down>',lambda e:payment_amount_entry.focus())
    
    payment_equb_type_entry.bind('<FocusIn>',find_and_fill_payment_entries_from_enrollment_event)
    
    # refresh_combo()
    
    def calculate_total(event):
        try:
            # if len(payment_search_entry.get())==0:
            customer_id=(payment_customer_name_entry.get()).split('/')[0]
            equb_type=payment_equb_type_entry.get()
            db = sqlite3.connect(database_name)
            cursor = db.cursor()
            
            cursor.execute(f'select id  from equb_type where equb_type=?',[payment_equb_type_entry.get()])
            id_result=cursor.fetchall()
            if id_result:
                
                cursor.execute(('select amount from equb_enrollment where customer_id=? and equb_type=?'),[customer_id,id_result[0][0]])
                amount_result=cursor.fetchall()
                
                if (amount_result):
                    if len(payment_amount_entry.get())>0  and float(payment_amount_entry.get()) >0  and float(payment_amount_entry.get())<= float(amount_result[0][0]):
                        unpaid_amount.config(state='normal')
                        unpaid_amount.delete(0,END)
                        unpaid_amount.insert(END,float(amount_result[0][0])-float(payment_amount_entry.get()))
                        unpaid_amount.config(state='disabled')
                    else:
                        unpaid_amount.config(state='normal')
                        
                        unpaid_amount.delete(0,END)
                        unpaid_amount.insert(END,'')
                        unpaid_amount.config(state='disabled')
            cursor.close()
            db.commit()
            db.close()
        except:
            unpaid_amount.delete(0,END)
            # payment_total_label_info.config(text='')
    payment_amount_label=ttk.Label(payment_frame,text='መጠን ገንዘብ')
    payment_amount_label.grid(row=6,column=0,padx=3,pady=3,sticky='w')
    payment_amount_entry=ttk.Entry(payment_frame,width=16)
    payment_amount_entry.grid(row=7,column=0,padx=2,pady=3,sticky='w')
    payment_amount_entry.bind('<Up>',lambda e:payment_equb_type_entry.focus())
    payment_amount_entry.bind('<Down>',lambda e:payment_round_entry.focus())
    payment_amount_entry.bind('<KeyRelease>',calculate_total)
    
    unpaid_amount_label=ttk.Label(payment_frame,text='ተረፍ ገንዘብ ')
    unpaid_amount_label.grid(row=6,column=0,padx=3,pady=3,sticky='e')
    unpaid_amount=ttk.Entry(payment_frame,width=16)
    unpaid_amount.grid(row=7,column=0,padx=2,pady=3,sticky='e')
    # unpaid_amount.bind('<KeyRelease>',calculate_total)
    unpaid_amount.bind('<Up>',lambda e:payment_amount_entry.focus())
    unpaid_amount.bind('<Down>',lambda e:payment_round_entry.focus())
    
    payment_total_label=ttk.Label(payment_frame,text='')
    payment_total_label.grid(row=10,column=0,padx=3,pady=3,sticky='w')
    
    payment_total_label_info=ttk.Label(payment_frame,text='')
    payment_total_label_info.grid(row=10,column=0,padx=3,pady=3,sticky='e')
    
    payment_reached_round_label=ttk.Label(payment_frame,text='')
    payment_reached_round_label.grid(row=11,column=0,padx=3,pady=3,sticky='e')
    
    payment_round_label=ttk.Label(payment_frame,text='ዝተከፈለ ዙር')
    payment_round_label.grid(row=11,column=0,padx=3,pady=3,sticky='w')
    
    global payment_round_entry
    payment_round_entry=ttk.Entry(payment_frame,width=35)
    payment_round_entry.grid(row=12,column=0,padx=3,pady=3,sticky='w')
    payment_round_entry.bind('<Up>',lambda e:payment_amount_entry.focus())
    payment_round_entry.bind('<Down>',lambda e:payment_punishment_entry.focus())
    
    def fill_punishment():
        try:
            db = sqlite3.connect(database_name)
            cursor = db.cursor()
            cursor.execute(f'select punishment_amount  from punishment where punishment_name=?',[payment_punishment_entry_list.get()])
            punishmet_amount=cursor.fetchall()
            
            if punishmet_amount:

                payment_punishment_entry.delete(0,END)
                payment_punishment_entry.insert(END,punishmet_amount[0][0])
            else:
                payment_punishment_entry.delete(0,END)
            cursor.close()
            db.commit()
            db.close()
        except:
            pass
    payment_punishment_label=ttk.Label(payment_frame,text='ቅፅዓት')
    payment_punishment_label.grid(row=13,column=0,padx=3,pady=3,sticky='w')
    payment_punishment_entry_list=ttk.Combobox(payment_frame,width=20,values=punishmet_list)
    payment_punishment_entry_list.grid(row=14,column=0,padx=3,pady=3,sticky='w')
    payment_punishment_entry_list.set(punishmet_list[-1])
    payment_punishment_entry_list.bind('<KeyRelease>',lambda e:fill_punishment())
    payment_punishment_entry_list.bind('<FocusIn>',lambda e:fill_punishment())
    payment_punishment_entry=ttk.Entry(payment_frame,width=10)

    payment_punishment_entry.grid(row=14,column=0,padx=3,pady=3,sticky='e')
    payment_punishment_entry.bind('<Up>',lambda e:payment_round_entry.focus())
    payment_punishment_entry.bind('<Down>',lambda e:payment_date_entry.focus())
    fill_punishment()
    payment_date_label=ttk.Label(payment_frame,text='ዕለት')
    payment_date_label.grid(row=15,column=0,padx=3,pady=3,sticky='w')
    payment_date_entry=ttk.Entry(payment_frame,width=30)
    payment_date_entry.grid(row=16,column=0,padx=3,pady=3,sticky='w')
    payment_date_entry.bind('<Up>',lambda e:payment_punishment_entry.focus(),)
    payment_date_entry.bind('<Down>',lambda e:payment_search_entry.focus())
    fill_date(payment_date_entry)
    # def fill_date_event():
    #     payment_date_entry.delete(0,END)
    #     payment_date_entry.insert(END,clock)
    payment_fill_date_button=ttk.Button(payment_frame,text='⏱️',width=3,command=lambda : fill_date(payment_date_entry))
    payment_fill_date_button.grid(row=16,column=0,padx=3,pady=3,sticky='e')
    
    payment_register_button=ttk.Button(payment_frame,width=10,text='ከፊሉ',command=register_payment,style='save.TButton')
    
    
    payment_update_button=ttk.Button(payment_frame,width=10,text='ኣመሓይሽ',style='update.TButton',command=update_payment)
    
    
    payment_delete_button=ttk.Button(payment_frame,width=10,text='ኣጥፍእ',style='delete.TButton',command=delete_payment)
    
    
    create_new_customer_button=ttk.Button(payment_frame,width=35,text='ሓድሽ ዓሚል መዝግብ',style='delete.TButton',command=display_register_customer_frame)
    create_new_customer_button.grid(row=18,column=0,padx=3,pady=12)
    def check_payment_qualification():
        if len(payment_search_entry.get())>0:
            payment_register_button.grid_forget()
            payment_update_button.config(width=16)
            payment_update_button.grid(row=17,column=0,padx=3,pady=3,sticky='w')
            payment_delete_button.config(width=16)
            payment_delete_button.grid(row=17,column=0,padx=3,pady=3,sticky='e')
        else:
            payment_register_button.config(width=35)
            payment_register_button.grid(row=17,column=0,padx=3,pady=3,sticky='w')
            payment_update_button.grid_forget()
            payment_delete_button.grid_forget()
    check_payment_qualification()
#******************************************drawn frame *******************************************
    #******************************************drawn******************************
    def fill_drawn_date():
        drawn_date_entry.delete(0,END)
        drawn_date_entry.insert(END,clock)
    def clear_drawn_total_label():
        drawn_total_label.config(text='ጠቕላላ:')
        drawn_total_label_info.config(text='')
    def clear_profile_photos():
        
        display_profile_picture(default_profile_photo,drawn_profile_photo_label)
        display_profile_picture(default_profile_photo,drawn_warrant_profile_photo_label)
    def clear_drawn_entries():
        drawn_customer_name_entry.delete(0,END),
        drawn_equb_type_entry.delete(0,END),
        drawn_amount_entry.delete(0,END),
        drawn_round_entry.delete(0,END),
        drawn_date_entry.delete(0,END),
        drawn_warrant_name_entry.delete(0,END)
        drawn_tax_entry.delete(0,END)
        # drawn_profile_photo_label.after('3000',clear_profile_photos)
        clear_profile_photos()
    def clear_drawn():
        clear_drawn_entries()
        clear_drawn_total_label()
        # drawn_total_label.config(text='')
        # drawn_total_label_info.config(text='registered successfully')
        # drawn_total_label.after('3000',clear_drawn_total_label)
        # drawn_total_label_info.after('3000',clear_drawn_total_label)
    to_be_drawn=[]

    def draw_winner_event(event):
        customer_photo=(fetch_data_by_id('*','customer',drawn_customer_name_entry.get().split('/')[0]))
        if customer_photo:
            new_customer_photo=customer_photo[5]
            display_profile_picture(default_profile_photo,drawn_warrant_profile_photo_label)
            display_profile_picture(new_customer_photo,drawn_profile_photo_label)
        else:
            display_profile_picture(default_profile_photo,drawn_warrant_profile_photo_label)
    def draw_winner():
        fill_drawn_customer_list()
        if len(drawn_equb_type_entry.get())>0:
            try:
                db=sqlite3.connect(database_name)
                cursor=db.cursor()
                cursor.execute('select id from equb_type where equb_type=? ',[drawn_equb_type_entry.get()])
                equb_id=cursor.fetchall()
                
                # if equb_id:
                #     cursor.execute('select tax from equb_type where id=? ',[equb_id[0][0]])
                #     tax=cursor.fetchall()
                
                if equb_id:
                    cursor.execute(("""select equb_enrollment.customer_id  ,number_of_paid_lot ,customer.customer_name
                                    from equb_enrollment JOIN customer ON equb_enrollment.customer_id=customer.id
                                    where number_of_paid_lot>0 and equb_type=?"""),([equb_id[0][0]]))
                    result=cursor.fetchall()
                    to_be_drawn.clear()
                    
                    if result:
                        for i in result:
                            to_be_drawn.append(f'{i[0]} / {i[2]}')
                        
                        selected_winner=random.choice(to_be_drawn)
                        drawn_customer_name_entry.delete(0,END)
                        drawn_customer_name_entry.insert(END,selected_winner)
                        
                        selected_winner_id=selected_winner.split('/')[0]
                        
                        # drawn_tax_entry.delete(0,END)
                        # drawn_tax_entry.insert(END,tax[0][0])
                        fill_drawn_total_amount()
                        fill_tax()
                        customer_photo=(fetch_data_by_id('*','customer',selected_winner_id))
                        calculate_drawn_total()
                        new_customer_photo=customer_photo[5]
                        display_profile_picture(default_profile_photo,drawn_warrant_profile_photo_label)
                        display_profile_picture(new_customer_photo,drawn_profile_photo_label)
                        drawn_generate_random_button.config(state='disabled')
                        drawn_customer_name_entry.config(state='disabled')
                        drawn_equb_type_entry.config(state='disabled')
                        def active_draw_button():
                            drawn_notification_label.config(text='',background='white')
                            drawn_generate_random_button.config(state='active')
                            drawn_customer_name_entry.config(state='active')
                            drawn_equb_type_entry.config(state='active')
                        drawn_generate_random_button.after('15000',active_draw_button)
                        drawn_notification_label.config(text='ካሊእ ዕጫ ንምውዳቕ 10 ሰከንድ ይፀበዩ')
                    else:
                        display_profile_picture(default_profile_photo,drawn_profile_photo_label)
                        clear_drawn()  
                cursor.close()
                db.commit()
                db.close()
            except:
                pass
    def find_and_fill_drawn_entries(event):
        find_and_fill_drawn_entries_after()
    
    def find_and_fill_drawn_entries_after():
        try:
            db=sqlite3.connect(database_name)
            cursor=db.cursor()
            cursor.execute(("""select customer.customer_name , equb_type.equb_type, drawn_date, drawn_list.amount_of_money ,warrant_id,drawn_round,customer_id,customer.photo,drawn_tax
                            from drawn_list 
                            JOIN customer ON drawn_list.customer_id=customer.id 
                            
                            JOIN equb_type ON drawn_list.equb_type_id=equb_type.id
                            where drawn_list.id=?"""),([drawn_search_entry.get()]))
            result=cursor.fetchone()
            if result:
                warrant_id=result[4]
                cursor.execute(("""select customer_name,photo
                                from customer
                                where id=?"""),([warrant_id]))
                warrant_name=cursor.fetchone()
                
            cursor.close()
            db.commit()
            db.close()
            
            clear_drawn_entries()
            if result :
                drawn_customer_name_entry.insert(END,f'{result[6]} / {result[0]}')
                drawn_equb_type_entry.insert(END,result[1])
                drawn_date_entry.insert(END,result[2])
                drawn_amount_entry.insert(END,result[3])
                drawn_warrant_name_entry.insert(END,f'{result[4]} / {warrant_name[0]}')
                drawn_round_entry.insert(END,result[5])
                drawn_tax_entry.insert(END,result[8])
            
                display_profile_picture(result[7],drawn_profile_photo_label)
                display_profile_picture(warrant_name[1],drawn_warrant_profile_photo_label)
            
            else:
                drawn_total_label_info.config(text='')
                display_profile_picture(default_profile_photo,drawn_profile_photo_label)
                display_profile_picture(default_profile_photo,drawn_warrant_profile_photo_label)
        except:
            pass
        
    def fill_drawn_type_list():
        customer_id=(drawn_customer_name_entry.get()).split('/')[0]
        db=sqlite3.connect(database_name)
        cursor=db.cursor()
        cursor.execute("""select equb_type from equb_enrollment 
                       where customer_id=?""",[customer_id])
        drawn_status_result=cursor.fetchall()
        cursor.close()
        db.commit()
        db.close()
        result=fetch_data('*','equb_type')
        drawn_equb_type.clear()
        if result:
            for i in result:
                drawn_equb_type.append(i[1])
            drawn_equb_type_entry.config(values=drawn_equb_type)
            drawn_equb_type_entry.delete(0,END)
            drawn_equb_type_entry.insert(END,drawn_equb_type[-1])
    def fill_drawn_warrant_list_like():
        db=sqlite3.connect(database_name)
        cursor=db.cursor()
        cursor.execute("""select customer_id , customer.customer_name 
                       from equb_enrollment JOIN customer ON equb_enrollment.customer_id=customer.id 
                       where number_of_paid_lot>0 and
                       customer.customer_name like '%"""+drawn_warrant_name_entry.get()+"""%'and 
    
                       equb_type=(select id from equb_type where equb_type=?)""",[(drawn_equb_type_entry.get())])
        warrant_result=cursor.fetchall()
        cursor.close()
        db.commit()
        db.close()
        # result=fetch_data('*','equb_enrollment')
        
        drawn_warrant_list.clear()
        if warrant_result:
            for i in warrant_result:
                #drawn_warrant_list.append([i[0],'/',i[1]])
                if f"{i[0]} / {i[1]}" not in drawn_warrant_list:
                        drawn_warrant_list.append(f"{i[0]} / {i[1]}")
            drawn_warrant_name_entry.config(values=drawn_warrant_list)
            # drawn_warrant_name_entry.delete(0,END)
            # drawn_warrant_name_entry.insert(END,drawn_warrant_list[0])
    def fill_drawn_customer_list_like():
        db=sqlite3.connect(database_name)
        cursor=db.cursor()
        cursor.execute("""select customer_id , customer.customer_name 
                       from equb_enrollment JOIN customer ON 
                       equb_enrollment.customer_id=customer.id where number_of_paid_lot>0 and
                       customer.customer_name like '%"""+drawn_customer_name_entry.get()+"""%' and 
    
                        equb_type=(select id from equb_type where equb_type=?)""",[(drawn_equb_type_entry.get())])
                       
        
        customer_result=cursor.fetchall()
        cursor.close()
        db.commit()
        db.close()
        # result=fetch_data('*','equb_enrollment')
        
        drawn_customer_list.clear()
        if customer_result:
            for i in customer_result:
                #drawn_customer_list.append([i[0],'/',i[1]])
                if f"{i[0]} / {i[1]}" not in drawn_customer_list:
                        drawn_customer_list.append(f"{i[0]} / {i[1]}")
            drawn_customer_name_entry.config(values=drawn_customer_list)
            # drawn_customer_name_entry.delete(0,END)
            # drawn_customer_name_entry.insert(END,drawn_customer_list[-1])
    global fill_drawn_customer_list
    def fill_drawn_customer_list():
        
        try:
            db=sqlite3.connect(database_name)
            cursor=db.cursor()
            cursor.execute("""select customer_id , customer.customer_name 
                        from equb_enrollment JOIN customer ON 
                        equb_enrollment.customer_id=customer.id where number_of_paid_lot>0 and 
                        equb_type=(select id from equb_type where equb_type=?)""",[(drawn_equb_type_entry.get())])
            customer_result=cursor.fetchall()
            cursor.execute("""select customer_id , customer.customer_name 
                        from equb_enrollment JOIN customer ON equb_enrollment.customer_id=customer.id 
                        where number_of_paid_lot>0 and 
                        equb_type=(select id from equb_type where equb_type=?)""",[(drawn_equb_type_entry.get())])
            warrant_result=cursor.fetchall()
            cursor.close()
            db.commit()
            db.close()
            # result=fetch_data('*','equb_enrollment')
            
            drawn_customer_list.clear()
            if customer_result:
                for i in customer_result:
                    #drawn_customer_list.append([i[0],'/',i[1]])
                    if f"{i[0]} / {i[1]}" not in drawn_customer_list:
                        drawn_customer_list.append(f"{i[0]} / {i[1]}")
                drawn_customer_name_entry.config(values=drawn_customer_list)
                drawn_customer_name_entry.delete(0,END)
                # drawn_customer_name_entry.insert(END,drawn_customer_list[-1])
            else:
                drawn_customer_list.clear()
                drawn_customer_name_entry.config(values=drawn_customer_list)
                drawn_customer_name_entry.delete(0,END)
            drawn_warrant_list.clear()
            if warrant_result:
                for i in warrant_result:
                    #drawn_warrant_list.append([i[0],'/',i[1]])
                    if f"{i[0]} / {i[1]}" not in drawn_warrant_list:
                        drawn_warrant_list.append(f"{i[0]} / {i[1]}")
                drawn_warrant_name_entry.config(values=drawn_warrant_list)
                drawn_warrant_name_entry.delete(0,END)
                drawn_warrant_name_entry.insert(END,drawn_warrant_list[0])
            else:
                drawn_warrant_list.clear()
                drawn_warrant_name_entry.config(values=drawn_warrant_list)
                drawn_warrant_name_entry.delete(0,END)
        except: 
            pass
    def refresh_combo ():
        fill_drawn_type_list()
        fill_drawn_list()
        fill_drawn_customer_list()
        
    # refresh_combo ()
    def fill_current_round():
        try:
            db=sqlite3.connect(database_name)
            cursor=db.cursor()
            cursor.execute("""select * from round where
            equb_type_id=(select id from equb_type 
            where equb_type=? )""",[drawn_equb_type_entry.get()])
            result=cursor.fetchall()
            cursor.close()
            db.commit()
            db.close()
            drawn_round_entry.delete(0,END)
            drawn_round_entry.insert(END,result[0][2])
        except:
            pass
    def fill_drawn_total_amount_event(event):
        fill_drawn_total_amount()
    def fill_tax_event(event):
        fill_tax()
    def fill_tax():
        try:
            db=sqlite3.connect(database_name)
            cursor=db.cursor()
            cursor.execute(("""select amount*reg_number_of_paid_lot from equb_enrollment where 
                                equb_type=(select id from equb_type where equb_type=? and customer_id=?)"""),[(drawn_equb_type_entry.get()),drawn_customer_name_entry.get().split('/')[0]])
            result=cursor.fetchone()
            db.commit()
            db.close()
            if result:
                drawn_tax_entry.delete(0,END)
                drawn_tax_entry.insert(END,result)
        except:
            pass
    def fill_drawn_total_amount():
        # try:
        db=sqlite3.connect(database_name)
        cursor=db.cursor()
        cursor.execute(("""select sum(amount*reg_number_of_paid_lot) from equb_enrollment where 
                        equb_type=(select id from equb_type where equb_type=?)"""),[(drawn_equb_type_entry.get())])
        result=cursor.fetchone()
        
        # cursor.execute(("""select sum(amount) from pay_list where 
        #                 equb_type_id=(select id from equb_type where equb_type=?) and customer_id=?"""),[drawn_equb_type_entry.get(),drawn_customer_name_entry.get().split('/')[0]])
        # result=cursor.fetchone()
        cursor.close()
        db.commit()
        db.close()
        if result:
            drawn_amount_entry.delete(0,END)
            drawn_amount_entry.insert(END,result)
        fill_current_round()
        fill_drawn_date()
        # except:
        #     pass
    def drawn_customer():
        # fill_drawn_customer_list()
        try:
            customer_id=(drawn_customer_name_entry.get()).split('/')[0]
            warrant_id=(drawn_warrant_name_entry.get()).split('/')[0]
            db=sqlite3.connect(database_name)
            cursor=db.cursor()
            cursor.execute('select id from equb_type where equb_type=? ',[drawn_equb_type_entry.get()])
            equb_id=cursor.fetchall()
            
            cursor.execute('select current_round from round where equb_type_id=? ',[equb_id[0][0]])
            rounded=cursor.fetchall()
            updated_round=rounded[0][0]+1
            
            cursor.execute('select number_of_paid_lot from equb_enrollment where customer_id=? and equb_type=?',[customer_id,equb_id[0][0]])
            num_of_lot=cursor.fetchall()
            
            updated_num_of_lot=int(num_of_lot[0][0])-1
            
            cursor.execute("""insert into drawn_list ( customer_id,equb_type_id,drawn_date,amount_of_money,warrant_id,drawn_round,drawn_tax) values (?,?,?,?,?,?,?)""",(
                [(customer_id),
                equb_id[0][0],
                drawn_date_entry.get(),
                drawn_amount_entry.get(),
                warrant_id,
                drawn_round_entry.get(),
                drawn_tax_entry.get()
                ]
            ))
            cursor.execute('update round set current_round=? where equb_type_id=?',[updated_round,equb_id[0][0]])
            
            cursor.execute('update equb_enrollment set number_of_paid_lot=? where customer_id=? and equb_type=?',[updated_num_of_lot,customer_id,equb_id[0][0]])
            cursor.close()
            db.commit()
            db.close() 
            clear_drawn()
            drawn_total_label.config(text='')
            drawn_total_label_info.config(text='ብትክክል ተመዝጊቡ')
            drawn_total_label.after('3000',clear_drawn_total_label)
            drawn_total_label_info.after('3000',clear_drawn_total_label)
            fill_drawn_customer_list()
            fill_date(drawn_date_entry)
        except:
            pass
        
    def update_drawn():
        if len(drawn_search_entry.get())>0:
            try:
                customer_id=(drawn_customer_name_entry.get()).split('/')[0]
                warrant_id=(drawn_warrant_name_entry.get()).split('/')[0]
                db=sqlite3.connect(database_name)
                cursor=db.cursor()
                cursor.execute('select id from equb_type where equb_type=? ',[drawn_equb_type_entry.get()])
                equb_id=cursor.fetchall()
                cursor.execute('update drawn_list set customer_id=?,equb_type_id=?,drawn_date=?,amount_of_money=?,warrant_id=?,drawn_round=? , drawn_tax=? where id=?',(
                    [
                    customer_id,
                    equb_id[0][0],
                    drawn_date_entry.get(),
                    drawn_amount_entry.get(),
                    warrant_id,
                    drawn_round_entry.get(),
                    drawn_tax_entry.get(),
                    drawn_search_entry.get()
                    ]
                ))
                cursor.close()
                db.commit()
                db.close()
                clear_drawn()
                drawn_total_label.config(text='')
                drawn_total_label_info.config(text='ብትክክል ተመሓይሹ')
                drawn_total_label.after('3000',clear_drawn_total_label)
                drawn_total_label_info.after('3000',clear_drawn_total_label)
                fill_drawn_customer_list()
                fill_date(drawn_date_entry)
            except:
                pass
    def delete_drawn():
        if len(drawn_search_entry.get())>0:
            try:
                customer_id=(drawn_customer_name_entry.get()).split('/')[0]
                db=sqlite3.connect(database_name)
                cursor=db.cursor()
                cursor.execute('select id from equb_type where equb_type=? ',[drawn_equb_type_entry.get()])
                equb_id=cursor.fetchall()
                cursor.execute('select number_of_paid_lot from equb_enrollment where customer_id=? and equb_type=?',[customer_id,equb_id[0][0]])
                num_of_lot=cursor.fetchall()
                
                updated_num_of_lot=int(num_of_lot[0][0])+1
                cursor.execute('update equb_enrollment set number_of_paid_lot=? where customer_id=? and equb_type=?',[updated_num_of_lot,customer_id,equb_id[0][0]])
                cursor.execute('delete from drawn_list  where id=?',(
                    [
                    drawn_search_entry.get()
                    ]
                ))
                cursor.close()
                db.commit()
                db.close()
                clear_drawn()
                drawn_total_label.config(text='')
                drawn_total_label_info.config(text='ብትክክል ጠፊኡ')
                drawn_total_label.after('3000',clear_drawn_total_label)
                drawn_total_label_info.after('3000',clear_drawn_total_label)
                fill_drawn_customer_list()
                fill_date(drawn_date_entry)
            except:
                pass
    def fill_warrant_profile_photo_event(event):
        fill_warrant_profile_photo()  
        fill_drawn_warrant_list_like()
    def fill_warrant_profile_photo():
        try:
            customer_id=(drawn_warrant_name_entry.get()).split('/')[0]
            
            warrant_photo=fetch_data_by_id('*','customer',customer_id)
            if warrant_photo:
                new_warrant_photo=warrant_photo[5]
                display_profile_picture(new_warrant_photo,drawn_warrant_profile_photo_label)
            else:
                display_profile_picture(default_profile_photo,drawn_warrant_profile_photo_label)
        except:
            pass
    def fill_drawn_list_event(event):
        fill_drawn_list()
    
    def fill_drawn_list():
        result=fetch_data('*','equb_type')
        
        drawn_equb_type.clear()
        if result:
            for i in result:
                drawn_equb_type.append(i[1])
            drawn_equb_type_entry.config(values=drawn_equb_type)
            drawn_equb_type_entry.delete(0,END)
            drawn_equb_type_entry.insert(END,drawn_equb_type[0])
    drawn_title=ttk.Label(drawn_frame,text='ዕጫ መውፅኢ ',font=('arial',15,'bold') ,foreground='purple')
    drawn_title.grid(row=0,column=0,padx=20,pady=5,sticky='w')

    drawn_customer_name_label=ttk.Label(drawn_frame,text='ዕጫ ዝበፅሖ ዓሚል')
    drawn_customer_name_label.grid(row=2,column=0,padx=3,pady=3,sticky='w')
    drawn_customer_name_entry=ttk.Combobox(drawn_frame,width=33,values=drawn_customer_list)
    drawn_customer_name_entry.grid(row=3,column=0,padx=3,pady=3)
    drawn_customer_name_entry.bind('<Up>',lambda e: drawn_search_entry.focus())
    drawn_customer_name_entry.bind('<Down>',lambda e: drawn_equb_type_entry.focus())
    # drawn_customer_name_entry.insert(END.set('')
    drawn_customer_name_entry.bind('<KeyRelease>',lambda e:fill_drawn_customer_list_like())
    drawn_customer_name_entry.bind('<FocusIn>',draw_winner_event)
    # drawn_customer_name_entry.focus()
   
    drawn_search_label=ttk.Label(drawn_frame,image=search_photo)
    drawn_search_label.grid(row=1,column=0,padx=3,pady=3,sticky='e')
    drawn_search_entry=ttk.Entry(drawn_frame,width=30)
    drawn_search_entry.grid(row=1,column=0,padx=3,pady=3,sticky='w')
    
    drawn_search_entry.bind('<Down>',lambda e:drawn_customer_name_entry.focus())
    drawn_search_entry.bind('<Up>',lambda e:drawn_round_entry.focus() )

    # def genterate_id(event):
    #    print(drawn_customer_name_entry.get())
   
    drawn_equb_type_label=ttk.Label(drawn_profile_photo_frame,text='ዓይነት ዕቑብ ብምምራፅ ዕጫ ኣውድቑ!')
    drawn_equb_type_label.grid(row=0,column=0,padx=3,pady=3,sticky='w')
    drawn_equb_type_entry=ttk.Combobox(drawn_profile_photo_frame,width=29,values=drawn_equb_type)
    drawn_equb_type_entry.grid(row=1,column=0,padx=3,pady=5,sticky='w')
    drawn_equb_type_entry.bind('<Up>',lambda e:drawn_customer_name_entry.focus())
    drawn_equb_type_entry.bind('<Down>',lambda e:drawn_date_entry.focus())
    drawn_equb_type_entry.focus()
    drawn_equb_type_entry.bind('<FocusIn>',lambda e:fill_drawn_customer_list())
    drawn_generate_random_button=ttk.Button(drawn_profile_photo_frame,text='ዕጫ ኣውድቕ',width=30,command=draw_winner)
    drawn_generate_random_button.grid(row=2,column=0,padx=3,pady=10,sticky='w')
    drawn_notification_label=ttk.Label(drawn_profile_photo_frame,text='',width=31)
    drawn_notification_label.grid(row=3,column=0,padx=3,pady=10,sticky='w')
    fill_drawn_type_list()
    fill_drawn_list()
    
    drawn_date_label=ttk.Label(drawn_frame,text='ዕጫ ዝወፀሉ ዕለት')
    drawn_date_label.grid(row=6,column=0,padx=3,pady=3,sticky='w')
    drawn_date_entry=ttk.Entry(drawn_frame,width=30)
    drawn_date_entry.grid(row=7,column=0,padx=3,pady=3,sticky='w')
    drawn_date_entry.bind('<Up>',lambda e:drawn_equb_type_entry.focus())
    drawn_date_entry.bind('<Down>',lambda e:drawn_amount_entry.focus())
    fill_date(drawn_date_entry)
    drawn_fill_date_button=ttk.Button(drawn_frame,text='⏱️',width=3,command=lambda : fill_date(drawn_date_entry))
    drawn_fill_date_button.grid(row=7,column=0,padx=3,pady=3,sticky='e')

    def calculate_drawn_total_event(event):
        calculate_drawn_total()
    def calculate_drawn_total():
        try:
            
                
            drawn_total_label_info.config(text=(float(drawn_amount_entry.get())- float(drawn_tax_entry.get())))
        # 1print(float(drawn_amount_entry.get())- float((float(drawn_tax_entry.get())/100)*float(drawn_amount_entry.get())))
        except:
            drawn_total_label_info.config(text='')
    drawn_amount_label=ttk.Label(drawn_frame,text='መጠን ገንዘብ')
    drawn_amount_label.grid(row=8,column=0,padx=3,pady=3,sticky='w')
    drawn_amount_entry=ttk.Entry(drawn_frame,width=35)
    drawn_amount_entry.grid(row=9,column=0,padx=3,pady=3)
    drawn_amount_entry.bind('<Up>',lambda e:drawn_date_entry.focus())
    drawn_amount_entry.bind('<Down>',lambda e:drawn_warrant_name_entry.focus())
    drawn_amount_entry.bind('<KeyRelease>',calculate_drawn_total_event)

    drawn_tax_label=ttk.Label(drawn_frame,text='ተቖራፂ ገንዘብ ')
    drawn_tax_label.grid(row=10,column=0,padx=3,pady=3,sticky='w')
    drawn_tax_entry=ttk.Entry(drawn_frame,width=35)
    drawn_tax_entry.grid(row=11,column=0,padx=3,pady=3)
    drawn_tax_entry.bind('<Up>',lambda e: drawn_amount_entry.focus())
    drawn_tax_entry.bind('<Down>',lambda e: drawn_round_entry.focus())
    drawn_tax_entry.bind('<KeyRelease>',calculate_drawn_total_event)
    drawn_tax_entry.bind('<FocusIn>',calculate_drawn_total_event)
    
    
    drawn_warrant_name_label=ttk.Label(drawn_frame,text='ናይ ወሓስ ሽም ምረፁ')
    drawn_warrant_name_label.grid(row=12,column=0,padx=3,pady=3,sticky='w')
    drawn_warrant_name_entry=ttk.Combobox(drawn_frame,width=33,values=drawn_customer_list)
    drawn_warrant_name_entry.grid(row=13,column=0,padx=3,pady=3)
    drawn_warrant_name_entry.bind('<Up>',lambda e: drawn_amount_entry.focus())
    drawn_warrant_name_entry.bind('<Down>',lambda e: drawn_round_entry.focus())
    drawn_warrant_name_entry.bind('<KeyRelease>',fill_warrant_profile_photo_event)
    drawn_warrant_name_entry.bind('<FocusIn>',fill_warrant_profile_photo_event)
    
    
    
    fill_drawn_customer_list()

    drawn_round_label=ttk.Label(drawn_frame,text='ዕጫ ዝወደቐሉ ዙር')
    drawn_round_label.grid(row=14,column=0,padx=3,pady=3,sticky='w')
    drawn_round_entry=ttk.Entry(drawn_frame,width=35)
    drawn_round_entry.grid(row=15,column=0,padx=3,pady=3)
    drawn_round_entry.bind('<Up>',lambda e:drawn_warrant_name_entry.focus())
    drawn_round_entry.bind('<Down>',lambda e:drawn_search_entry.focus())

    drawn_total_label=ttk.Label(drawn_frame,text='ጠቕላላ ገንዘብ')
    drawn_total_label.grid(row=16,column=0,padx=3,pady=3,sticky='w')

    drawn_total_label_info=ttk.Label(drawn_frame,text='')
    drawn_total_label_info.grid(row=16,column=0,padx=3,pady=3)

    
    drawn_search_entry.bind('<KeyRelease>',find_and_fill_drawn_entries)
    drawn_search_entry.bind('<FocusIn>',find_and_fill_drawn_entries)
    
    drawn_register_button=ttk.Button(drawn_frame,width=10,text='መዝግብ',command=drawn_customer,style='save.TButton')
    drawn_register_button.grid(row=18,column=0,padx=3,pady=3,sticky='w')

    drawn_update_button=ttk.Button(drawn_frame,width=10,text='ኣመሓይሽ',style='update.TButton',command=update_drawn)
    drawn_update_button.grid(row=18,column=0,padx=3,pady=3)

    drawn_delete_button=ttk.Button(drawn_frame,width=10,text='ኣጥፍእ',style='delete.TButton',command=delete_drawn)
    drawn_delete_button.grid(row=18,column=0,padx=3,pady=3,sticky='e')

#*************************************customer list table with scroll bar**********************
    def fetch_customer_and_insert_into_table():
        
        result=fetch_data('*','customer')
        list_of_customers.delete(*list_of_customers.get_children())
        if result:
            for i in result:
                list_of_customers.insert('','end',values=(i[0],i[1],i[2],i[3],i[4],i[5]))  
    def fetch_customer_and_insert_into_table_like():
        try:
            db=sqlite3.connect(database_name)
            cursor=db.cursor()
            cursor.execute("""select * from customer where customer_name like 
                    '%"""+table_search_entry.get()+"""%'""")
            result=cursor.fetchall()
            cursor.close()
            db.commit()
            db.close()
            list_of_customers.delete(*list_of_customers.get_children())
            if result:
                for i in result:
                    list_of_customers.insert('','end',values=(i[0],i[1],i[2],i[3],i[4],i[5]))
        except:
            pass
    def customer_enter_event(event):
        item_number=list_of_customers.selection()
        selected_value=list_of_customers.item(item_number)
        selected_id=selected_value['values'][0]
        if type(selected_id)==int:
            main_notebook.select(0)
            display_register_customer_frame()
            search_customer.delete(0,END)
            search_customer.insert(END,selected_id )
            search_customer_and_fill()
    def customer_treeview_event(event):
        list_of_customers.bind('<Return>',customer_enter_event)
        list_of_customers.bind("<Double-Button-1>",customer_enter_event)
    
    def fetch_pay_and_insert_into_table_like():
        try:
            db=sqlite3.connect(database_name)
            cursor=db.cursor()
            cursor.execute("""select pay_list.id , customer.customer_name,equb_type.equb_type,amount ,unpaid_amount,
                        paid_round ,punished_amount, paid_date from pay_list
                        JOIN customer ON pay_list.customer_id=customer.id 
                        JOIN equb_type ON pay_list.equb_type_id=equb_type.id
                        where customer.customer_name like '%"""+table_search_entry.get()+"""%' and pay_list.equb_type_id=(select id from equb_type
                        where equb_type=?) """,[table_equb_type_entry.get()])
            result=cursor.fetchall()
            print('resutl',result)
            cursor.execute("""select 
                        sum(amount) , sum(unpaid_amount),sum(punished_amount), customer.customer_name 
                            from pay_list JOIN customer ON pay_list.customer_id=customer.id 
                        where customer.customer_name like '%"""+table_search_entry.get()+"""%' and 
                        pay_list.equb_type_id=(select id from equb_type
                        where equb_type=?)  """,[table_equb_type_entry.get()])
            sum_result=cursor.fetchone()
            
            cursor.close()
            db.commit()
            db.close()
            list_of_customers.delete(*list_of_customers.get_children())
            if result:
                
                for i in result:
                        list_of_customers.insert('','end',values=(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7])) 
                if sum_result:

                    list_of_customers.insert('','end',values=("","","","ጠቕላላ ዝተከፈለ ገንዘብ","ድምር ዘይተኸፈለ ገንዘብ","","ጠቕላላ ቅፅዓት",""))
                    list_of_customers.insert('','end',values=("","","",sum_result[0],sum_result[1],"",sum_result[2],""))
        except:
            pass
    
    def fetch_pay_and_insert_into_table():
        try:
            db=sqlite3.connect(database_name)
            cursor=db.cursor()
            cursor.execute("""select pay_list.id , customer.customer_name,equb_type.equb_type,amount , unpaid_amount ,
                        paid_round ,punished_amount, paid_date from pay_list
                        JOIN customer ON pay_list.customer_id=customer.id 
                        JOIN equb_type ON pay_list.equb_type_id=equb_type.id
                        where pay_list.equb_type_id=(select id from equb_type
                        where equb_type=?) """,[table_equb_type_entry.get()])
            result=cursor.fetchall()
            cursor.execute("""select sum(amount) , sum(unpaid_amount), 
                            sum(punished_amount) from pay_list 
                        where pay_list.equb_type_id=(select id from equb_type
                        where equb_type=?)  """,[table_equb_type_entry.get()])
            sum_result=cursor.fetchone()
            cursor.close()
            db.commit()
            db.close()
            list_of_customers.delete(*list_of_customers.get_children())
            
            if result:
                for i in result:
                    list_of_customers.insert('','end',values=(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7])) 
                if sum_result:
                    list_of_customers.insert('','end',values=("","","","ጠቕላላ ዝተከፈለ ገንዘብ","ድምር ዘይተኸፈለ ገንዘብ","","ጠቕላላ ቅፅዓት",""))
                    list_of_customers.insert('','end',values=("","","",sum_result[0],sum_result[1],"",sum_result[2],""))
        except:
            pass
    def pay_enter_event(event):
        item_number=list_of_customers.selection()
        selected_value=list_of_customers.item(item_number)
        selected_id=selected_value['values'][0]
        if type(selected_id)==int:
            main_notebook.select(0)
            display_payment_frame()
            payment_search_entry.delete(0,END)
            payment_search_entry.insert(END,selected_id )
            find_and_fill_payment_entries_after()
    def pay_treeview_event(event):
        list_of_customers.bind('<Return>',pay_enter_event)
        list_of_customers.bind("<Double-Button-1>",pay_enter_event)
        
    def fetch_unpayed_and_insert_into_table_like():
        try:
            db=sqlite3.connect(database_name)
            cursor=db.cursor()
            cursor.execute("select id from equb_type where equb_type=?",[table_equb_type_entry.get()])
            equb_id_result=cursor.fetchone()
            
            if equb_id_result:

                cursor.execute("""
                            select  equb_enrollment.id , customer.customer_name,equb_type.equb_type,amount ,reg_number_of_paid_lot, 
                            (amount *reg_number_of_paid_lot)  from equb_enrollment 
                            JOIN customer ON equb_enrollment.customer_id=customer.id 
                            JOIN equb_type ON equb_enrollment.equb_type=equb_type.id
                            where equb_enrollment.customer_id NOT IN
                            (select pay_list.customer_id from pay_list where 
                            paid_round=? and pay_list.equb_type_id=?) and customer.customer_name
                            like '%"""+table_search_entry.get()+"""%' 
                            and equb_enrollment.equb_type=?
                            """,[table_round_entry.get(),equb_id_result[0],equb_id_result[0]])         
                result=cursor.fetchall()
                cursor.execute("""select 
                            sum(amount) ,sum(reg_number_of_paid_lot), sum(amount * reg_number_of_paid_lot) as net
                                from equb_enrollment
                                JOIN customer ON equb_enrollment.customer_id=customer.id 
                                where equb_enrollment.customer_id NOT IN
                            (select pay_list.customer_id from pay_list where 
                            paid_round=? and pay_list.equb_type_id=?) and customer.customer_name
                            like '%"""+table_search_entry.get()+"""%' 
                            and equb_enrollment.equb_type=?
                            """,[table_round_entry.get(),equb_id_result[0],equb_id_result[0]])
                sum_result=cursor.fetchone()
            
                list_of_customers.delete(*list_of_customers.get_children())
                if result:
                    for i in result:
                        list_of_customers.insert('','end',values=(i[0],i[1],i[2],i[3],i[4],i[5])) 
                    if sum_result:
                        list_of_customers.insert('','end',values=("","",""," ","ጠቕላላ ዘይተኸፈለ ዕጫ","ጠቕላላ ገንዘብ"))
                        list_of_customers.insert('','end',values=("","","","",sum_result[1],sum_result[2]))
                else:
                    list_of_customers.delete(*list_of_customers.get_children())
        
            cursor.close()
            db.commit()
            db.close()
        except:
            pass
    def fetch_unpayed_and_insert_into_table():
        try:
            db=sqlite3.connect(database_name)
            cursor=db.cursor()
            cursor.execute("select id from equb_type where equb_type=?",[table_equb_type_entry.get()])
            equb_id_result=cursor.fetchone()
            
            if equb_id_result:

                cursor.execute("""
                            select  equb_enrollment.id , customer.customer_name,equb_type.equb_type,amount ,reg_number_of_paid_lot, 
                            (amount *reg_number_of_paid_lot)  from equb_enrollment 
                            JOIN customer ON equb_enrollment.customer_id=customer.id 
                            JOIN equb_type ON equb_enrollment.equb_type=equb_type.id
                            where equb_enrollment.customer_id NOT IN
                            (select pay_list.customer_id from pay_list where  
                            paid_round=? and pay_list.equb_type_id=?) 
                            and equb_enrollment.equb_type=?
                            """,[table_round_entry.get(),equb_id_result[0],equb_id_result[0]])         
                result=cursor.fetchall()

                cursor.execute("""select 
                            sum(amount) ,sum(number_of_paid_lot), sum(amount * number_of_paid_lot) as net
                                from equb_enrollment
                                where equb_enrollment.customer_id NOT IN
                            (select pay_list.customer_id from pay_list where 
                            paid_round=? and pay_list.equb_type_id=?) 
                            and equb_enrollment.equb_type=?
                            """,[table_round_entry.get(),equb_id_result[0],equb_id_result[0]])
                sum_result=cursor.fetchone()
            
                list_of_customers.delete(*list_of_customers.get_children())
                if result:
                    for i in result:
                        list_of_customers.insert('','end',values=(i[0],i[1],i[2],i[3],i[4],i[5])) 
                    if sum_result:
                        list_of_customers.insert('','end',values=("","",""," ","ጠቕላላ ዘይተኸፈለ ዕጫ","ጠቕላላ ገንዘብ"))
                        list_of_customers.insert('','end',values=("","","","",sum_result[1],sum_result[2]))
                else:
                    list_of_customers.delete(*list_of_customers.get_children())
        
            cursor.close()
            db.commit()
            db.close()
        except:
            pass
    
    def fetch_enrollment_and_insert_into_table_like():
        try:
            db=sqlite3.connect(database_name)
            cursor=db.cursor()
            cursor.execute("""select equb_enrollment.id , customer.customer_name,equb_type.equb_type,amount ,reg_number_of_paid_lot, 
                        (amount * reg_number_of_paid_lot),number_of_paid_lot , paid_date from equb_enrollment 
                        JOIN customer ON equb_enrollment.customer_id=customer.id 
                        JOIN equb_type ON equb_enrollment.equb_type=equb_type.id
                        where customer.customer_name like '%"""+table_search_entry.get()+"""%' and equb_enrollment.equb_type=(select id from equb_type
                        where equb_type=?)""",[table_equb_type_entry.get()])
            result=cursor.fetchall()
            cursor.execute("""select 
                        sum(amount) ,sum(reg_number_of_paid_lot), sum(amount * reg_number_of_paid_lot) , 
                        sum(number_of_paid_lot) as net , customer.customer_name
                            from equb_enrollment  JOIN customer ON equb_enrollment.customer_id=customer.id 
                            where customer.customer_name like
                            '%"""+table_search_entry.get()+"""%' and  
                            equb_enrollment.equb_type=(select id from equb_type
                        where equb_type=?)""",[table_equb_type_entry.get()])
            sum_result=cursor.fetchone()
            cursor.close()
            db.commit()
            db.close()
            list_of_customers.delete(*list_of_customers.get_children())
            
            if result:
                for i in result:
                    list_of_customers.insert('','end',values=(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7])) 
                if sum_result:
                    list_of_customers.insert('','end',values=("","","","","ጠቕላላ በዝሒ ዕጫ","ድምር","ጠቕላላ ዕጫ ዘይበፅሖም",""))
                    list_of_customers.insert('','end',values=("","","","",sum_result[1],sum_result[2],sum_result[3],""))
        except:
            pass
    
    
    def fetch_enrollment_and_insert_into_table():
        try:
            db=sqlite3.connect(database_name)
            cursor=db.cursor()
            cursor.execute("""select equb_enrollment.id , customer.customer_name,equb_type.equb_type,amount ,reg_number_of_paid_lot, 
                        (amount * reg_number_of_paid_lot),number_of_paid_lot , paid_date from equb_enrollment 
                        JOIN customer ON equb_enrollment.customer_id=customer.id 
                        JOIN equb_type ON equb_enrollment.equb_type=equb_type.id
                        where equb_enrollment.equb_type=(select id from equb_type
                        where equb_type=?)""",[table_equb_type_entry.get()])
            result=cursor.fetchall()
            cursor.execute("""select 
                        sum(amount) ,sum(reg_number_of_paid_lot), sum(amount * reg_number_of_paid_lot) , sum(number_of_paid_lot) as net
                            from equb_enrollment where equb_enrollment.equb_type=(select id from equb_type
                        where equb_type=?)""",[table_equb_type_entry.get()])
            sum_result=cursor.fetchone()
            cursor.close()
            db.commit()
            db.close()
            list_of_customers.delete(*list_of_customers.get_children())
            
            if result:
                for i in result:
                    list_of_customers.insert('','end',values=(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7])) 
                if sum_result:
                    list_of_customers.insert('','end',values=("","","","","ጠቕላላ በዝሒ ዕጫ","ድምር","ጠቕላላ ዕጫ ዘይበፅሖም",""))
                    list_of_customers.insert('','end',values=("","","","",sum_result[1],sum_result[2],sum_result[3],""))
        except:
            pass
    def fetch_undrawn_customer_and_insert_into_table_like():
        try:
            db=sqlite3.connect(database_name)
            cursor=db.cursor()
            cursor.execute("""select equb_enrollment.id , customer.customer_name,equb_type.equb_type,
                        number_of_paid_lot  from equb_enrollment 
                        JOIN customer ON equb_enrollment.customer_id=customer.id 
                        JOIN equb_type ON equb_enrollment.equb_type=equb_type.id
                        where customer.customer_name like '%"""+table_search_entry.get()+"""%' and equb_enrollment.equb_type=(select id from equb_type
                        where equb_type=?) and number_of_paid_lot>0""",[table_equb_type_entry.get()])
            result=cursor.fetchall()
            cursor.execute("""select 
                        
                        sum(number_of_paid_lot) as net , customer.customer_name
                            from equb_enrollment  JOIN customer ON equb_enrollment.customer_id=customer.id 
                            where customer.customer_name like
                            '%"""+table_search_entry.get()+"""%' and  
                            equb_enrollment.equb_type=(select id from equb_type
                        where equb_type=?) and number_of_paid_lot>0""",[table_equb_type_entry.get()])
            sum_result=cursor.fetchone()
            cursor.close()
            db.commit()
            db.close()
            list_of_customers.delete(*list_of_customers.get_children())
            
            if result:
                for i in result:
                    list_of_customers.insert('','end',values=(i[0],i[1],i[2],i[3])) 
                if sum_result:
                    list_of_customers.insert('','end',values=("","","","ጠቕላላ ዕጫ ዘይበፅሖም"))
                    list_of_customers.insert('','end',values=("","","",sum_result[0]))
        except:
            pass
    def fetch_undrawn_customer_and_insert_into_table():
        try:
            db=sqlite3.connect(database_name)
            cursor=db.cursor()
            cursor.execute("""select equb_enrollment.id , customer.customer_name,equb_type.equb_type,
                       number_of_paid_lot  from equb_enrollment 
                        JOIN customer ON equb_enrollment.customer_id=customer.id 
                        JOIN equb_type ON equb_enrollment.equb_type=equb_type.id
                        where equb_enrollment.equb_type=(select id from equb_type
                        where equb_type=?) and number_of_paid_lot>0""",[table_equb_type_entry.get()])
            result=cursor.fetchall()
            
            cursor.execute("""select 
                         sum(number_of_paid_lot) as net
                            from equb_enrollment where equb_enrollment.equb_type=(select id from equb_type
                        where equb_type=?) and number_of_paid_lot>0""",[table_equb_type_entry.get()])
            sum_result=cursor.fetchone()
            cursor.close()
            db.commit()
            db.close()
            list_of_customers.delete(*list_of_customers.get_children())
            
            if result:
                for i in result:
                    list_of_customers.insert('','end',values=(i[0],i[1],i[2],i[3])) 
                if sum_result:
                    list_of_customers.insert('','end',values=("","","","ጠቕላላ ዕጫ ዘይበፅሖም"))
                    list_of_customers.insert('','end',values=("","","",sum_result[0]))
        except:
            pass
    def enrollment_enter_event(event):
        item_number=list_of_customers.selection()
        selected_value=list_of_customers.item(item_number)
        selected_id=selected_value['values'][0]
        if type(selected_id)==int:
            main_notebook.select(0)
            display_enrollment_frame()
            enrollment_search_entry.delete(0,END)
            enrollment_search_entry.insert(END,selected_id )
            find_and_fill_enrollment_entries_after()
    def enrollment_treeview_event(event):
        list_of_customers.bind('<Return>',enrollment_enter_event)
        list_of_customers.bind("<Double-Button-1>",enrollment_enter_event)
        
    def fetch_drawn_and_insert_into_table_like():
        
        try:
        # if len(table_round_entry.get())>0:
            db=sqlite3.connect(database_name)
            cursor=db.cursor()
            cursor.execute("""select drawn_list.id , customers.customer_name as customers_name ,equb_type.equb_type,
                        drawn_list.amount_of_money ,drawn_tax ,(drawn_list.amount_of_money-drawn_tax) as total 
                        , warrant.customer_name as warrant_name  ,drawn_round , drawn_date from drawn_list
                        JOIN customer customers ON drawn_list.customer_id=customers.id 
                        JOIN equb_type ON drawn_list.equb_type_id=equb_type.id
                        JOIN customer warrant ON drawn_list.warrant_id=warrant.id 
                        where customers.customer_name like
                            '%"""+table_search_entry.get()+"""%' and
                            drawn_list.equb_type_id=(select id from equb_type
                        where equb_type=?) and drawn_round=?""",[table_equb_type_entry.get(),table_round_entry.get()])
            result=cursor.fetchall()
            cursor.execute("""select 
                        sum(amount_of_money) ,sum(drawn_tax), sum(amount_of_money - drawn_tax) as net,
                        customers.customer_name
                            from drawn_list 
                            JOIN customer customers ON drawn_list.customer_id=customers.id
                        where customers.customer_name like
                            '%"""+table_search_entry.get()+"""%' and
                            drawn_list.equb_type_id=(select id from equb_type
                        where equb_type=?) and drawn_round=?""",[table_equb_type_entry.get(),table_round_entry.get()])
            sum_result=cursor.fetchone()
            cursor.close()
            db.commit()
            db.close()
            list_of_customers.delete(*list_of_customers.get_children())
            if result:
                for i in result:
                    list_of_customers.insert('','end',values=(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8])) 
                if sum_result:
                    list_of_customers.insert('','end',values=("","","","ጠቕላል ገንዘብ","ጠቕላላ ዝተቖረፀ ገንዘብ","ድምር","","",""))
                    list_of_customers.insert('','end',values=("","","",sum_result[0],sum_result[1],sum_result[2],"","",""))
        except:
            pass
        
    def fetch_drawn_and_insert_into_table():
        try:
            
            db=sqlite3.connect(database_name)
            cursor=db.cursor()
            cursor.execute("""select drawn_list.id , customers.customer_name as customers_name ,equb_type.equb_type,
                        drawn_list.amount_of_money ,drawn_tax ,(drawn_list.amount_of_money-drawn_tax) as total 
                        , warrant.customer_name as warrant_name  ,drawn_round , drawn_date from drawn_list
                        JOIN customer customers ON drawn_list.customer_id=customers.id 
                        JOIN equb_type ON drawn_list.equb_type_id=equb_type.id
                        JOIN customer warrant ON drawn_list.warrant_id=warrant.id 
                        where drawn_list.equb_type_id=(select id from equb_type
                        where equb_type=?)  """,[table_equb_type_entry.get()])
            result=cursor.fetchall()
            cursor.execute("""select 
                        sum(amount_of_money) ,sum(drawn_tax), sum(amount_of_money - drawn_tax) as net
                            from drawn_list 
                        where drawn_list.equb_type_id=(select id from equb_type
                        where equb_type=?) """,[table_equb_type_entry.get()])
            sum_result=cursor.fetchone()
            cursor.close()
            db.commit()
            db.close()
            list_of_customers.delete(*list_of_customers.get_children())
            if result:
                for i in result:
                    list_of_customers.insert('','end',values=(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8])) 
                if sum_result:
                    list_of_customers.insert('','end',values=("","","","ጠቕላል ገንዘብ","ጠቕላላ ዝተቖረፀ ገንዘብ","ድምር","","",""))
                    list_of_customers.insert('','end',values=("","","",sum_result[0],sum_result[1],sum_result[2],"","",""))
        except:
            pass
    def drawn_enter_event(event):
        item_number=list_of_customers.selection()
        selected_value=list_of_customers.item(item_number)
        selected_id=selected_value['values'][0]
        if type(selected_id)==int:
            main_notebook.select(1)
            drawn_search_entry.delete(0,END)
            drawn_search_entry.insert(END,selected_id )
            find_and_fill_drawn_entries_after()
            
    def drawn_treeview_event(event):
        list_of_customers.bind('<Return>',drawn_enter_event)
        list_of_customers.bind("<Double-Button-1>",drawn_enter_event)
 
 
 #************************************************************************************   
    def refresh_table_list():
        table_option.config(values=table_list)
        table_option.delete(0,END)
        table_option.insert(END,table_list[0])
        fetch_customer_and_insert_into_table()
    customer_title_list=["መለለዪ ቁፅሪ" ,"ሽም ዓሚል" ,"ስልኪ ቁፅሪ","ኣድራሻ" ,"ዝተመዝገበሉ ዕለት"]
    enrollment_title_list=["መለለዪ ቁፅሪ","ሽም ዓሚል", "ዓይነት ዕቑብ", " መጠን ገንዘብ","በዝሒ ዕጫ","ጠቅላላ ገንዘብ","ዘይወደቐ ዕጫ","ዕቁብ ዝኣተውሉ ዕለት"]
    pay_title_list=["መለለዪ ቁፅሪ","ሽም ዓሚል", "ዓይነት ዕቑብ", " ዝተኸፈለ ገንዘብ","ተረፍ ዘይተኸፈለ","ዝተከፈለሉ ዙር","ቅፅዓት","ዝተከፈለሉ ዕለት"]
    drawn_title_list=["መለለዪ ቁፅሪ","ሽም ዓሚል", "ዓይነት ዕቑብ", " ጠቕላላ ገንዘብ","ዝተቀነሰ ገንዘብ","ዝተወሰደ ገንዘብ","ሽም ወሓስ","ዕጫ ዝበፅሖም ዙር","ዕጫ ዝወደቐሉ ዕለት"]
    undrawn_title_list=["መለለዪ ቁፅሪ","ሽም ዓሚል", "ዓይነት ዕቑብ","በዝሒ ዕጫ"]
    
    table_list=["ዝርዝር ዘይከፈሉ","ናይ ዕቁብ መዝገብ","ዝርዝር ዝኸፈሉ","ዝርዝር ዓሚል","ዕጫ ዝበፅሖም","ዕጫ ዘይበፅሖም"]
    unpaid_title_list=["መለለዪ ቁፅሪ","ሽም ዓሚል", "ዓይነት ዕቑብ", " ዘይተኸፈለ ገንዘብ","ዘይተከፈለ ዕጫ","ጠቕላላ"]
    def fill_table_equb_type():
        result=fetch_data("*","equb_type")
        equb_type.clear()
        for i in result:
            equb_type.append(i[1])
        table_equb_type_entry.config(values=equb_type)
        table_equb_type_entry.delete(0,END)
        table_equb_type_entry.insert(END,equb_type[0])
    
    
    def fill_table_round_entry_event():
        fill_table_round_entry()
    def fill_table_round_entry():
        
        current_round=(return_current_round(table_equb_type_entry.get()) )
        table_round_entry.delete(0,END)
        table_round_entry.insert(END,current_round[0])
    
    def customize_table():  
        if table_option.get()=="ዝርዝር ዓሚል": 
            title_list=customer_title_list
            length=len(customer_title_list)
            list_of_customers.config(columns=(1,2,3,4,5),show='headings',selectmode='browse')
            # list_of_customers.delete(*list_of_customers.get_children())
            
            fetch_customer_and_insert_into_table()
            list_of_customers.bind('<<TreeviewSelect>>',customer_treeview_event)
        elif table_option.get()=="ናይ ዕቁብ መዝገብ":
            title_list=enrollment_title_list
            length=len(enrollment_title_list)
            list_of_customers.config(columns=(1,2,3,4,5,6,7,8),show='headings',selectmode='browse')
            # list_of_customers.delete(*list_of_customers.get_children())
            fetch_enrollment_and_insert_into_table()
            list_of_customers.bind('<<TreeviewSelect>>',enrollment_treeview_event)
        elif table_option.get()=="ዝርዝር ዝኸፈሉ" :
            title_list=pay_title_list
            length=len(pay_title_list)
            
            list_of_customers.config(columns=(1,2,3,4,5,6,7,8),show='headings',selectmode='browse')
            # list_of_customers.delete(*list_of_customers.get_children())
            fetch_pay_and_insert_into_table()
            list_of_customers.bind('<<TreeviewSelect>>',pay_treeview_event)
        elif table_option.get()=="ዝርዝር ዘይከፈሉ":
            title_list=unpaid_title_list
            length=len(unpaid_title_list)
            list_of_customers.config(columns=(1,2,3,4,5,6),show='headings',selectmode='browse')
            
            list_of_customers.delete(*list_of_customers.get_children())
            fetch_unpayed_and_insert_into_table()
            # list_of_customers.bind('<<TreeviewSelect>>',pay_treeview_event)
        elif table_option.get()=="ዕጫ ዝበፅሖም":
            title_list=drawn_title_list
            length=len(drawn_title_list)
            list_of_customers.config(columns=(1,2,3,4,5,6,7,8,9),show='headings',selectmode='browse')
            # list_of_customers.delete(*list_of_customers.get_children())
            fetch_drawn_and_insert_into_table()
            list_of_customers.bind('<<TreeviewSelect>>',drawn_treeview_event)
        elif table_option.get()=="ዕጫ ዘይበፅሖም":
            title_list=undrawn_title_list
            length=len(undrawn_title_list)
            list_of_customers.config(columns=(1,2,3,4),show='headings',selectmode='browse')
            # 
            fetch_undrawn_customer_and_insert_into_table()
            # list_of_customers.bind('<<TreeviewSelect>>',drawn_treeview_event)
        list_of_customers.column(1,width=80,minwidth=80)
        list_of_customers.heading(1,text=title_list[0],anchor='sw')
        for i in range(2,length+1):
            list_of_customers.column(i,width=140,minwidth=140)
            list_of_customers.heading(i,text=title_list[i-1],anchor='sw')
    
    def table_option_event(event):
        table_option_function()
        # fill_table_round_entry()
    def table_option_function():
        try:
            current_round=(return_current_round(table_equb_type_entry.get()) )
            check_table_query_entries()
            customize_table()
            table_reached_round_label.config(text='')
            table_reached_round_label.config(text=f'ሕዚ ዘሎ ዙር : {current_round[0]}ይ')
        except:
            pass
    def handle_round_like():
        if len(table_round_entry.get())==0:
            table_option_function()
        else:
            handle_like_table()
    def handle_like_table():
        
        if table_option.get()=="ዝርዝር ዓሚል": 
            fetch_customer_and_insert_into_table_like()
        elif table_option.get()=="ናይ ዕቁብ መዝገብ":
            fetch_enrollment_and_insert_into_table_like()
        elif table_option.get()=="ዝርዝር ዝኸፈሉ" :
            fetch_pay_and_insert_into_table_like()
        elif table_option.get()=="ዝርዝር ዘይከፈሉ":
            
            fetch_unpayed_and_insert_into_table_like()
        elif table_option.get()=="ዕጫ ዝበፅሖም":
            fetch_drawn_and_insert_into_table_like()
        elif table_option.get()=="ዕጫ ዘይበፅሖም":
            fetch_undrawn_customer_and_insert_into_table_like()
    customer_list_entries_frame=ttk.Frame(customer_list_frame,width=int(screen_width*0.2))
    customer_list_entries_frame.pack(fill=Y,side=LEFT)
    customer_list_table_frame=ttk.Frame(customer_list_frame)
    customer_list_table_frame.pack(fill=BOTH,side=LEFT,expand=True)
    # table_option=ttk.Combobox(customer_list_frame,width=22,values=table_list)
    table_option_label=ttk.Label(customer_list_entries_frame,text='እንታይ ይደልዩ?')
    table_option_label.grid(row=0,column=0,padx=10,pady=2,sticky='w')
    table_option=ttk.Combobox(customer_list_entries_frame,width=22,values=table_list)
    # table_option.pack(padx=5,pady=5,side=TOP,anchor='w')
    table_option.grid(row=1,column=0,padx=10,pady=2,sticky='w')
    table_option.bind('<KeyRelease>',table_option_event)
    table_option.bind('<FocusIn>',table_option_event)
    
    
    table_equb_type_label=ttk.Label(customer_list_entries_frame,text='ዓይነት ዕቑብ ይምረፁ ')
    # table_equb_type_label.grid(row=0,column=1,padx=25,pady=2,sticky='w')
    table_equb_type_entry=ttk.Combobox(customer_list_entries_frame,width=22,values=equb_type)
    # table_equb_type_entry.pack(padx=5,pady=5,side=TOP,anchor='w')
    # table_equb_type_entry.grid(row=1,column=1,padx=25,pady=2,sticky='w')
    table_equb_type_entry.bind('<KeyRelease>',table_option_event)
    table_equb_type_entry.bind('<FocusIn>',table_option_event)
    
    table_round_label=ttk.Label(customer_list_entries_frame,text='ናይ ዕጫ ዙር የእትዉ ')
    # table_round_label.grid(row=0,column=2,padx=25,pady=2,sticky='w')
        
    table_round_entry=ttk.Entry(customer_list_entries_frame,width=25)
    # table_round_entry.pack(padx=5,pady=5,side=TOP,anchor='w')
    # table_round_entry.grid(row=1,column=2,padx=25,pady=2,sticky='w')
    # table_round_entry.bind('<KeyRelease>',table_option_event )
    # table_round_entry.bind('<FocusIn>',table_option_event)
    table_round_entry.bind('<KeyRelease>',lambda e:  handle_round_like() )
    table_round_entry.bind('<FocusIn>',lambda e:  handle_round_like())
    table_reached_round_label=ttk.Label(customer_list_entries_frame,text='',font=('bold',16))
    table_reached_round_label.grid(row=9,column=0,padx=10,pady=2)
    # table_search_label=ttk.Label(customer_list_entries_frame,text='ሽም ብምእታው ይኣልሹ ')
    table_search_label=ttk.Label(customer_list_table_frame,text='ሽም ብምእታው ይኣልሹ ')
    
    # table_search_label.grid(row=7,column=0,padx=10,pady=2,sticky='w')
    table_search_label.pack(padx=50,pady=2,anchor='w')
    # table_search_entry=ttk.Entry(customer_list_entries_frame,width=25)
    table_search_entry=ttk.Entry(customer_list_table_frame,width=25)
    table_search_entry.pack(padx=50,pady=2,anchor='w')
    # table_search_entry.grid(row=8,column=0,padx=10,pady=2,sticky='w')
    # table_search_entry.bind('<KeyRelease>',table_option_event)
    table_search_entry.bind('<KeyRelease>',lambda e:  handle_like_table())
    table_search_entry.bind('<FocusIn>',lambda e:  handle_like_table())
    def check_table_query_entries():
        if  table_option.get()=="ዝርዝር ዘይከፈሉ"  or table_option.get()=="ዕጫ ዝበፅሖም":
            # current_round=(return_current_round(table_equb_type_entry.get()) )
            table_equb_type_label.grid(row=3,column=0,padx=10,pady=2,sticky='w')
            table_equb_type_entry.grid(row=4,column=0,padx=10,pady=2,sticky='w')
            table_round_label.grid(row=5,column=0,padx=10,pady=2,sticky='w')
            table_round_entry.grid(row=6,column=0,padx=10,pady=2,sticky='w')
            table_reached_round_label.grid(row=9,column=0,padx=10,pady=2)
            
            # table_round_entry.delete(0,END)
            # table_round_entry.insert(END, current_round[0])
        elif table_option.get()=="ዝርዝር ዝኸፈሉ" or table_option.get()=="ናይ ዕቁብ መዝገብ" or table_option.get()=="ዕጫ ዘይበፅሖም" :
            table_equb_type_label.grid(row=3,column=0,padx=10,pady=2,sticky='w')
            table_equb_type_entry.grid(row=4,column=0,padx=10,pady=2,sticky='w')
            table_reached_round_label.grid(row=9,column=0,padx=10,pady=2)
            table_round_entry.grid_forget()
            table_round_label.grid_forget()
        elif table_option.get()=="ዝርዝር ዓሚል":
            table_equb_type_entry.grid_forget()
            table_equb_type_label.grid_forget()
            table_round_entry.grid_forget()
            table_round_label.grid_forget()
            table_reached_round_label.grid_forget()
        else:
            pass
    check_table_query_entries()
    list_of_customers=ttk.Treeview(customer_list_table_frame)
    list_of_customers.pack(fill=BOTH,expand=True,padx=50,pady=10)
    
    # list_of_customers.grid(row=4,column=0,padx=5,pady=5,sticky='e',columnspan=8)
    
    refresh_table_list()
    fill_table_equb_type()
    # fill_table_round_entry()
    vsbs=ttk.Scrollbar(list_of_customers,orient=VERTICAL,command=list_of_customers.yview)
    vsbs.place(relx=0.978,rely=0.05,height=390)
    list_of_customers.configure(yscrollcommand=vsbs.set)
    hsbs=ttk.Scrollbar(list_of_customers,orient=HORIZONTAL,command=list_of_customers.xview)
    hsbs.place(relx=0,rely=0.97,width=screen_width-25)
    list_of_customers.configure(xscrollcommand=hsbs.set)
    # fetch_customer_and_insert_into_table()
#*******************************************************************************************
    main_window.protocol('WM_DELETE_WINDOW',close_main_window)
#********************************************registration page*****************************************
def display_about_window():
    global about_window
    about_window=Toplevel(home_page)
    # home_page.state('iconic')
    home_page.state('withdrawn')
    about_window.title(company_title)
    about_window.configure(background='blue')
    about_window.resizable('False','False')
    about_window.geometry(f"{520}x{325}+350+200")
    about_photo_frame=ttk.Frame(about_window)
    about_photo_frame.pack()
    about_photo_label=ttk.Label(about_photo_frame,image=about_image)
    about_photo_label.pack()
    about_window.state('normal')
    about_window.protocol('WM_DELETE_WINDOW',close_about_window)
    
#********************************************homepage*****************************************
def create_backup_file():
    source='db/db.db'
    destination=filedialog.askdirectory(title='መሐለውታ ፋይል ኣቀምጥ')
    if destination:
        shutil.copy(source,destination)
        messagebox.showinfo('ሓበሬታ','መሐለውታ ፋይል ብትክክል ተቐዲሑ')
# Create the home page with Tkinter
home_page = Tk()
home_page.title(company_title)
home_page.configure(background='white')
home_page.iconbitmap(window_icon)
# home_page.theme_use('vista')
# home_page.map('TButton',foreground=[('pressed','pink'),('disabled','orange'),('hover','red'),('background','yellow'),('selected','yellow'),('active','green')])
#***********************************************************************************
# styles********************************************************************************************************************************************************************************************************************************************************************************************
styles=ttk.Style()
styles.configure('TLabel',foreground='black',background='white')
styles.configure('Treeview',rowheight=48,fieldbackground='white')
styles.configure('TNotebook',background='white')
styles.configure('TFrame',background='white')
styles.configure('TLabel',background='white')
styles.configure('pink.TFrame',background='pink')
styles.configure('TEntry',background='blue')
# styles.configure('TButton',background='blue')
# styles.map('TButton',background=[('hover','black'),('background','black')])

styles.configure('save.TButton',background='lightgreen')
styles.configure('update.TButton',background='orange')
styles.configure('delete.TButton',background='pink')
styles.configure('about.TButton',background='blue')
styles.configure('pink.TLabel',background='pink')
equb_logo = PhotoImage(file='./image/logo.png')
# uploded_
background_photo=(PhotoImage(file='./image/background_photo.png'))
# image=Image.open('./image/background_photo.png')
# image = image.resize((int(750),int(520)))
# background_photo = ImageTk.PhotoImage(image)
# ethiopian_coin_photo=(PhotoImage(file='/home/robel/Documents/captured file/Equb/image/ethiopian_coin.png')).subsample(2,2)
small_equb_logo=equb_logo.subsample(3,3)
customer_photo=PhotoImage(file='./image/logo.png')
qr_image=PhotoImage(file='./image/qr_code.png')
small_qr_code=qr_image.subsample(10,10)
# Calculate screen width and height
screen_width = home_page.winfo_screenwidth()
screen_height = home_page.winfo_screenheight()

home_page.geometry(f"{screen_height}x{screen_width}+0+0")
home_page.minsize(screen_width,screen_height)

# Header Frame
header_frame =Frame(home_page,height=screen_height*0.1,width=screen_width, background='darkblue')
header_frame.grid(row=0,column=0)

logo_label = ttk.Label(header_frame, image=small_equb_logo,background='darkblue')
logo_label.place(x=0,y=0)
# logo_label.grid(row=0,column=0,sticky='w')
global title_label
title_label=Label(header_frame,text=company_name,foreground='yellow',background='darkblue' ,font=('bold',42))
title_label.place(x=0.4*screen_width,y=5)
# title_label.place(relx=0.5,y=0,anchor='se')
# title_label.grid(row=0,column=1,sticky='e')
# Main Frame
main_frame = ttk.Frame(home_page,height=screen_height*0.7,width=screen_width)
main_frame.grid(row=1,column=0)
#left frame for form
left_frame =ttk.Frame(main_frame,height=screen_height*0.7,width=int(screen_width*0.50))
left_frame.grid(row=0,column=0,pady=20,ipady=60,sticky='nsew')
# left_frame.configure(height=800,width=900)

#photo frame
right_frame =ttk.Frame(main_frame,height=screen_height*0.7,width=int(screen_width*0.50))
right_frame.grid(row=0,column=1,sticky='nsew')
#******************************************** main frame ********************
log_in_image=PhotoImage(file='./image/login.png')
small_login=log_in_image.subsample(4,4)
# login_label=ttk.Label(left_frame,text='LOG IN',font=('bold',14),foreground='blue')
login_label=ttk.Label(left_frame,image=small_login)
login_label.grid(row=1,column=1,padx=5,pady=5)
expire_image=PhotoImage(file='./image/expire.png')
expire_small=expire_image.subsample(1,1)
def close_expire_window():
    home_page.state('normal')
    expire_window.destroy()
def expiry_date_reached():
    # print('software expired')
    global expire_window
    expire_window=Toplevel(home_page)
    home_page.state('withdrawn')
    expire_window.geometry('520x620+350+30')
    expire_window.resizable('False','False')
    expire_window.iconbitmap(window_icon)
    frame=ttk.Frame(expire_window)
    frame.pack()
    expire_img=ttk.Label(frame,image=expire_small)
    expire_img.pack()
    expire_window.protocol('WM_DELETE_WINDOW',close_expire_window)
def clear_password_error():
    password_error.config(text='')
# logged_user_role=''
def check_expire_date():
    current_date=date.today()
    installed_date=date.today()
    db = sqlite3.connect(database_name)
    cursor = db.cursor()
    cursor.execute("create table if Not Exists expiry_date ('installed_date' varchar(20),'length' INT)")
    cursor.execute('select * from expiry_date')
    value=cursor.fetchall()
    
    if value:
        splited_value=((value[0][0]).split(' ')[0]).split('-')
       
        installed_date=date(int(splited_value[0]),int(splited_value[1]),int(splited_value[2]))
    else: 
        installed_date=date.today()
        cursor.execute("insert into expiry_date values(?,?)",(installed_date,7))
    subtructed_date=current_date-installed_date
    fetched=fetch_data("length ","expiry_date")
    
    if fetched:
        if fetched[0][0]=='no':
            return False
        else:
            duration=int(fetched[0][0])
            if  (subtructed_date.days>duration or subtructed_date.days<0):
                return True
            else:
                return False
    cursor.close()
    db.commit()
    db.close()
##def check_user_name_and_password():
##    db = sqlite3.connect(database_name)
##    cursor = db.cursor()
##    cursor.execute('select * from user where user_name=? and password=?',[user_name_entry.get(),password_entry.get()])
##    result=cursor.fetchone()
##    
##    
##    is_expired=check_expire_date()
##    
##    
##    if result:
##        if is_expired and str(result[4])!=str('super_admin'):
##            expiry_date_reached()
##        else:
##            global logged_user_role
##            global logged_user_id
##            logged_user_id=result[0]
##            logged_user_role=result[4]
##            
##            display_main_window()
##    else:
##        password_entry.delete(0,END)
##        password_error.config(text='መሕለፊ ቃል ኣስተካክሉ ',foreground='red')
##        password_error.after('2000',clear_password_error)
##    cursor.close()
##    db.commit()
##    db.close()
##    password_entry.delete(0,END)
def check_user_name_and_password():
    try:
        db = sqlite3.connect(database_name)
        cursor = db.cursor()
        
        # Get the username entered by the user
        user_name = user_name_entry.get()
        password = password_entry.get()
    
        # Fetch the user record from the database (including hashed password)
        cursor.execute('SELECT * FROM user WHERE user_name=?', [user_name])
        result = cursor.fetchone()
    
        # Check for password expiration
        is_expired = check_expire_date()
    
        if result:
            # The password is stored in a hashed form, so we check using bcrypt
            stored_hashed_password = result[3]  # Assuming the hashed password is in the third column (index 3)
            global logged_user_role
            global logged_user_id
            global logged_user_name
            global logged_user_full_name
            global logged_user_photo
            logged_user_id = result[0]
            logged_user_full_name=result[1]
            logged_user_name=result[2]
            logged_user_role = result[4]
            if result[5]:
                logged_user_photo=result[5]
            else:
                logged_user_photo=default_profile_photo
            # Check if the password entered by the user matches the stored hashed password
            if bcrypt.checkpw(password_entry.get().encode('utf-8'), stored_hashed_password):
                if is_expired and str(result[4]) != str('super_admin'):
                    expiry_date_reached()
                else:
                    
                    display_main_window()
            else:
                # Invalid password
                password_entry.delete(0, END)
                password_error.config(text='መሕለፊ ቃል ኣስተካክሉ ', foreground='red')
                password_error.after(2000, clear_password_error)
        else:
            # Username not found
            password_entry.delete(0, END)
            password_error.config(text='መሕለፊ ቃል ኣስተካክሉ ', foreground='red')
            password_error.after(2000, clear_password_error)
    
        cursor.close()
        db.commit()
        db.close()
        password_entry.delete(0, END)
    except:
        pass
#*************************************************************************

def clear_login_entry():
    password_entry.delete(0,END)
    user_name_entry.delete(0,END)
#***************************************************user name*******************
user_name_label=ttk.Label(left_frame,text='መጥቀሚ ሽም',font=(Tera,12,'bold'))
user_name_label.grid(row=2,column=1,padx=5,pady=5,sticky='w')
user_name_entry=ttk.Entry(left_frame,width=20,font=(Tera,12,'bold'))
user_name_entry.grid(row=3,column=1,padx=5,pady=5)
user_name_entry.delete(0,END)
user_name_entry.insert(END,'@equb')

logged_user=user_name_entry.get()
# user_name_error=ttk.Label(left_frame,text=error['user_name_error'],width='30',foreground='red')
# user_name_error.grid(row=4,column=1,padx=5,pady=5,sticky='w')

#********************************************* logo   ********************************
background_image=ttk.Label(right_frame,image=background_photo)
background_image.grid( row=0,column=0,padx=0,pady=5,sticky='e')
#***************************************************user name form ******************************
# def password_event(event):
#     if len(password_entry.get())>0 and len(password_entry.get())<8:
#         error['password_error']='weak password'
#         password_error.config(text=error['password_error'])
#     else:
#         error['password_error']=''
#         password_error.config(text=error['password_error'])
#*********************************** password form******************************************
password_label=ttk.Label(left_frame,text='መሕለፊ ቃል',font=(Tera,12,'bold'))
password_label.grid(row=5,column=1,padx=5,pady=5,sticky='w')
password_entry=ttk.Entry(left_frame,width=20,font=(Tera,12,'bold'))
password_entry.grid(row=6,column=1,padx=5,pady=5,sticky='w')
# password_entry.bind('<KeyRelease>',password_event)
password_entry.config(show='•')
#****************************************log in button ****************************************
login_button=ttk.Button(left_frame,width=29,text='ቀፅል',command=check_user_name_and_password)
                        # command=display_main_window)
login_button.grid(row=7,column=1,padx=5,pady=5)
#************************************************back up file button********************************
# backup_button=ttk.Button(left_frame,width=29,text='save backup file',command=create_backup_file)
# backup_button.grid(row=9,column=1,padx=5,pady=5)
#************************************** about developer **********************************
about_button=ttk.Button(left_frame,width=29,text='ብዛዕባ ሰራሒ ሶፍትዌር',command=display_about_window)
##                        display_about_window)
                        # ,command=lambda :expiry_date_reached())
                        # 
about_button.grid(row=8,column=1,padx=5,pady=5)
password_error=ttk.Label(left_frame,text='',width='30',foreground='red')
password_error.grid(row=9,column=1,padx=5,pady=5,sticky='w')

about_image=PhotoImage(file='image/about.png')
#*****************************************close window*******************************************
def close_home_page():
    if messagebox.askyesno('ምዕፃው','ክትዓፅውዎ ትደልዩ ዲኹም?'):
        home_page.destroy()

#***********************************************************************************
# close_home_page_button=ttk.Button(left_frame,width=29,text='close',command=close_home_page)
# close_home_page_button.grid(row=11,column=1,padx=5,pady=5)
# close_home_page_button.config(style='delete.TButton')

#***************************************************************************
#coin_photo=ttk.Label(left_frame,image=ethiopian_coin_photo,background='white')
#coin_photo.grid(row=9,column=2,padx=5,pady=5)
# ********************************** Footer Frame **********************************
footer_frame =ttk.Frame(home_page,height=screen_height*0.1,width=screen_width)
footer_frame.place(relx=0, rely=0.9, relwidth=1, relheight=0.1) 
##.place(relx=0,rely=0.5)
# footer_frame.grid(row=2,column=0,sticky='s')

clock_label=ttk.Label(footer_frame,text=clock,font=('bold',18))
##clock_label.grid(row=1,column=1,padx=5,pady=5)
clock_label.place(relx=0.5, rely=0.5, anchor='center')
# Start the main loop
home_page.protocol('WM_DELETE_WINDOW',close_home_page)
home_page.mainloop()
