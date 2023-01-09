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
            'class_admins': {
                'add_admin': "➕ Add admin"
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
            },
            'group_now': {
                'name': "Change name 🗣",
                'timetable': "Edit timetable 🗓",
                'delete': "Delete group ❌"
            },
            'group_delete': {
                'yes': "Yes",
                'no': "No"
            },
            'group_timetable': {
                'add': "➕ Add lesson",
                'jan': "Jan",
                'feb': "Feb",
                'mar': "Mar",
                'apr': "Apr",
                'may': "May",
                'jun': "Jun",
                'jul': "Jul",
                'aug': "Aug",
                'sep': "Sep",
                'oct': "Oct",
                'nov': "Nov",
                'dec': "Dec",
                'mon': "Mon",
                'tue': "Tue",
                'wed': "Wed",
                'thi': "Thi",
                'fri': "Fri",
                'sat': "Sat",
                'sun': "Sun",
            },
            'lesson': {
                'name': "💁‍♂️ Change name",
                'time': "⏳ Start time and duration",
                'homework': "📚 Homework",
                'place': "📍 Place",
                'weekly': "📅 Weekly? {weekly}",
                'all': "👁‍🗨 Add for all groups? {all}",
                'create': "Create lesson ➕",
                'save': "Save changes ✅",
                'delete': "❌ Delete lesson",
                'original': "⤴ Back to original lesson",
                'restore': "♻ Restore changes"
            },
            'lesson_time': {
                'start': "⏰ Start time",
                'hrs': "{hrs} hrs",
                'mins': "{mins} mins",
                'duration': "⏳ Duration",
                'length': "{length} mins",
                'save': "✅ Save changes"
            }
        },
        'start':
            """
Hi {name}! 👋

📅 I'm @srnmSchoolBot for scheduling your school *lessons* and reminding you about your *school tasks*

📝 I should be added into your *class chat* to be able to send you messages about your *lessons*

📌 For more info try /help
            """,
        'help':
            """
🌎 First of all, go to /settings and choose your language if exists!

🤔 To use @srnmSchoolBot you should go with /class command

📃 If you had already created at least one class, just choose it from the list (or create a new one)
➕ Otherwise, you will be given an opportunity to create one. Enter the name of your new class

💭 After that you should add @srnmSchoolBot into your class chat
✅ Then write /verify to connect your class and the bot (note that you should be an administrator in this chat)

⏩ Now you're done! You can go with /class command again and choose your class
⚙ Go to settings at first! Here choose if you want to be notified about the lessons, choose the timezone of your class to be notified in the correct time and then you have to set notification time
👨‍💻 You can also add another administrator, for example, if you want someone to help you in editing the schedule (note that new administrators can delete other admins)
👉 To choose language for your class, just press the button

❌ You can delete whole class with all groups and lessons, you can change class name

📍 To use scheduling feature, create at least one group. You can also delete it with all the lessons or change its name

🗓 Now you can edit timetable!
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
        'no_classes':
            """
❗ You have no classes to verify! Go to @srnmSchoolBot to create a new class
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
            """,
        'group_now':
            """
This is *{clas} {group}*. Choose, what you want to do 👇
            """,
        'group_change_name':
            """
Which name do you prefer instead of *{clas} {group}*? 🤔 
            """,
        'group_delete':
            """
Are you sure you want to delete your *{group}* of *{clas}*? Your timetable for this group will be deleted too! ❌
            """,
        'class_admins':
            """
Here are all admins of *{name}*! You can delete these admins, except for yourself

Also, you can add other admins for your class
            """,
        'class_add_admin':
            """
To add an admin to *{name}*, send me the Telegram ID of the user

Ask this user to use @userinfobot to give you their Telegram ID
            """,
        'group_timetable':
            """
🗓 This is the timetable for *{clas} {group}*!

🤔 Here you can copy an existing timetable from the another group if they exist and add new lessons or edit the existing ones on the particular date
            """,
        'lesson_create_name':
            """
What should be the name of your new lesson? 📕
            """,
        'lesson_name':
            """
What should be a new name of your lesson called *{lesson}*? 📕
            """,
        'lesson_create':
            """
Here you can edit your new lesson for *{clas} {group}*! 👈

♻ You can change the name of it, choose start time and its duration, input the homework, change the place, set if this lesson should be every week, choose if this lesson should be added to all groups

And that is what info about your lesson you have already filled 👇
            """,
        'lesson':
            """
Here you can edit your lesson for *{clas} {group}*! 👈

♻ You can change the name of it, choose start time and its duration, input the homework, change the place, set if this lesson should be every week and delete it

And that is what info about your lesson you have already filled 👇
            """,
        'weekly_lesson':
            """
Here you can edit your lesson for *{clas} {group}*! 👈

🤔 This lesson is automatically created, because you set Weekly parameter in the original lesson! Here you can only change name, homework and place of the lesson
👉 You can also go to the original lesson to apply changes to all future weekly scheduled lessons or you can restore changes for this particular lesson to match with the original one

And that is what info about your lesson you have already filled 👇
            """,
        'lesson_time':
            """
Here you can change when the lesson starts and its duration ⏰
            """,
        'lesson_homework':
            """
Send me your homework here 📗
            """,
        'lesson_place':
            """
Choose a place for your lesson! It can be the number of your classroom or even the whole address 📍
            """
    }
}