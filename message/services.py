from usercp.models import User
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from threading import Thread
from startups.object import get_user_service
from . import models
from .forms import *
from startups.utils import *



def send_message_chat_instances_service(pk, track_info, context):
    """get message by primary key if it's exists and if the messages is not readed 
       is_readed of the message objects become True

    Arguments:
        pk {PRIMARY KEY/INT} -- a unique field to select the message we want
        track_info {DICT} -- dictionary contains of user id and ip to update status_of_user

    Returns:
        OBJECT -- returns receiver object for the form
    """    
    receiver = get_user_service(pk=pk)
    send_m_receiver = models.SendMessage.objects.filter(receiver=receiver)
    all_messages = models.AllMessages.objects.prefetch_related('send_message').filter(
        send_message__in=send_m_receiver)
    message_form = SendMessageForm()
    status = f"پیام {receiver.first_name} {receiver.last_name} را خوانده"
    status_of_user(track_info, status, 'seeing-message')
    context.update({'form': message_form, 'receiver': receiver, 'all_messages': all_messages})
    return receiver


def send_message_chat_service(form, user, receiver, track_info):
    """allow user to send message to the chosen user 

    Arguments:
        form {POST Method} -- to get message title
        user {OBJECT} -- requested user as sender
        receiver {OBJECT} -- the user that message sent to
        track_info {DICT} -- dictionary contains of user id and ip to update status_of_user

    Returns:
        BOOLEAN/ERROR -- returns True if form is valid else returns forms error
    """    
    message_form = SendMessageForm(form)
    if message_form.is_valid():
        message_form.instance.sender = user
        message_form.instance.receiver = receiver
        message_form.save()
        all_m = models.AllMessages.objects.create(
            message_title=form.get('message_title'), message_type='chat')
        all_m.send_message.add(message_form.instance)
        status = f"به {message_form.instance.receiver} پیام از نوع {all_m.message_type} فرستاد"
        status_of_user(track_info, status, 'sending-message')
        return True
    else:
        logger.error(str(message_form.errors))
        return message_form.errors


def show_messages_instance_service(pk, user, context):
    """get instance messages of the chat room that is selected if exists

    Arguments:
        pk {PRIMARY KEY/INT} -- the primary key of the message(chat room)
        user {OBJECT} -- if the receiver is the reqeusted user and has un readed messages the messages is_readed become True
        context {DICT} -- a dictionary to pass messages(all messages in chat room) and form to send replays

    Returns:
        OBJECT -- returns the chat room context
    """    
    the_m = models.AllMessages.objects.prefetch_related('send_message').get(pk=pk)
    for x in the_m.send_message.all():
        if x.receiver == user:
            mess = models.SendMessage.objects.get(pk=x.pk)
            if mess.is_readed == True: continue
            mess.is_readed = True
            mess.save()
    message_form = SendMessageForm()
    context.update({"all_messages": the_m, 'SendForm': message_form})
    return the_m


def show_message_send_service(form, user, track_info, the_m):
    """the form that sends replay message 
       the sender is requested user
       the receiver is the sender if the sender is not the requested user
       else the sender is the receiver that is not the requested user

    Arguments:
        form {POST Method} -- to define the method of the SendMessageForm
        user {OBJECT} -- requested user
        track_info {DICT} -- dictionary contains of user id and ip to update status_of_user
        the_m {OBJECT} -- selected message(chat room)

    Returns:
        BOOLEAN/STRING -- returns True if form is valid else returns forms error
    """    
    message_form = SendMessageForm(form)
    if message_form.is_valid():
        message_form.instance.sender = user
        message_form.instance.receiver = the_m.send_message.first().sender if the_m.send_message.first(
        ).sender != user else the_m.send_message.exclude(pk=user.pk).first().receiver
        message_form.save()
        the_m.send_message.add(message_form.instance)
        status = f"جواب پیام {message_form.instance.receiver} را داد"
        status_of_user(track_info, status, 'import-message-show')
        return True
    else:
        logger.error(str(message_form.errors))
        return message_form.errors



def send_message_error_instance_service():
    """define the reciever of message(that is the manager)

    Returns:
        OBJECT -- returns the manager user
    """
    return User.objects.filter(user_type='manager').first()


def send_message_error_service(form, user, url, track_info, receiver):
    """send fidback message from requested user to manager with the link of the requested page

    Arguments:
        form {POST Method} -- to define method and get message title
        user {OBJECT} -- requested user as sender of message
        url {STRING} -- the url of the page that error has been sent
        track_info {DICT} -- dictionary contains of user id and ip to update status_of_user
        receiver {OBJECT} -- the manager

    Returns:
        BOOLEAN/STRING -- returns True if form is valid else returns forms error
    """  
    message_form = SendMessageForm(form)
    if message_form.is_valid():
        message_form.instance.sender = user
        message_form.instance.receiver = receiver
        message_form.instance.chat_room = receiver.pk
        message_form.instance.url = url
        message_form.save()
        status = f"یک فیدبک فرستاد"
        status_of_user(track_info, status, 'import-send-message')
        all_m = models.AllMessages.objects.create(
            message_title=form.get('message_title'), message_type='error')
        all_m.send_message.add(message_form.instance)
        return True
    else:
        logger.error(str(message_form.errors))
        return message_form.errors


def notification_service(track_info, user, offset):
    """list of all notifications of requested user and if there is unreaded notification will make is_readed True

    Arguments:
        track_info {DICT} -- dictionary contains of user id and ip to update status_of_user
        user {OBJECT} -- requested user
        offset {GET Method} -- to get page number

    Returns:
        DICT -- returns dictionary of notification queryset
    """    
    status = f"لیست نوتیفیکیشن هایش را دید"
    status_of_user(track_info, status, 'import-notification-panel')
    notifications = models.Notification.objects.select_related('status').filter(user=user).order_by('-created_date')
    for notification in notifications:
        if notification.is_readed == True: continue
        notification.is_readed = True
        notification.save()

    paginator = Paginator(notifications, 30)
    page = offset
    notifications = paginator.get_page(page)
    return {'notifications': notifications }


def message_box_service(track_info, search, context):
    status = f"صفحه صندوق پیام را دید"
    status_of_user(track_info, status, 'import-message-box')
    error_messages = models.AllMessages.objects.prefetch_related('send_message').filter(
        message_type='error').order_by('-created_date')
    chat_messages = models.AllMessages.objects.prefetch_related('send_message').filter(
        message_type='chat').order_by('-created_date')[:5]
    context.update({"chat_messages": chat_messages, "error_messages": error_messages,})
    user_list = User.objects.all()
    if search.get("startup_search"):
        user_list = user_list.prefetch_related('startup').filter(is_admin=False).filter(
            user_type='startup').filter(startup__title__icontains=search.get("startup_search"))
        context.update({"user_list": user_list})
    if search.get("fname_search"):
        user_list = user_list.filter(is_admin=False).filter(
            first_name__icontains=search.get("fname_search"))
        context.update({"user_list": user_list})
    if search.get("lname_search"):
        user_list = user_list.filter(is_admin=False).filter(
            last_name__icontains=search.get("lname_search"))
        context.update({"user_list": user_list})
    if search.get("email_search"):
        user_list = user_list.filter(is_admin=False).filter(
            email__icontains=search.get("email_search"))
        context.update({"user_list": user_list})

    return True


def support_service(user, file_value, form, session, track_info, current_site, protocol):
    """get the phone number from session if exists else if user is authenticated will get phone from database else we don't pass any phone
       assgin user informaion to the SupportModel

    Arguments:
        user {OBJECT} -- requested user
        form {POST Method} -- get screen-shot(base-64)
        session {SESSION} -- to get phone number from session
        track_info {DICT} -- dictionary contains of user id and ip to update status_of_user

    Returns:
        BOOLEAN/STRING -- returns True if form is valid else returns forms errors
    """    
    if user.is_authenticated:
        the_phone = user.phone
        the_user = user
    elif session.get('phone'):
        the_phone = session.get('phone')
        the_user = get_user_service(phone=the_phone)
    else:
        the_phone = None
        the_user = None

    try:
        support_form = SupportForm(form)
        if support_form.is_valid():
            support_form.instance.user = the_user
            support_form.instance.phone = the_phone
            support_form.instance.image = file_value.get('screenshot')
            support_form.save()
            the_message = support_form.instance.content
            try:
                the_messages2 = f'کاربر با نام {support_form.instance.user.first_name} {support_form.instance.user.last_name} و شماره تماس {support_form.instance.user.phone} :'
            except:
                the_messages2 = f'کاربر با شماره تماس {the_phone} :'
            sub = 'گزارش پشتیبانی در روند ثبت نام'
            template = 'email/startup-email.html'
            to = 'lordofhell225@gmail.com'
            to2 = 'lordofhell226@gmail.com'
            image_url = ''.join([str(protocol), '://', str(current_site), str(support_form.instance.image.url)])
            Thread(target=send_email, args=(track_info,), kwargs={
                    "to": [to, to2], 'template': template, 'sub': sub, 'the_messages': the_message, 'the_messages2': the_messages2, 'image': image_url }).start()
            return True
        else:
            logger.error(str(support_form.errors))
            return support_form.errors
    except Exception as e:
        logger.error(str(e))
