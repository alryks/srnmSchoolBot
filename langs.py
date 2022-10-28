langs = {
    'en': {
        'keyboards': {
            'edit_class': {
                'name': "⚙ Edit name",
                'delete': "❌ Delete class",
                'cancel': "🔙 Cancel"
            },
            'new_class': {
                'cancel': "🔙 Cancel"
            },
            'delete_class': {
                'yes': "👍 Yes, I am!",
                'no': "😢 Nooo!"
            },
            'sure_delete_class': {
                'yes': "✅ No doubt!",
                'no': "❌ Not on your life!"
            }
        },
        'start':
            """
Hi {name}! 👋

📅 I'm @srnmSchoolBot for scheduling your school *lessons* and reminding you about your *school tasks* 📝

📌 For more _info_ try /help
            """,
        'help':
            """
🤔 To use @srnmSchoolBot add it into *your class chat*
After that use _this commands_ in order and _follow instructions_:

📍 /class — firstly, you should create your class. Type in name of it. If it is already created, you can change its name or delete it with all data!

📍 /settings — after you have created your class, you should go to settings to choose the language and your timezone and change the notification system
            """,
        'not_group':
            """
❌ To use @srnmSchoolBot and its command you should chat with it in a group!

📍 For detailed instructions use /help
            """,
        'not_text':
            """
🤔 Make sure that what you send is a text message!
            """,
        'only_admin':
            """
❌ Only admin can do this!
            """,
        'edit_class':
            """
😍 This is your class: *{name}*

👉 Here you can change its name or *delete* it

_❗❗❗ WARNING ❗❗❗
Note that if you delete your class, all data including groups and timetables will be deleted_
            """,
        'edit_class_name':
            """
Choose a new name for your class...
            """,
        'edit_class_name_changed':
            """
♻ Class name was changed on *{name}*
            """,
        'new_class':
            """
What would be the name of your class?
            """,
        'new_class_created':
            """
🎉 Your class with name *{name}* has been successfully created!

📍 Don't forget to check out /settings before using the bot!
            """,
        'delete_class':
            """
❓ Are you sure you want to delete your class *{name}*? 

All your data will be deleted including your groups and timetables for this groups! ❌
            """,
        'sure_delete_class':
            """
🤔 *100% SURE???*
            """,
        'sure_delete_class_deleted':
            """
✅ Your class has been successfully deleted!

📍 You can create a new one via /class
            """
    }
}