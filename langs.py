langs = {
    'en': {
        'keyboards': {
            'cancel': "🔙 Cancel",
            'back': "🔙 Back",
            'settings': {
                'lang': "🗺 Language: {lang}"
            },
            'class_choose': {
                'add_class': "📚 Create class"
            },
            'class_now': {
                'groups': "Groups 👫",
                'name': "Change name 🔁",
                'settings': "Settings ⚙",
                'delete': "Delete ❌"
            },
            'class_settings': {
                'admins': "Admins 👨‍💻",
                'lang': "🗺 Language: {lang}",
                'notify': "🔔 Notifications: {notify}",
                'time': "⏰ Notification time",
                'tz': "⏳ Timezone: {tz}"
            },
            'class_delete': {
                'yes': "Yes",
                'no': "No"
            },
            'class_settings_tz': {
                '-12': "UTC−12, USA, Baker Island",
                '-11': "UTC−11, USA, Samoa",
                '-10': "UTC−10, USA, Hawaii",
                '-9': "UTC−9, France, Gambier Islands",
                '-8': "UTC−8, USA, Washington",
                '-7': "UTC−7, USA, New Mexico",
                '-6': "UTC−6, USA, Minnesota",
                '-5': "UTC−5, USA, New York",
                '-4': "UTC−4, Dominican Republic",
                '-3': "UTC−3, Argentina",
                '-2': "UTC−2, Brazil, Fernando de Noronha",
                '-1': "UTC−1, Portugal, Azores islands",
                '+0': "UTC+0, Ireland",
                '+1': "UTC+1, Germany",
                '+2': "UTC+2, Russia, Kaliningrad",
                '+3': "UTC+3, Russia, Moscow",
                '+4': "UTC+4, Russia, Samara",
                '+5': "UTC+5, Russia, Yekaterinburg",
                '+6': "UTC+6, Russia, Omsk",
                '+7': "UTC+7, Russia, Krasnoyarsk",
                '+8': "UTC+8, Russia, Irkutsk",
                '+9': "UTC+9, Russia, Amur",
                '+10': "UTC+10, Russia, Vladivostok",
                '+11': "UTC+11, Russia, Magadan",
                '+12': "UTC+12, Fiji",
                '+13': "UTC+13, Samoa",
                '+14': "UTC+14, Kitibati, Line Islands",
            },
            'class_settings_time': {
                'day': "🌞 Day before",
                'lesson': "🛎 Before lesson",
                'hrs': "{hrs} hrs",
                'mins': "{mins} mins",
                'gap': "{gap} mins",
                'save': "✅ Save changes"
            },
            'group_choose': {
                'add': "Add group ➕"
            }
        },
        'start':
            """
Hi {name}! 👋

📅 I'm @srnmSchoolBot for scheduling your school *lessons* and reminding you about your *school tasks* 📝

📌 For more info try /help
            """,
        'help':
            """
🤔 To use @srnmSchoolBot add it into your class chat
After that use this commands in order and _follow instructions_:

📍 /class — firstly, you should create your class. Type in name of it. If it is already created, you can change its name or delete it with all data!

📍 /settings — after you have created your class, you should go to settings to choose the language and your timezone and change the notification system
            """,
        'max_lim':
            """
❗ Your message should be less than {symbols} symbols
            """,
        'settings':
            """
⚙ These are @srnmSchoolBot settings! You can change your language here:
            """,
        'class_create_name':
            """
What name should be given for your new class?
            """,
        'class_verify':
            """
🤔 Now you should verify *{name}*!

👉 Add @srnmSchoolBot to your class chat and then go with /verify in this chat

📌 _Notice that you should be an administrator in this chat_
            """,
        'class_exists':
            """
Class for this chat already exists! ❌
            """,
        'not_admin':
            """
❗ You must be an admin of this chat to create a class
            """,
        'class_added':
            """
Class has been successfully added! ✅

Use /class
            """,
        'class_choose':
            """
🏫 Here are your classes. Choose one to work with:
            """,
        'class_now':
            """
This is your class *{name}* 👈

⚙ You can change its name, delete it, change some settings and choose a group to edit timetable
            """,
        'class_change_name':
            """
What new name of your class {name} should we take? 🤔
            """,
        'class_settings':
            """
Here are the settings for your class *{name}*:

🔻 You can change admins of the class
🔻 Change language settings
🔻 Turn on/off notifications about lessons
🔻 Edit the time of notifications
🔻 Change the timezone
            """,
        'class_delete':
            """
❓ Sure want to delete your class {name}? *ALL DATA ABOUT YOUR LESSONS AND GROUPS WILL BE DELETED!!!* ❓
            """,
        'class_deleted':
            """
Class {name} has been successfully *deleted*! Try /class to create a new one or choose the existing one
            """,
        'class_settings_tz':
            """
🌏 Choose your timezone to be notified in the correct time
            """,
        'class_settings_time':
            """
⌚ Put the time your class *{name}* would be notified the day before lessons

🕰 Then put a time gap when you would be notified about the next lesson 
            """,
        'group_create_name':
            """
What should be the name of your *{name}* group?
            """,
        'group_choose':
            """
Here are *{name}* groups! Choose one to edit timetable 👈 
            """
    }
}