# -*- coding: utf-8 -*-
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler, CallbackQueryHandler)
import random
import string
''' ---- START: PASSWORD GENERATION ---- '''
def digits(n):
    s = ''
    while (n >0):
        s = s + str(random.randint(0,9))
        n = n - 1
    return s

def letters(n):
    return ''.join(random.choice(string.ascii_letters) for x in range(n))

def lettersanddigits(n):
    return ''.join(random.choice(string.ascii_letters + string.digits) for x in range(n))

def everything(n):
    return ''.join(random.choice(string.punctuation + string.ascii_letters + string.digits) for x in range(n))

''' ---- END: PASSWORD GENERATION ---- '''
''' ---- START: LOGGING CODE ---- '''
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
''' ---- END: LOGGING CODE ---- '''
''' ----- START: STATES ----- '''
PASSWORDLEN, PASSWORDGEN, REPEAT = range(3)
''' ----- END: STATES ----- '''

# Commands required:
# 1. start - letters, digits and special characters return value to be a conditional 
# 2. error handling
# 3. main method at the bottom


def start(update, context):
    user = update.message.from_user
    logger.info("%s has initiated Password Generator Bot", user.last_name)
    reply_keyboard = [['Letters with Digits', 'Digits Only'],
                 ['Letters Only', 'Letters, Digits and Special Characters']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard = True)
    update.message.reply_text('Hi! I am a Password Generator Bot. \n'
                                'I will recommend a good password of 8 characters for you! 我会帮你选出密码！;)\n'
                                'Send /cancel to stop talking to me.\n\n'
                                'Choose Your Password Preference! \n选你的密码方面！', reply_markup=markup)
    
    return PASSWORDLEN

def passwordLen(update, context):
    user = update.message.from_user
    global user_choice_type 
    user_choice_type = update.message.text
    logger.info("%s has initiated Password Generator Bot", user.last_name)
    update.message.reply_text('What is the length of your password? Please key an integer\nA Good Password has more than 10 Characters!')
    return PASSWORDGEN

def passwordGen(update, context):
    user = update.message.from_user
    user_choice_len = update.message.text
    num = int(user_choice_len)
    logger.info("%s chose option: %s", user.last_name, update.message.text)
    ''' Conditionals for splitting of User Preferences ''' 
    if user_choice_type == 'Digits Only':
        update.message.reply_text('Your password is: ' + digits(num))
    elif user_choice_type == 'Letters Only':
        update.message.reply_text('Your password is: ' + letters(num))
    elif user_choice_type == 'Letters with Digits':
        update.message.reply_text('Your password is: ' + lettersanddigits(num))
    else : 
        update.message.reply_text('Your password is: ' + everything(num))

    update.message.reply_text('/repeat to choose another password! \n/cancel to stop the bot',  
                        reply_markup=ReplyKeyboardRemove())
    return REPEAT

def repeat(update, context):
    user = update.message.from_user 
    reply_keyboard = [['Letters with Digits', 'Digits Only'],
                 ['Letters Only', 'Letters, Digits and Special Characters']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard = True)
    update.message.reply_text('Was the password not good enough? :(\nYou might want to try another option!',
                                reply_markup = markup)
    return PASSWORDLEN


def cancel(update, context):
    user = update.message.from_user
    logger.info("%s canceled the conversation.", user.last_name)
    update.message.reply_text('Bye! I hope we can talk again some day. \n' + 
                                '/start to start the bot again',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def help(update, context):
    update.message.reply_text("Use /start to test this bot.")

def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("TOKEN", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={

            PASSWORDLEN: [MessageHandler(Filters.regex(
                '^(Letters with Digits|Digits Only|Letters Only|Letters, Digits and Special Characters)$'), 
                passwordLen)],

            PASSWORDGEN: [MessageHandler(Filters.text, 
                 passwordGen)],

            REPEAT: [CommandHandler('repeat', repeat)]

        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )
    
    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
