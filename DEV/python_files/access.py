import database_functions
import log

ERROR = -1
DENIED = 0
GRANTED = 1

USER_EXISTS = True
USER_DOESNT_EXIST = False

USER_IS_ADMIN = True
NOT_ADMIN = False

def verify_password(username,password):
    ''' Vérifying User exists 
        Parameters
            login
            password
        Returns
            status
            relative message
    '''
    status, result = database_functions.get_password(username)
    if status=='KO':
        return { 'status': ERROR, 'error_code': log.error_messages['DATABASE_ERROR'] }
    else:
        if result!=password:
            return { 'status': DENIED, 'error_code': log.error_messages['BAD_PASSWORD'] }
        else:
            return { 'status': GRANTED, 'error_code': '' }

def verify_user_login(username,):
    ''' Vérifying User exists 
        Parameters
            login
        Returns
            status
    '''    
    status, results = database_functions.get_users_username()
    if status=='KO':
        return ERROR
    else:
        if username in results:    
            return USER_EXISTS
        else:
            return USER_DOESNT_EXIST

def verify_admin_login(username):
    ''' Vérifying User is an admin 
        Parameters
            login
        Returns
            status
    '''
    if username == "admin":
        return USER_IS_ADMIN
    else:
        return NOT_ADMIN

def verify_user_access(username,password):
    ''' Verifying user access : login then password
        Parameters
            login
            password
        Returns
            status
            relative message
    '''
    return_from_verify_user_login=verify_user_login(username)
    if return_from_verify_user_login==ERROR:
        return { 'status': ERROR, 'error_code': log.error_messages['DATABASE_ERROR'] }    
    elif return_from_verify_user_login==USER_DOESNT_EXIST:
        return { 'status': DENIED, 'error_code': log.error_messages['USER_UNKNOWN'] }    
    else:
        return verify_password(username,password)
        
def verify_admin_access(username,password):
    ''' Verifying admon access : login then password
        Parameters
            login
            password
        Returns
            status
            relative message
    '''
    if verify_admin_login(username)==NOT_ADMIN:
        return { 'status': DENIED, 'error_code': log.error_messages['NOT_ADMIN'] }    
    else:
        return verify_password(username,password)

