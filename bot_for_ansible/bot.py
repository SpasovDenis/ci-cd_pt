import logging
import re
import os
import psycopg2
from psycopg2 import Error
import paramiko
from dotenv import load_dotenv
from telegram import Update, ForceReply
from telegram.ext import Updater,CallbackContext, CommandHandler, MessageHandler, Filters, ConversationHandler
load_dotenv()

token = os.getenv('TOKEN')
TOKEN = token

# Подключаем логирование
logging.basicConfig(
    filename='logfile.txt', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def start(update: Update, context):
    user = update.effective_user
    update.message.reply_text(f'Привет, {user.full_name}!')


def helpCommand(update: Update, context):
    update.message.reply_text('Вы можете использовать следующие комманды:\n 1)/find_email - ищет email-адреса в вашем тексте; \n 2)/find_phone_number - ищет телефонные номера в вашем тексте; \n 3) /verify_password - проверяет сложность вашего пароля; \n 4) /get_release - собирает информацию о релизе удаленного сервера; \n 5) /get_uname - собирает информацию об архитектуре процессора, имени хоста системы и версии ядра удаленного сервера; \n 6) /get_uptime - собирает информацию о времени работы удаленного сервера; \n 7) /get_df - собирает информацию о состоянии файловой системы удаленного сервера; \n 8) /get_free - собирает информацию о состоянии оперативной памяти удаленного сервера; \n 9) /get_mpstat - собирает информацию о производительности системы удаленного сервера; \n 10) /get_w - собирает информацию о работающих пользователях удаленного сервера; \n 11) /get_auths - собирает логи последних 10 входо на удаленный сервер; \n 12) /get_critical - собирает логи последних 5 критических событий на удаленном сервере; \n 13) /get_ps - собирает информацию о запущенных процессах удаленного сервера; \n 14) /get_ss - собирает информацию об используемых портах удаленного сервера; \n 15) /get_apt_list - собирает информацию об установленных пакетах удаленного сервера(можно выбрать вывод информации обо всех пакетах или о выбранном вами); \n 16) /get_services - собирает информацию о запущенных сервисах удаленного сервера; \n 17) /get_emails - выводит адреса почты из таблицы emails; \n 18) /get_phone_numbers - выводит номера телефонов из таблицы phone_numbers; \n 20) /get_repl_logs - выводит логи о репликации БД')


def findPhoneNumbersCommand(update: Update, context):
    update.message.reply_text('Введите текст для поиска телефонных номеров: ')

    return 'find_phone_number'

def findEmailCommand(update: Update, context):
    update.message.reply_text('Введите текст для поиска email-адресов: ')

    return 'find_email'

def verifyPassCommand(update: Update, context):
    update.message.reply_text('Введите пароль для проверки сложности:')

    return 'verify_password'

def getaptCommand(update: Update, context):
    update.message.reply_text('Введите all, если необходима информация обо всех пакетах, или название пакета, информаци о котором вам необходима:')

    return 'get_apt_list'

def getrealeseCommand(update: Update, context):
    host = os.getenv('RM_HOST')
    port = os.getenv('RM_PORT')
    username = os.getenv('RM_USER')
    password = os.getenv('RM_PASSWORD')

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('cat /etc/os-release')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')
    update.message.reply_text(data)

def getunameCommand(update: Update, context):
    host = os.getenv('RM_HOST')
    port = os.getenv('RM_PORT')
    username = os.getenv('RM_USER')
    password = os.getenv('RM_PASSWORD')

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('hostnamectl')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')
    update.message.reply_text(data)

def getuptimeCommand(update: Update, context):
    host = os.getenv('RM_HOST')
    port = os.getenv('RM_PORT')
    username = os.getenv('RM_USER')
    password = os.getenv('RM_PASSWORD')

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('uptime')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')
    update.message.reply_text(data)

def getdfCommand(update: Update, context):
    host = os.getenv('RM_HOST')
    port = os.getenv('RM_PORT')
    username = os.getenv('RM_USER')
    password = os.getenv('RM_PASSWORD')

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('df -a')
    data = stdout.read() + stderr.read()
    decoded_data = data.decode('utf-8')
    client.close()
    decoded_data = str(decoded_data).replace('\\n', '\n').replace('\\t', '\t')
    update.message.reply_text(decoded_data)

def getfreeCommand(update: Update, context):
    host = os.getenv('RM_HOST')
    port = os.getenv('RM_PORT')
    username = os.getenv('RM_USER')
    password = os.getenv('RM_PASSWORD')

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('free')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')
    update.message.reply_text(data)

def getmpstatCommand(update: Update, context):
    host = os.getenv('RM_HOST')
    port = os.getenv('RM_PORT')
    username = os.getenv('RM_USER')
    password = os.getenv('RM_PASSWORD')

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('mpstat')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')
    update.message.reply_text(data)

def getwCommand(update: Update, context):
    host = os.getenv('RM_HOST')
    port = os.getenv('RM_PORT')
    username = os.getenv('RM_USER')
    password = os.getenv('RM_PASSWORD')

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('w')
    data = stdout.read() + stderr.read()
    decoded_data = data.decode('utf-8')
    client.close()
    decoded_data = str(decoded_data).replace('\\n', '\n').replace('\\t', '\t')
    update.message.reply_text(decoded_data)

def getauthsCommand(update: Update, context):
    host = os.getenv('RM_HOST')
    port = os.getenv('RM_PORT')
    username = os.getenv('RM_USER')
    password = os.getenv('RM_PASSWORD')

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('last -10')
    data = stdout.read() + stderr.read()
    decoded_data = data.decode('utf-8')
    client.close()
    decoded_data = str(decoded_data).replace('\\n', '\n').replace('\\t', '\t')
    update.message.reply_text(decoded_data)

def getcritCommand(update: Update, context):
    host = os.getenv('RM_HOST')
    port = os.getenv('RM_PORT')
    username = os.getenv('RM_USER')
    password = os.getenv('RM_PASSWORD')

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('journalctl -p crit -n 5')
    data = stdout.read() + stderr.read()
    decoded_data = data.decode('utf-8')
    client.close()
    decoded_data = str(decoded_data).replace('\\n', '\n').replace('\\t', '\t')
    update.message.reply_text(decoded_data)

def getpsCommand(update: Update, context):
    host = os.getenv('RM_HOST')
    port = os.getenv('RM_PORT')
    username = os.getenv('RM_USER')
    password = os.getenv('RM_PASSWORD')

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('ps -A u | head -n 10')
    data = stdout.read() + stderr.read()
    decoded_data = data.decode('utf-8')
    client.close()
    decoded_data = str(decoded_data).replace('\\n', '\n').replace('\\t', '\t')
    update.message.reply_text(decoded_data)

def getssCommand(update: Update, context):
    host = os.getenv('RM_HOST')
    port = os.getenv('RM_PORT')
    username = os.getenv('RM_USER')
    password = os.getenv('RM_PASSWORD')

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('ss | head -n 10')
    data = stdout.read() + stderr.read()
    decoded_data = data.decode('utf-8')
    client.close()
    decoded_data = str(decoded_data).replace('\\n', '\n').replace('\\t', '\t')
    update.message.reply_text(decoded_data)

def getservicesCommand(update: Update, context):
    host = os.getenv('RM_HOST')
    port = os.getenv('RM_PORT')
    username = os.getenv('RM_USER')
    password = os.getenv('RM_PASSWORD')

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('systemctl --type=service --state=running')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')
    update.message.reply_text(data)

def getemailCommand(update: Update, context):
    connection = None
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    host = os.getenv('DB_HOST')
    port = os.getenv('DB_PORT')
    database = os.getenv('DB_DATABASE')
    try:
        connection = psycopg2.connect(user=user,
                                      password=password,
                                      host=host,
                                      port=port,
                                      database=database)

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM emails;")
        data = cursor.fetchall()
        email = ''
        k=0
        for i in data:#range(len(data))
            email += f'ID:{data[k][0]}. email:{data[k][1]}\n'  # Записываем очередной номер
            k +=1
        update.message.reply_text(email)
        #update.message.reply_text(data)
        logging.info("Команда успешно выполнена")
    except (Exception, Error) as error:
        logging.error("Ошибка при работе с PostgreSQL: %s", error)
    finally:
        if connection is not None:
            cursor.close()
            connection.close()

def getphoneCommand(update: Update, context):
    connection = None
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    host = os.getenv('DB_HOST')
    port = os.getenv('DB_PORT')
    database = os.getenv('DB_DATABASE')
    try:
        connection = psycopg2.connect(user=user,
                                      password=password,
                                      host=host,
                                      port=port,
                                      database=database)

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM phone_numbers;")
        data = cursor.fetchall()
        ph = ''
        k=0
        for i in data:#range(len(data))
            ph += f'ID:{data[k][0]}. номер:{data[k][1]}\n'  # Записываем очередной номер
            k +=1
        update.message.reply_text(ph)
        #update.message.reply_text(data)
        logging.info("Команда успешно выполнена")
    except (Exception, Error) as error:
        logging.error("Ошибка при работе с PostgreSQL: %s", error)
    finally:
        if connection is not None:
            cursor.close()
            connection.close()

def getreglogCommand(update: Update, context):
    host = os.getenv('DB_HOST')
    port = os.getenv('DB_PORT')
    username = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command("cat /var/log/postgresql/postgresql-15-main.log | grep 'replica' | tail -n 10")
    data = stdout.read() + stderr.read()
    decoded_data = data.decode('utf-8')
    client.close()
    decoded_data = str(decoded_data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    update.message.reply_text(decoded_data)


def find_phone_number(update: Update,context: CallbackContext):
    user_input = update.message.text  # Получаем текст, содержащий(или нет) номера телефонов

    phoneNumRegex = re.compile(r'(8|\+7)(\s|-|\.)?(\d{3}|\(\d{3}\))(\s|-|\.)?(\d{3})(\s|-|\.)?(\d{2})(\s|-|\.)?(\d{2})')  # все форматы

    phoneNumberList = phoneNumRegex.findall(user_input)  # Ищем номера телефонов

    if not phoneNumberList:  # Обрабатываем случай, когда номеров телефонов нет
        update.message.reply_text('Телефонные номера не найдены')
        return ConversationHandler.END  # Завершаем выполнение функции
    phoneNumbers = ''  # Создаем строку, в которую будем записывать номера телефонов
    for i in range(len(phoneNumberList)):
        phoneNumbers += f'{i + 1}. {"".join(phoneNumberList[i])}\n'  # Записываем очередной номер
    update.message.reply_text(phoneNumbers)
    update.message.reply_text('Желаете записать найденные номера телефонов в базу данных?( Напишите да или yes, если желаете, и нет или no, если не желаете)')
    context.user_data['phoneNumberList'] = phoneNumbers
    return 'save_phone_numbers'


def save_phone_numbers(update: Update, context: CallbackContext) -> int:
    answer = update.message.text.lower()
    connection = None
    if 'да' in answer or 'yes' in answer:
        phone_numbers = context.user_data.get('phoneNumberList', [])
        phone_numbers = re.split(r'\s*\d+\.\s*', phone_numbers)[1:]
        cleaned_number = []
        for number in phone_numbers:
            # Удаление нумерации, сохранение знака плюса, пробелов и дефисов
            clean_number = re.sub(r'(?<!\+)[^\d\s\-\(\)]', '', number).rstrip('\n')
            cleaned_number.append(clean_number)
        if cleaned_number:
            try:
                connection = psycopg2.connect(user=os.getenv('DB_USER'),
                                                password=os.getenv('DB_PASSWORD'),
                                                host=os.getenv('DB_HOST'),
                                                port=os.getenv('DB_PORT'),
                                                database=os.getenv('DB_DATABASE'))
                cursor = connection.cursor()
                for phone_number in phone_numbers:
                    cursor.execute("INSERT INTO phone_numbers (numbers) VALUES (%s);", (phone_number,))
                connection.commit()
                update.message.reply_text('Номера телефонов успешно сохранены в базу данных.')
            except Exception as e:
                update.message.reply_text(f'Произошла ошибка при сохранении номеров: {e}')
            finally:
                if connection:
                    cursor.close()
                    connection.close()
                    return ConversationHandler.END  # Завершаем диалог после сохранения номеров
    elif 'нет' in answer or 'no' in answer:
        update.message.reply_text('Сохранение номеров отменено.')
        return ConversationHandler.END  # Завершаем диалог, если пользователь отказался сохранять номера
    return ConversationHandler.END

def find_email(update: Update, context: CallbackContext):
    user_input = update.message.text  # Получаем текст, содержащий(или нет) email

    emailRegex = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')  # формат 8 (000) 000-00-00

    emailList = emailRegex.findall(user_input)  # Ищем email

    if not emailList:  # Обрабатываем случай, когда email
        update.message.reply_text('Email-адреса не найдены')
        return ConversationHandler.END  # Завершаем выполнение функции
    emails = ''  # Создаем строку, в которую будем записывать номера телефонов
    for i in range(len(emailList)):
        emails += f'{i + 1}. {emailList[i]}\n'  # Записываем очередной номер

    update.message.reply_text(emails)  # Отправляем сообщение пользователю
    update.message.reply_text('Желаете записать найденные email-адреса в базу данных?( Напишите да или yes, если желаете, и нет или no, если не желаете)')
    context.user_data['emailList'] = emailList
    return 'save_emails'

def save_emails(update: Update, context: CallbackContext) -> int:
    connection = None
    answer = update.message.text.lower()
    if 'да' in answer or 'yes' in answer:
        emailList = context.user_data.get('emailList', [])
        if emailList:
            try:
                connection = psycopg2.connect(user=os.getenv('DB_USER'),
                                                password=os.getenv('DB_PASSWORD'),
                                                host=os.getenv('DB_HOST'),
                                                port=os.getenv('DB_PORT'),
                                                database=os.getenv('DB_DATABASE'))
                cursor = connection.cursor()
                for email in emailList:
                    cursor.execute("INSERT INTO emails (mails) VALUES (%s);", (email,))
                connection.commit()
                update.message.reply_text('Email-адреса успешно сохранены в базу данных.')
            except Exception as e:
                update.message.reply_text(f'Произошла ошибка при сохранении адресов: {e}')
            finally:
                if connection:
                    cursor.close()
                    connection.close()
                    return ConversationHandler.END  # Завершаем диалог после сохранения адресов
    elif 'нет' in answer or 'no' in answer:
        update.message.reply_text('Сохранение номеров отменено.')
        return ConversationHandler.END  # Завершаем диалог, если пользователь отказался сохранять адреса
    return ConversationHandler.END


def verify_password(update: Update, context):
    user_input = update.message.text  # Получаем пароль
    passRegex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&*()])[a-zA-Z0-9!@#$%^&*()]{8,}$')  # Проверка пароля

    checkpass = bool(passRegex.match(user_input)) # И
    if checkpass is True:  # Обрабатываем случай, когда email
        update.message.reply_text('Пароль сложный')
        return ConversationHandler.END
    else:
        update.message.reply_text('Пароль простой')
        return ConversationHandler.END

def get_apt_list(update: Update, context):
    user_input = update.message.text  #
    host = os.getenv('RM_HOST')
    port = os.getenv('RM_PORT')
    username = os.getenv('RM_USER')
    password = os.getenv('RM_PASSWORD')

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    aptRegex = re.compile(r'all')  #

    checkall = bool(aptRegex.match(user_input))
    if checkall is True:
        stdins, stdout, stderr = client.exec_command('dpkg-query -l | head -n 10')
        data = stdout.read() + stderr.read()
        decoded_data = data.decode('utf-8')
        client.close()
        decoded_data = str(decoded_data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
        update.message.reply_text(decoded_data)
    else:
        stdin, stdout, stderr = client.exec_command('dpkg-query -s '+ user_input)
        data = stdout.read() + stderr.read()
        decoded_data = data.decode('utf-8')
        client.close()
        decoded_data = str(decoded_data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
        update.message.reply_text(decoded_data)

    return ConversationHandler.END  # Завершаем работу обработчика диалога

def main():
    updater = Updater(TOKEN, use_context=True)

    # Получаем диспетчер для регистрации обработчиков
    dp = updater.dispatcher

    # Обработчик диалога
    convHandlerFindPhoneNumbers = ConversationHandler(
        entry_points=[CommandHandler('find_phone_number', findPhoneNumbersCommand)],
        states={
            'find_phone_number': [MessageHandler(Filters.text & ~Filters.command, find_phone_number)],
            'save_phone_numbers': [MessageHandler(Filters.text & ~Filters.command, save_phone_numbers)]
        },
        fallbacks=[]
    )
    convHandlerFindemail = ConversationHandler(
        entry_points=[CommandHandler('find_email', findEmailCommand)],
        states={
            'find_email': [MessageHandler(Filters.text & ~Filters.command, find_email)],
            'save_emails': [MessageHandler(Filters.text & ~Filters.command, save_emails)]
        },
        fallbacks=[]
    )
    convHandlerVerifyPass = ConversationHandler(
        entry_points=[CommandHandler('verify_password', verifyPassCommand)],
        states={
            'verify_password': [MessageHandler(Filters.text & ~Filters.command, verify_password)],
        },
        fallbacks=[]
    )
    convHandlerGetApt = ConversationHandler(
        entry_points=[CommandHandler('get_apt_list', getaptCommand)],
        states={
            'get_apt_list': [MessageHandler(Filters.text & ~Filters.command, get_apt_list)],
        },
        fallbacks=[]
    )




    # Регистрируем обработчики команд
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", helpCommand))
    dp.add_handler(convHandlerFindPhoneNumbers)
    dp.add_handler(convHandlerFindemail)
    dp.add_handler(convHandlerVerifyPass)
    dp.add_handler(convHandlerGetApt)
    dp.add_handler(CommandHandler("get_release", getrealeseCommand))
    dp.add_handler(CommandHandler("get_uname", getunameCommand))
    dp.add_handler(CommandHandler("get_uptime", getuptimeCommand))
    dp.add_handler(CommandHandler("get_df", getdfCommand))
    dp.add_handler(CommandHandler("get_free", getfreeCommand))
    dp.add_handler(CommandHandler("get_mpstat", getmpstatCommand))
    dp.add_handler(CommandHandler("get_w", getwCommand))
    dp.add_handler(CommandHandler("get_auths", getauthsCommand))
    dp.add_handler(CommandHandler("get_critical", getcritCommand))
    dp.add_handler(CommandHandler("get_ps", getpsCommand))
    dp.add_handler(CommandHandler("get_ss", getssCommand))
    dp.add_handler(CommandHandler("get_services", getservicesCommand))
    dp.add_handler(CommandHandler("get_emails", getemailCommand))
    dp.add_handler(CommandHandler("get_phone_numbers", getphoneCommand))
    dp.add_handler(CommandHandler("get_repl_logs", getreglogCommand))

    # Запускаем бота
    updater.start_polling()

    # Останавливаем бота при нажатии Ctrl+C
    updater.idle()


if __name__ == '__main__':
    main()
