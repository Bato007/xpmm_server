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
    print('6. Borrar cuenta')
    print('7. Cerrar sesion')
    option = input('[CLIENT] Ingrese su opcion: ')

    if (option == '1'):
      print('1. Mostrar contactos')
      server.signOut()
      user = INIT_STATE.copy()
    
    elif (option == '2'):
      print('2. Agregar contacto')
    
    elif (option == '3'):
      print('3. Mostrar detalles de un usuario')

    # Mensajes individuales
    elif (option == '4'):
      print('\t --- Mensajes directos ---')
      # Pregunta a quien mensajear
      server.current_chat = input('Ingrese el usuario con el que desea hablar: ') + '@' + SERVER
      send_message = ''
      print('------------------ INGRESE \'BACK\' PARA REGRESAR AL MENU PRINCIAPL ------------------')

      # Mientras este en el chat
      while (1):

        send_message = input('[CLIENT] Ingrese su mensaje\n')
        if (send_message == 'BACK'): break

        server.sendDirectMessage(send_message)

    # Mensajes grupales
    elif (option == '5'):
      print('\t --- Mensajes grupales ---')
      # server.current_chat = input('Ingrese al room chat al que se quiere unir: ')
      # server.current_chat = input('Ingrese al room chat al que se quiere unir: ')
      server.current_chat = 'amiwos'
      server.joinChatRoom()
      send_message = ''

      while (1):

        send_message = input('[CLIENT] Ingrese su mensaje\n')
        if (send_message == 'BACK'): break

        server.sendGroupMessage(send_message)

    elif (option == '6'):
      print('\t --- Borrar cuenta ---')
      asyncio.run(server.deleteAccount())
      server.signOut()
      server = None
      server_thread = None
      user = INIT_STATE.copy()

    elif (option == '7'):
      print('\t --- Cerrar Cuenta ---')
      server.signOut()
      server = None
      server_thread = None
      user = INIT_STATE.copy()
    
    else:
      print('[CLIENT] Opcion incorrecta')
