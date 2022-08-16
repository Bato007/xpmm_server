import asyncio, logging
import user as accountCTL
from user import AccountController
from time import sleep
from threading import Thread

logging.basicConfig(level=logging.DEBUG, format='%(levelname)-8s %(message)s')

# Initial data for the 
SERVER = 'alumchat.fun'
INIT_STATE = {
  'username': None,
  'password': None,
}

server = None
server_thread = None
user = INIT_STATE.copy()
option = '1'

# Menu
while (1):

  # No ha iniciado sesion
  if ((user['username'] is None) or (user['password'] is None)):
    print(' CHAT SERVER ')
    print('1. Iniciar sesion')
    print('2. Crear cuenta')
    print('3. Salir')
    option = input('[CLIENT] Ingrese su opcion: ')

    if (option == '1'):
      print('\n --- SIGN IN ---')
      # username = input('Ingrese su usuario: ') + '@' + SERVER
      # password = input('Ingrese su contrasenia: ')
      username = 'brandontest@alumchat.fun'
      password = 'gallos'

      server = AccountController(username, password)
      server.current_user = username
      server_thread = Thread(target=server.threadSignIn)
      server_thread.start()

      sleep(5)
      user['username'] = username
      user['password'] = password

    else:
      print('\n --- SIGN UP ---')
      username = input('[CLIENT] Ingrese su usuario: ') + '@' + SERVER
      password = input('[CLIENT] Ingrese su contrasenia: ')
      wasCreated = accountCTL.signUp(username, password)

      if (wasCreated):
        print('\n[CLIENT] Cuenta creada correctamente')
      else:
        print('\n[CLIENT] La cuenta no pudo ser creada')
  
  # Ya inicio sesion
  else:
    print('\n\tMenu Principal ')
    print('1. Mostrar contactos')
    print('2. Agregar contacto')
    print('3. Mostrar detalles de un usuario')
    print('4. Mensajes directos')
    print('5. Mensajes grupales')
    print('6. Enviar notificacion')
    print('7. Definir mensaje de presencia')
    print('da. Borrar cuenta')
    print('cs. Cerrar sesion')
    option = input('[CLIENT] Ingrese su opcion: ')

    # Mostar contactos
    if (option == '1'):
      print('\t --- Mostrar Contactos ---')
      server.getContacts()

      for contact in server.contacts:
        print('-> User: ' + contact[0] + '\t\tStatus: ' + contact[1] )
    
    # Agregar contacto
    elif (option == '2'):
      print('\t --- Agregar Contacto ---')
      newContact = input('Ingrese el nombre del contacto nuevo: ') + '@' + SERVER
      server.addContact(newContact)
    
    # Mostrar info de un usuario
    elif (option == '3'):
      print('\t --- Mostrar un Contacto ---')
      toShow = input('Ingrese el nombre del usuario que desea observar: ') + '@' + SERVER
      server.getContacts()

      showed = False
      for contact in server.contacts:
        if toShow == contact[0]:
          showed = True
          print('-> User: ' + contact[0] + '\t\tStatus: ' + contact[1] )

      if (not showed):
        print('[CLIENT] No se encuentra en su lista de contactos')

    # Mensajes individuales
    elif (option == '4'):
      print('\n\t --- Mensajes directos ---')
      # Pregunta a quien mensajear
      server.current_chat = input('Ingrese el usuario con el que desea hablar: ') + '@' + SERVER
      send_message = ''
      print('------------------ INGRESE \'BACK\' PARA REGRESAR AL MENU PRINCIAPL ------------------')

      # Mientras este en el chat
      while (1):

        send_message = input('[CLIENT] Ingrese su mensaje\n')
        if (send_message == 'BACK'): break

        asyncio.run(server.sendDirectMessage(send_message))

    # Mensajes grupales
    elif (option == '5'):
      print('\n\t --- Mensajes grupales ---')
      server.current_chat = input('[CLIENT] Ingrese al grupo que se desea unir: ') + '@conference.' + SERVER
      send_message = ''

      while (1):
        send_message = input('[CLIENT] Ingrese su mensaje\n')
        if (send_message == 'BACK'): break

        asyncio.run(server.sendGroupMessage(send_message))
    
    # Se envian notifiicaciones
    elif (option == '6'):
      print('\n\t --- Notificaciones ---')
      send_message = ''

      send_message = input('[CLIENT] Ingrese su notificacion para sus contactos\n')

      for contact in server.contacts:
        asyncio.run(server.sendNotification(contact[0], send_message))

    # Se envian notifiicaciones
    elif (option == '7'):
      options = ['chat', 'away', 'xa', 'dnd']
      print('\n\t --- Mensaje de presencia ---')
      print('1. Disponible')
      print('2. Afuera')
      print('3. No disponible')
      print('4. Ocupado')
      option = input('Ingrese la opcion: ')
      status = input('Ingrese su nuevo estado: ')

      try:
        option = int(option) - 1
      except:
        option = 0

      server.sendPresence(options[option], status)

    # Borrar cuenta
    elif (option == 'da'):
      print('\n\t --- Borrar cuenta ---')
      asyncio.run(server.deleteAccount())
      server.signOut()
      server = None
      server_thread = None
      user = INIT_STATE.copy()

    # Cerrar sesion
    elif (option == 'cs'):
      print('\n\t --- Cerrar Cuenta ---')
      asyncio.run(server.signOut())
      server = None
      server_thread = None
      user = INIT_STATE.copy()
    
    else:
      print('[CLIENT] Opcion incorrecta')
