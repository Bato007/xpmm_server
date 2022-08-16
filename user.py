import xmpp, asyncio, slixmpp, logging

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

def signUp(username: str, password: str):
  jid = xmpp.JID(username)
  client = xmpp.Client(jid.getDomain(), debug=[])
  client.connect()
  return xmpp.features.register(client, jid.getDomain(), {
    'username': jid.getNode(),
    'password': password,
  })

class AccountController(slixmpp.ClientXMPP):
  def __init__(self, jid, password):
    slixmpp.ClientXMPP.__init__(self, jid, password)

    # Gesister plugin
    self.register_plugin('xep_0004')  # Data Forms
    self.register_plugin('xep_0030')  # Service Discovery
    self.register_plugin('xep_0045')  # Group Chat
    self.register_plugin('xep_0060')  # PubSub
    self.register_plugin('xep_0077')  # In Bound Registration
    self.register_plugin('xep_0085')  # Chat State Notifications
    self.register_plugin('xep_0092')  # Software version
    self.register_plugin('xep_0096')  # Jabber Search
    self.register_plugin('xep_0199')  # XMPP Ping
    self.register_plugin('xep_0249')  # Direct MUC Invitations

    self.connected_event = asyncio.Event()
    self.current_chat = ''
    self.add_event_handler('groupchat_message', self.groupMessage)
    self.add_event_handler('message', self.message)

    self.add_event_handler('chatstate_gone', self.contactGone)
    self.add_event_handler('chatstate_active', self.contactActive)
    self.add_event_handler('chatstate_inactive', self.contactInactive)
    self.add_event_handler('chatstate_paused', self.contactPause)
    self.add_event_handler('chatstate_composing', self.contactTyping)

    self.add_event_handler('session_start', self.onSessionStart)

  def threadSignIn(self):
    self.signIn()
    print('[Server]: Se ha conectado correctamente')
    self.process(forever=True)

  def signIn(self):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    self.connect()
    loop.run_until_complete(self.connected_event.wait())

  async def onSessionStart(self, event):
    self.send_presence()
    await self.get_roster()
    self.getContacts()
    self.connected_event.set()

  async def deleteAccount(self):
    await self.get_roster()
    await self._deleteAccount()
  
  async def _deleteAccount(self):
    query = self.Iq()
    query['type'] = 'set'
    query['from'] = self.boundjid.user
    query['register']['remove'] = True

    try:
        await query.send()
        self.disconnect()
        print('La cuenta fue borrada')
    except:
        print('Couldn\'t remove the account')
        self.disconnect()
    
  async def signOut(self):
    await self.get_roster()
    self.disconnect(wait=False)

  # --------------------------------- Contactos
  def getContacts(self):
    roster = self.client_roster.groups()
    self.contacts = []

    for group in roster:
      for user in roster[group]:
        self.client_roster[user]['subscription']

        # Obtener el estado
        conexions = self.client_roster.presence(user)
        if (not conexions):
          status = 'offline'
        else:
          for _, obj in conexions.items():
            if (obj['status'] == ''):
              status = 'online'
            else:
              status = obj['status']
        
        self.contacts.append([
          user,
          status
        ])
        status = ''

  async def addContact(self, newContact):
    self.send_presence_subscription(newContact)
    print('[SERVER]: Se ha agregado a la lista de contactos', newContact)

  # --------------------------------- Notificaciones
  def contactGone(self, event):
    msg_from = str(event['from'])
    if (self.current_chat in msg_from):
      print('[NOTIFICACION] ' + msg_from + ' se fue')

  def contactInactive(self, event):
    msg_from = str(event['from'])
    if (self.current_chat in msg_from):
      print('[NOTIFICACION] ' + msg_from + ' esta inactivo')

  def contactActive(self, event):
    msg_from = str(event['from'])
    if (self.current_chat in msg_from):
      print('[NOTIFICACION] ' + msg_from + ' esta activo')

  def contactPause(self, event):
    msg_from = str(event['from'])
    if (self.current_chat in msg_from):
      print('[NOTIFICACION] ' + msg_from + ' paro de escribir')

  def contactTyping(self, event):
    msg_from = str(event['from'])
    if (self.current_chat in msg_from):
      print('[NOTIFICACION] ' + msg_from + ' esta escribiendo...')

  async def sendNotification(self, contact, message):
    self.send_message(
      mto=contact,
      mbody=message,
      mtype='chat'
    )

  def sendPresence(self, show, status):
    self.send_presence(pshow=show, pstatus=status)

  # --------------------------------- Mensajeria
  async def sendDirectMessage(self, message):
    self.send_message(
      mto=self.current_chat,
      mbody=message,
      mtype='chat'
    )

  async def sendGroupMessage(self, message):
    self.plugin['xep_0045'].join_muc(
      self.current_chat,
      self.current_user.split('@')[0],
    )
    self.send_message(
      mto=self.current_chat,
      mbody=message,
      mtype='groupchat'
    )

  def message(self, msg):
    msg_from = str(msg['from'])
    msg_type = str(msg['type'])
    if (self.current_user in msg_from): return
    if (msg_type == 'groupchat'): return

    if (msg_type == 'chat'):
      if (self.current_chat in msg_from):
        print('[' + msg_from.split('/')[0] + ']: ' + str(msg['body'].split('@')[0]))
        return

    print('[NOTIFICACION] Mensaje de:', msg_from)

  def groupMessage(self, msg):
    msg_from = str(msg['from'])
    if (self.current_user in msg_from): return

    msg_nick = str(msg['mucnick'])
    if (msg_nick not in self.current_user):
      print('[' + msg_from.split('@')[0] +
        '-' + msg_from.split('/')[1] + ']: ' +
        str(msg['body'].split('@')[0])
      )
      return
