from tkinter import *
from tkinter import ttk
from dd_email import DailyDigestEmail
from dd_scheduler import DailyDigestScheduler
import json
import re


class DailyDigestGUI:

    def __init__(self, root):
        # build the GUI #
        self.__root = root
        self.__root.title('Daily Digest')
        title_label = ttk.Label(self.__root, text=' \U0001F4DC Daily Digest \U0001F4DC',
                                font='Algerian 32 bold', justify=CENTER)
        title_label.pack(padx=5, pady=5)

        self.__style = ttk.Style()
        self.__style.configure('TButton', font=('Arial', 12, 'bold'))
        self.__style.configure('Header.TLabel', font=('Arial', 18, 'bold'))

        # GUI listbox for recipients
        recipients_frame = ttk.Frame(self.__root)
        recipients_frame.pack(padx=5, pady=5)
        self.__add_recipient_email_var = StringVar()
        self.__add_recipient_city_var = StringVar()
        self.__add_recipient_country_var = StringVar()
        self.__recipient_list_data_var = Variable()
        self.__build_gui_recipients(recipients_frame,
                                    self.__add_recipient_email_var,
                                    self.__add_recipient_city_var,
                                    self.__add_recipient_country_var,
                                    self.__recipient_list_data_var
                                    )

        # GUI elements to schedule delivery time
        schedule_frame = ttk.Frame(self.__root)
        schedule_frame.pack(padx=5, pady=5)
        self.__hour_var = StringVar()
        self.__minute_var = StringVar()
        self.__second_var = StringVar()
        self.__build_gui_schedule(schedule_frame,
                                  self.__hour_var,
                                  self.__minute_var,
                                  self.__second_var)

        # GUI checkboxes of content to include in email
        contents_frame = ttk.Frame(self.__root)
        contents_frame.pack(padx=5, pady=5)
        self.__quote_var = IntVar()
        self.__weather_var = IntVar()
        self.__twitter_var = IntVar()
        self.__wikipedia_var = IntVar()
        self.__build_gui_contents(contents_frame,
                                  self.__quote_var,
                                  self.__weather_var,
                                  self.__twitter_var,
                                  self.__wikipedia_var)

        # GUI fields for sender email/password credentials
        sender_frame = ttk.Frame(self.__root)
        sender_frame.pack(padx=5, pady=5)
        self.__sender_email_var = StringVar()
        self.__sender_password_var = StringVar()
        self.__sender_gmail_var = StringVar()
        self.__sender_pwgmail_var = StringVar()
        self.__build_gui_sender(sender_frame,
                                self.__sender_email_var,
                                self.__sender_password_var,
                                self.__sender_gmail_var,
                                self.__sender_pwgmail_var)

        # GUI field for controls
        controls_frame = ttk.Frame(self.__root)
        controls_frame.pack(padx=5, pady=5)
        self.__build_gui_controls(controls_frame)

        # set initial values for variables
        self.__email = DailyDigestEmail()
        self.__scheduler = DailyDigestScheduler()
        try:
            self.__load_config()
            self.__update_settings()
        except:
            print('Your data is empty. Please fill in.')
            with open('dd_config.json', 'w') as file:
                json.dump('', file, indent=4)

        # initialize scheduler
        self.__scheduler.start()
        self.__root.protocol("WM_DELETE_WINDOW", self.__shutdown)  # shuts down the scheduler

    """
    Build GUI elements to add/remove recipients 
    """

    def __build_gui_recipients(self, master, add_recipient_email_var, add_recipient_city_var,
                               add_recipient_country_var, recipient_list_data_var):
        # create GUI widgets
        header = ttk.Label(master, text='Recipients:', style='Header.TLabel')
        email_label = ttk.Label(master, text='Email:')
        city_label = ttk.Label(master, text='City:')
        country_label = ttk.Label(master, text='Country:')
        spacer_frame = ttk.Frame(master)  # used as GUI spacer

        recipients_entry_email = ttk.Entry(master, width=30, textvariable=add_recipient_email_var)
        recipients_entry_city = ttk.Entry(master, width=15, textvariable=add_recipient_city_var)
        recipients_entry_country = ttk.Entry(master, width=15, textvariable=add_recipient_country_var)
        recipients_scrollbar = ttk.Scrollbar(master, orient=VERTICAL)
        recipients_scrollbar.grid(row=4, column=2, sticky=E)

        recipients_listbox_data = Listbox(master, listvariable=recipient_list_data_var,
                                          selectmode='multiple', height=5)  # width=50
        recipients_listbox_data.configure(yscrollcommand=recipients_scrollbar.set)
        recipients_scrollbar.config(command=recipients_listbox_data.yview)

        add_button = ttk.Button(master, text='Add Recipient', command=self.__add_recipient_data)
        remove_button = ttk.Button(master, text='Remove Selected',
                                   command=lambda: self.__remove_selected_recipients(
                                       recipients_listbox_data.curselection()))

        # place GUI widgets using grid geometry manager
        header.grid(row=0, column=1, sticky=NE)
        email_label.grid(row=1, column=0, padx=5, pady=5, sticky=NW)
        recipients_entry_email.grid(row=2, column=0, padx=5, pady=5, sticky=NW)
        city_label.grid(row=1, column=1, padx=5, pady=5, sticky=N)
        recipients_entry_city.grid(row=2, column=1, padx=5, pady=5, sticky=N)
        country_label.grid(row=1, column=2, padx=5, pady=5, sticky=NE)
        recipients_entry_country.grid(row=2, column=2, padx=5, pady=5, sticky=NE)

        add_button.grid(row=3, column=2, padx=5, pady=5, sticky=NE)

        recipients_listbox_data.grid(row=4, column=0, columnspan=3, padx=5, pady=5, sticky=EW)

        remove_button.grid(row=5, column=2, padx=5, pady=5, sticky=NE)

        spacer_frame.grid(row=4, column=1, pady=5)

    """
    Build GUI elements to schedule send time
    """

    @staticmethod
    def __build_gui_schedule(master, hour_var, minute_var, second_var):
        # create GUI widgets
        header = ttk.Label(master, text='Scheduled Time (24hr):', style='Header.TLabel')
        hour_label = ttk.Label(master, text='hours')
        minute_label = ttk.Label(master, text='minutes')
        second_label = ttk.Label(master, text='seconds')

        hour_label.grid(row=1, column=0, sticky=W, padx=2, pady=5)
        minute_label.grid(row=1, column=2, sticky=W, padx=2, pady=5)
        second_label.grid(row=1, column=4, sticky=E, padx=2, pady=5)

        hour_spinbox = ttk.Spinbox(master, from_=0, to=23, textvariable=hour_var,
                                   wrap=True, width=3, justify=CENTER, font='Arial 12')
        minute_spinbox = ttk.Spinbox(master, from_=0, to=59, textvariable=minute_var,
                                     wrap=True, width=3, justify=CENTER, font='Arial 12')
        second_spinbox = ttk.Spinbox(master, from_=0, to=59, textvariable=second_var,
                                     wrap=True, width=3, justify=CENTER, font='Arial 12')
        # place GUI widgets using grid geometry manager
        header.grid(row=0, column=0, columnspan=6)
        hour_spinbox.grid(row=1, column=1, sticky=E, padx=2, pady=5)
        minute_spinbox.grid(row=1, column=3, sticky=W, padx=2, pady=5)
        second_spinbox.grid(row=1, column=5, sticky=W, padx=2, pady=5)

    """
    Build GUI elements to select content to include
    """

    @staticmethod
    def __build_gui_contents(master, quote_var, weather_var, twitter_var, wikipedia_var):
        # create GUI widgets
        header = ttk.Label(master, text='Digest Contents:', style='Header.TLabel')
        quote_checkbox = Checkbutton(master, text='Motivational Quote',
                                     onvalue=True, offvalue=False,
                                     variable=quote_var)
        weather_checkbox = Checkbutton(master, text='Weather Forecast',
                                       onvalue=True, offvalue=False,
                                       variable=weather_var)
        twitter_checkbox = Checkbutton(master, text='Twitter Trends',
                                       onvalue=True, offvalue=False,
                                       variable=twitter_var)
        wikipedia_checkbox = Checkbutton(master, text='Wikipedia Article',
                                         onvalue=True, offvalue=False,
                                         variable=wikipedia_var)

        # place GUI widgets using grid geometry manager
        header.grid(row=0, column=0, columnspan=2)
        quote_checkbox.grid(row=1, column=0, sticky=W)
        weather_checkbox.grid(row=2, column=0, sticky=W)
        twitter_checkbox.grid(row=1, column=1, sticky=W)
        wikipedia_checkbox.grid(row=2, column=1, sticky=W)

    """
    Build GUI elements to configure sender credentials
    """

    @staticmethod
    def __build_gui_sender(master, sender_email_var, sender_password_var, sender_gmail_var, sender_pwgmail_var):
        # create GUI widgets
        header = ttk.Label(master, text='Sender Credentials:', style='Header.TLabel')
        email_label = ttk.Label(master, text="Email Outlook:")
        email_entry = ttk.Entry(master, width=40,
                                textvariable=sender_email_var)
        password_label = ttk.Label(master, text='Password:')
        password_entry = ttk.Entry(master, width=40, show='*',
                                   textvariable=sender_password_var)

        # place GUI widgets using grid geometry manager
        header.grid(row=0, column=0, columnspan=2)
        email_label.grid(row=1, column=0, pady=2, sticky=E)
        email_entry.grid(row=1, column=1, pady=2, sticky=W)
        password_label.grid(row=2, column=0, pady=2, sticky=E)
        password_entry.grid(row=2, column=1, pady=2, sticky=W)

        email_label_ = ttk.Label(master, text="Email Gmail:")
        email_entry_ = ttk.Entry(master, width=40,
                                 textvariable=sender_gmail_var)
        password_label_ = ttk.Label(master, text='Password:')
        password_entry_ = ttk.Entry(master, width=40, show='*',
                                    textvariable=sender_pwgmail_var)

        # place GUI widgets using grid geometry manager
        email_label_.grid(row=3, column=0, pady=2, sticky=E)
        email_entry_.grid(row=3, column=1, pady=2, sticky=W)
        password_label_.grid(row=4, column=0, pady=2, sticky=E)
        password_entry_.grid(row=4, column=1, pady=2, sticky=W)

    """
    Build GUI elements to update settings & manually send digest email
    """

    def __build_gui_controls(self, master):
        # create GUI widgets
        update_button = ttk.Button(master, text='Update Settings', command=self.__update_settings)
        send_button = ttk.Button(master, text='Manual Send', command=self.__manual_send)

        # place GUI widgets using grid geometry manager
        update_button.grid(row=0, column=0, padx=5, pady=5)
        send_button.grid(row=0, column=1, padx=5, pady=5)

    """
    Callback function to add recipient
    """

    def __add_recipient_data(self):
        new_recipient_email = self.__add_recipient_email_var.get()
        new_recipient_city = self.__add_recipient_city_var.get()
        new_recipient_country = self.__add_recipient_country_var.get()
        pattern_email = r'^(\w+\.)*\w+@(\w+\.)?\w+\.com$'
        matches_email = re.search(pattern_email, new_recipient_email)
        pattern_city_country = r'(\b\ *){1,3}'
        matches_city = re.search(pattern_city_country, new_recipient_city)
        matches_country = re.search(pattern_city_country, new_recipient_country)
        if matches_email and matches_city and matches_country:
            new_recipient_data = ', '.join((new_recipient_email, new_recipient_city, new_recipient_country))
            recipient_list_data = self.__recipient_list_data_var.get()
            if recipient_list_data != '':
                self.__recipient_list_data_var.set(recipient_list_data + (new_recipient_data,))
            else:
                self.__recipient_list_data_var.set([new_recipient_data])
            self.__add_recipient_email_var.set('')  # clear entry field
            self.__add_recipient_city_var.set('')
            self.__add_recipient_country_var.set('')

    """
    Callback function to remove selected recipient(s)
    """

    def __remove_selected_recipients(self, selection):
        recipient_list = list(self.__recipient_list_data_var.get())
        for index in reversed(selection):
            recipient_list.pop(index)
        self.__recipient_list_data_var.set(recipient_list)

    """
    Callback function to update settings
    """

    def __update_settings(self):
        print('Updating settings...')
        content = {}
        try:
            content = self.__email.create_content(recipient_data=self.__email.recipients_list[0])
        except AttributeError as e:
            print(e)
        content['quote']['include'] = self.__quote_var.get()
        content['weather']['include'] = self.__weather_var.get()
        content['twitter']['include'] = self.__twitter_var.get()
        content['wikipedia']['include'] = self.__wikipedia_var.get()

        self.__email.sender_credentials = {'outlook': self.__sender_email_var.get(),
                                           'password': self.__sender_password_var.get(),
                                           'gmail': self.__sender_gmail_var.get(),
                                           'passwrd': self.__sender_pwgmail_var.get(),
                                           'gmail_server': 'smtp.gmail.com',
                                           'outlook_server': 'smtp.office365.com'}
        users = self.__recipient_list_data_var.get()
        user_lst = []
        for record in users:
            email, city, country = record.split(', ')
            user_lst.append(dict(email=email, city=city, country=country))
        self.__email.recipients_list = user_lst
        try:
            self.__scheduler.schedule_daily(int(self.__hour_var.get()),
                                            int(self.__minute_var.get()),
                                            int(self.__second_var.get()),
                                            self.__email.handle_email_type)
        except AttributeError as e:
            print(e)
        print('Finished!')

    """
    Callback function to manually send digest email
    """

    def __manual_send(self):
        # note: settings are not updated before manual send
        print('Manually sending email digest...')
        self.__email.handle_email_type()

    """
    Shutdown the scheduler before closing the GUI window
    """

    def __shutdown(self):
        print('Shutting down the scheduler...')
        self.__scheduler.stop()
        self.__scheduler.join()
        try:
            self.__save_config()
        except Exception as e:
            print(e)
        self.__root.destroy()  # close the GUI

    def __save_config(self, file_path='dd_config.json'):
        config = {'add_recipient_email': self.__add_recipient_email_var.get(),
                  'add_recipient_city': self.__add_recipient_city_var.get(),
                  'add_recipient_country': self.__add_recipient_country_var.get(),
                  'recipient_list': self.__recipient_list_data_var.get(),
                  'hour': self.__hour_var.get(),
                  'minute': self.__minute_var.get(),
                  'second': self.__second_var.get(),
                  'quote': self.__quote_var.get(),
                  'weather': self.__weather_var.get(),
                  'twitter': self.__twitter_var.get(),
                  'wikipedia': self.__wikipedia_var.get(),
                  'sender_outlook': self.__sender_email_var.get(),
                  'sender_password_outlook': self.__sender_password_var.get(),
                  'sender_gmail': self.__sender_gmail_var.get(),
                  'sender_password_gmail': self.__sender_pwgmail_var.get(), }
        with open(file_path, 'w') as file:
            json.dump(config, file, indent=4)

    def __load_config(self, file_path='dd_config.json'):
        with open(file_path, 'r') as file:
            config = json.load(file)
            self.__add_recipient_email_var.set(config['add_recipient_email'])
            self.__add_recipient_city_var.set(config['add_recipient_city'])
            self.__add_recipient_country_var.set(config['add_recipient_country'])
            self.__recipient_list_data_var.set(config['recipient_list'])
            self.__hour_var.set(config['hour'])
            self.__minute_var.set(config['minute'])
            self.__second_var.set(config['second'])
            self.__quote_var.set(config['quote'])
            self.__weather_var.set(config['weather'])
            self.__twitter_var.set(config['twitter'])
            self.__wikipedia_var.set(config['wikipedia'])
            self.__sender_email_var.set(config['sender_outlook'])
            self.__sender_password_var.set(config['sender_password_outlook'])
            self.__sender_gmail_var.set(config['sender_gmail'])
            self.__sender_pwgmail_var.set(config['sender_password_gmail'])


if __name__ == '__main__':
    root_ = Tk()
    app = DailyDigestGUI(root_)
    root_.mainloop()
