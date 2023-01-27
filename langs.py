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

📝 I should be added into your Telegram *class chat* to be able to send you messages about your *lessons*

📌 For more info try /help
            """,
        'help':
            """
🌎 First of all, go to /settings and choose your language if exists!

🤔 To use @srnmSchoolBot you should go with /class command

📃 If you had already created at least one class, just choose it from the list (or create a new one)
➕ Otherwise, you will be given an opportunity to create one. Enter the name of your new class

💭 After that you should add @srnmSchoolBot into your Telegram class chat
✅ Then write /verify to connect your class and the bot (note that you should be an *administrator* in this chat)

⏩ Now you're done! You can go with /class command again and choose your class
⚙ Go to settings at first! Here choose if you want to be notified about the lessons, choose the timezone of your class to be notified in the correct time and then you have to set notification time
👨‍💻 You can also add another administrator, for example, if you want someone to help you in editing the schedule (note that new administrators can delete other admins)
👉 To choose language for your class, just press the button

❌ You can delete whole class with all groups and lessons, you can change class name

📍 To use scheduling feature, create at least one group. You can also delete it with all the lessons or change its name

🗓 Now you can edit timetable!
👉 Go to the day you want your new lesson to be and press the button to add a lesson
📚 Input info about your lesson: name (ex. Math), start time (ex. 9hrs 30mins), duration (ex. 45mins), homework (not necessary, ex. Task 5 p. 11), place (not necessary, ex. Room 214 or Caroline College Center)
🔜 All this info will be displayed, when you would be notified about the lesson. You can also put weekly parameter on if your lesson is held every week. With that type of lessons you can't change their time for future lessons
🌐 You can also add the lesson for all groups. The duplicates of the lesson will be created for each group in your class

↪ When you are done with scheduling your lessons, you can go to your Telegram class chat and go with /class command again, choose the desired group and choose the lesson you want to know info about
✅ You will be also notified about the lessons in your chat if you put notification parameter on in settings
            """,
        'support':
            """
📍 If you see something doesn't work or you need help, you can contact @srnm9
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
        'no_class':
            """
❗ You don't have a class for this chat! Go to @srnmSchoolBot to create a new class if you are an admin of this chat
            """,
        'no_groups':
            """
❗ You have no groups for *{name}*! If you are an admin for this class, go to @srnmSchoolBot to create at least one group. If not, ask your admin to do that
            """,
        'lesson_notification':
            """
*{clas} #group\_{group}*
🕰 Your lesson starts in {start} mins
            """,
        'daily_notification':
            """
*{clas} #group\_{group}*
Tomorrow you will have following lessons:
            """,
        'no_lessons':
            """
*{clas} #group\_{group}* you have no lessons tomorrow!
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
        'group_create_name':
            """
What should be the name of your *{name}* group?
            """,
        'group_choose':
            """
Here are *{name}* groups! Choose one to edit timetable 👈 
            """,
        'group_choose_timetable':
            """
Here are *{name}* groups! Choose one to view timetable 👈 
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
        'group_timetable':
            """
🗓 This is the timetable for *{clas} {group}*!

🤔 Here you can add new lessons or edit the existing ones on the particular date
            """,
        'timetable':
            """
🗓 This is the timetable for *{clas} {group}*!

🤔 Here you can view info about your lessons
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
        'group_lesson':
            """
Here is info about your lesson in *{clas} {group}* 👇
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
            """,
    },

    'ru': {
        'keyboards': {
            'cancel': "🔙 Отмена",
            'back': "🔙 Назад",
            'settings': {
                'lang': "🗺 Язык: {lang}"
            },
            'class_choose': {
                'add_class': "📚 Создать класс"
            },
            'class_now': {
                'groups': "Группы 👫",
                'name': "Изменить имя 🔁",
                'settings': "Настройки ⚙",
                'delete': "Удалить ❌"
            },
            'class_settings': {
                'admins': "Администраторы 👨‍💻",
                'lang': "🗺 Язык: {lang}",
                'notify': "🔔 Уведомления: {notify}",
                'time': "⏰ Время уведомлений",
                'tz': "⏳ Часовой пояс: {tz}"
            },
            'class_delete': {
                'yes': "Да",
                'no': "Нет"
            },
            'class_admins': {
                'add_admin': "➕ Добавить администратора"
            },
            'class_settings_tz': {
                '-12': "UTC−12, США, остров Бейкер",
                '-11': "UTC-11, США, Самоа",
                '-10': "UTC−10, США, Гавайи",
                '-9': "UTC−9, Франция, острова Гамбье",
                '-8': "UTC-8, США, Вашингтон",
                '-7': "UTC−7, США, Нью-Мексико",
                '-6': "UTC−6, США, Миннесота",
                '-5': "UTC-5, США, Нью-Йорк",
                '-4': "UTC−4, Доминиканская Республика",
                '-3': "UTC-3, Аргентина",
                '-2': "UTC−2, Бразилия, Фернандо де Норонья",
                '-1': "UTC-1, Португалия, Азорские острова",
                '+0': "UTC+0, Ирландия",
                '+1': "UTC+1, Германия",
                '+2': "UTC+2, Россия, Калининград",
                '+3': "UTC+3, Россия, Москва",
                '+4': "UTC+4, Россия, Самара",
                '+5': "UTC+5, Россия, Екатеринбург",
                '+6': "UTC+6, Россия, Омск",
                '+7': "UTC+7, Россия, Красноярск",
                '+8': "UTC+8, Россия, Иркутск",
                '+9': "UTC+9, Россия, Амур",
                '+10': "UTC+10, Россия, Владивосток",
                '+11': "UTC+11, Россия, Магадан",
                '+12': "UTC+12, Фиджи",
                '+13': "UTC+13, Самоа",
                '+14': "UTC+14, Китибати, острова Лайн",
            },
            'class_settings_time': {
                'day': "🌞 За день до уроков",
                'lesson': "🛎 До урока",
                'hrs': "{hrs} ч.",
                'mins': "{mins} мин.",
                'gap': "{gap} мин.",
                'save': "✅ Сохранить изменения"
            },
            'group_choose': {
                'add': "Создать группу ➕"
            },
            'group_now': {
                'name': "Изменить имя 🗣",
                'timetable': "Редактировать расписание 🗓",
                'delete': "Удалить группу ❌"
            },
            'group_delete': {
                'yes': "Да",
                'no': "Нет"
            },
            'group_timetable': {
                'add': "➕ Добавить урок",
                'jan': "Янв",
                'feb': "Фев",
                'mar': "Мар",
                'apr': "Апр",
                'may': "Май",
                'jun': "Июн",
                'jul': "Июл",
                'aug': "Авг",
                'sep': "Сен",
                'oct': "Окт",
                'nov': "Ноя",
                'dec': "Дек",
                'mon': "Пн",
                'tue': "Вт",
                'wed': "Ср",
                'thi': "Чт",
                'fri': "Пт",
                'sat': "Сб",
                'sun': "Вс",
            },
            'lesson': {
                'name': "💁‍♂️ Изменить имя",
                'time': "⏳ Начало и длительность",
                'homework': "📚 Домашнее задание",
                'place': "📍 Место",
                'weekly': "📅 Еженедельно? {weekly}",
                'all': "👁‍🗨 Добавить для всех групп? {all}",
                'create': "Создать урок ➕",
                'save': "Сохранить изменения ✅",
                'delete': "❌ Удалить урок",
                'original': "⤴ Вернуться к исходному уроку",
                'restore': "♻ Отменить изменения"
            },
            'lesson_time': {
                'start': "⏰ Начало",
                'hrs': "{hrs} ч.",
                'mins': "{mins} мин.",
                'duration': "⏳ Длительность",
                'length': "{length} мин.",
                'save': "✅ Сохранить изменения"
            }
        },
        'start':
            """
Привет {name}! 👋

📅 Я @srnmSchoolBot для создания *школьного расписания* и уведомления учеников о предстоящих *уроках*

📝 Меня нужно добавить в ваш *классный чат* Telegram, чтобы я мог напоминать Вам о *Ваших уроках*

📌 Для подробной информации введите /help
            """,
        'help':
            """
🌎 Прежде всего, введите /settings и выберите свой язык, если таковой имеется!

🤔 Чтобы использовать @srnmSchoolBot напишите команду /class

📃 Если Вы уже создали по крайней мере один класс, выберите его из списка (или создайте новый)
➕ В другом случае, создайте его. Введите имя Вашего нового класса

💭 После этого добавьте @srnmSchoolBot в Ваш классный чат в Telegram
✅ Введите /verify чтобы связать Ваш чат с классом в боте (заметьте, что Вы должны быть *администратором* этого чата)

⏩ Теперь мы готовы! Вновь введите /class и выберите свой класс
⚙ Вначале зайдите в настройки! Здесь выберите, хотите ли Вы получать уведомления об уроках, выберите часовой пояс класса, чтобы получать уведомления вовремя, а затем выберите время получения уведомлений
👨‍💻 Также Вы можете добавить другого администратора, например, если хотите, чтобы кто-то Вам помогал в заполнении расписания (заметьте, что добавленные администраторы смогут удалять назначенных админов)
👉 Для выбора языка Вашего класса просто нажмите на соответствующую кнопку

❌ Вы можете целиком удалить Ваш класс со всеми группами и уроками, а также сменить имя класса

📍 Чтобы использовать расписание для класса, необходимо создать хотя бы одну группу. Вы также можете удалить ее со всеми уроками или же изменить её имя

🗓 Наконец, Вы можете приступить к изменению расписания!
👉 Перейдите в день, в котором должен находиться урок и нажмите на кнопку, чтобы создать урок
📚 Введите информацию о Вашем уроке: имя (напр., Математика), время начала (напр., 8 ч. 30 мин.), длительность (ex. 45 мин.), домашнее задание (не обязательно, напр., №5-7 стр. 14), место проведения (не обязательно, напр., Кабинет 302 или Спортивный зал)
🔜 Вся эта информация будет отображаться, когда Вы будете уведомлены об уроке. Вы также можете сделать урок еженедельным, если Ваш урок проводится соответствующим образом. Если, например, в будущем произойдёт замена и Вам нужно будет отредактировать урок, то Вы для данного типа уроков не сможете менять время начала и продолжительность
🌐 Вы также можете добавить урок для всех групп в классе. Создаются дубликаты урока для каждой группы

↪ Когда вы закончили с расписанием, можете перейти в ваш классный чат в Telegram и снова написать команду /class, выберите нужную группу и урок, о котором вы хотите узнать информацию
✅ Вы также будете уведомлены об уроке в классном чате, если соответствующий параметр включён в настройках класса
            """,
        'support':
            """
📍 Если вы обнаружили, что что-то не работает, либо же Вам нужна помощь, свяжитесь с @srnm9
            """,
        'max_lim':
            """
❗ В Вашем сообщении должно быть менее {symbols} символов
            """,
        'settings':
            """
⚙ Это настройки @srnmSchoolBot! Здесь Вы можете изменить язык бота:
            """,
        'class_create_name':
            """
Какое должно быть имя у Вашего нового класса?
            """,
        'class_verify':
            """
🤔 Теперь нужно подтвердить *{name}*!

👉 Добавьте @srnmSchoolBot в Ваш классный чат в Telegram и введите /verify в этом чате

📌 _Заметьте, что вы должны быть администратором этого чата_
            """,
        'class_exists':
            """
Класс в этом чате уже существует! ❌
            """,
        'not_admin':
            """
❗ Вы должны быть администратором этого чата, чтобы добавить класс в бота
            """,
        'no_classes':
            """
❗ У Вас нет классов, требующих подтверждения! Зайдите в @srnmSchoolBot чтобы создать новый класс
            """,
        'no_class':
            """
❗ Класса в этом чате не существует! Зайдите в @srnmSchoolBot чтобы создать новый класс, если Вы являетесь админом этого чата
            """,
        'no_groups':
            """
❗ У Вас нет групп в *{name}*! Если Вы являетесь админом этого класса, зайдите в @srnmSchoolBot чтобы создать по крайней мере одну группу в классе. Если же нет, попросите Вашего администратора сделать это
            """,
        'lesson_notification':
            """
*{clas} #группа\_{group}*
🕰 Ваш урок начинается через {start} минут
            """,
        'daily_notification':
            """
*{clas} #группа\_{group}*
Завтра у Вас будут следующие уроки:
            """,
        'no_lessons':
            """
*{clas} #группа\_{group}* завтра у Вас нет уроков!
            """,
        'class_added':
            """
Класс успешно добавлен! ✅

Введите /class
            """,
        'class_choose':
            """
🏫 Вот Ваши классы. Выберите один, с которым будете работать сейчас:
            """,
        'class_now':
            """
Это Ваш класс *{name}* 👈

⚙ Вы можете изменить его имя, удалить его, изменить его настройки и выбрать группу, чтобы изменять расписание
            """,
        'class_change_name':
            """
Какое новое имя подходит для Вашего класса {name}? 🤔
            """,
        'class_settings':
            """
Это настройки Вашего класса *{name}*:

🔻 Вы можете изменять администраторов класса
🔻 Смените язык
🔻 Включите/выключите уведомления о предстоящих уроках
🔻 Измените время уведомлений
🔻 Смените часовой пояс
            """,
        'class_delete':
            """
❓ Уверены, что хотите удалить Ваш класс {name}? *ВСЕ ДАННЫЕ О ВАШИХ УРОКАХ И ГРУППАХ БУДУТ УДАЛЕНЫ!!!* ❓
            """,
        'class_deleted':
            """
Класс {name} был успешно *удалён*! Введите /class чтобы создать новый или выбрать из существующих
            """,
        'class_settings_tz':
            """
🌏 Выберите временную зону класса, чтобы получать уведомления в верное время
            """,
        'class_settings_time':
            """
⌚ Выберите время, в которое Ваш класс *{name}* будет уведомлен за день до начала уроков

🕰 После этого выберите время, за которое до начала урока Вы будете уведомлены 
            """,
        'class_admins':
            """
Вот все администраторы *{name}*! Вы можете удалить этих админов, кроме себя

Также можете добавить других администраторов Вашего класса
            """,
        'class_add_admin':
            """
Чтобы добавить админа в *{name}*, введите его Telegram ID

Попросите этого человека использовать @userinfobot чтобы получить его Telegram ID
            """,
        'group_create_name':
            """
Какое название должно быть у группы *{name}*?
            """,
        'group_choose':
            """
Вот группы *{name}*! Выберите ту, чьё расписание собираетесь изменить 👈 
            """,
        'group_choose_timetable':
            """
Вот группы *{name}*! Выберите ту, чьё расписание Вас интересует 👈 
            """,
        'group_now':
            """
Это *{clas} {group}*. Выберите, что вы хотите сделать 👇
            """,
        'group_change_name':
            """
Какое имя вы предпочитаете вместо *{clas} {group}*? 🤔 
            """,
        'group_delete':
            """
Вы уверены, что хотите удалить группу *{group}* Вашего класса *{clas}*? Ваше расписание для этой группы будет также *удалено*! ❌
            """,
        'group_timetable':
            """
🗓 Это расписание *{clas} {group}*!

🤔 Здесь Вы можете создать новый урок, либо изменить уже существующий
            """,
        'timetable':
            """
🗓 Это расписание *{clas} {group}*!

🤔 Здесь Вы можете смотреть информацию об уроках
            """,
        'lesson_create_name':
            """
Какое название у создаваемого урока? 📕
            """,
        'lesson_name':
            """
Какое новое название будет у урока *{lesson}*? 📕
            """,
        'lesson_create':
            """
Здесь Вы можете изменять Ваш новый урок *{clas} {group}*! 👈

♻ Вы можете изменить его имя, выбрать время начала, его длительность, ввести домашнее задание, изменить его место, выбрать, если урок является еженедельным, выбрать, нужно ли добавлять этот урок во все группы класса

А вот та информация об уроке, которая уже заполнена 👇
            """,
        'lesson':
            """
Здесь Вы можете редактировать урок *{clas} {group}*! 👈

♻ Вы можете изменить его имя, выбрать время начала, его длительность, ввести домашнее задание, изменить его место, выбрать, если урок является еженедельным, выбрать, нужно ли добавлять этот урок во все группы класса

А вот та информация об уроке, которая уже заполнена 👇
            """,
        'weekly_lesson':
            """
Здесь Вы можете редактировать урок *{clas} {group}*! 👈

🤔 Этот урок создан автоматически, так как Вы указали параметр Еженедельно в первоначальном уроке! Здесь вы можете только изменить его название, домашнее задание и место
👉 Также Вы можете вернуться к исходному уроку и применить изменения ко всем будущим урокам или же отменить изменения, то есть вернуть его к исходному уроку

А вот та информация об уроке, которая уже заполнена 👇
            """,
        'group_lesson':
            """
Вот информация об уроке *{clas} {group}* 👇
            """,
        'lesson_time':
            """
Здесь вы можете изменить время начала урока, а также его длительность ⏰
            """,
        'lesson_homework':
            """
Введите домашнее задание 📗
            """,
        'lesson_place':
            """
Выберите место для Вашего урока! Это может быть как номер аудитории или кабинета, так и целый адрес 📍
            """,
    }
}
