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
    self.register_plugin('xep_0092')  # Software version
    self.register_plugin('xep_0199')  # XMPP Ping
    self.register_plugin('xep_0249')  # Direct MUC Invitations

    self.connected_event = asyncio.Event()
    self.add_event_handler('session_start', self.onSessionStart)
    self.add_event_handler('message', self.message)
    self.add_event_handler("groupchat_message", self.groupMessage)

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
    self.connected_event.set()

  async def deleteAccount(self):
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
    
  def signOut(self):
    self.disconnect()

  # --------------------------------- Mensajeria
  def sendDirectMessage(self, message):
    self.send_message(
      mto=self.current_chat,
      mbody=message,
      mtype='chat'
    )

  def sendGroupMessage(self, message):
    self.send_message(
      mto=self.current_chat,
      mbody=message,
      mtype='groupchat'
    )

  def joinChatRoom(self):
    self.plugin['xep_0045'].join_muc(
      self.current_chat,
      self.current_user.split('@')[0],
    )

  def message(self, msg):
    msg_from = str(msg['from'])
    msg_type = str(msg['mtype'])
    if (self.current_user in msg_from): return
    if (msg_type == 'groupchat'): return

    if (msg_type == 'chat'):
      if (self.current_chat in msg_from):
        print('[' + msg_from + ']: ' + str(msg['body'].split('@')[0]))
        return

    print('[NOTIFICATION]', msg)

  def groupMessage(self, msg):
    msg_from = str(msg['from'])
    if (self.current_user in msg_from): return

    msg_from = str(msg['mucnick'])
    print(msg, msg_from)
    # if (self.current_chat in msg_from):
    #   print('[' + msg_from + ']: ' + str(msg['body'].split('@')[0]))
    #   return

    print('[NOTIFICATION]', msg)

class AccountController2(slixmpp.ClientXMPP):
  def __init__(self, jid, password):
    slixmpp.ClientXMPP.__init__(self, jid, password)

    # Gesister plugin
    self.register_plugin('xep_0004')  # Data Forms
    self.register_plugin('xep_0030')  # Service Discovery
    self.register_plugin('xep_0045')  # Group Chat
    self.register_plugin('xep_0060')  # PubSub
    self.register_plugin('xep_0077')  # In Bound Registration
    self.register_plugin('xep_0092')  # Software version
    self.register_plugin('xep_0199')  # XMPP Ping
    self.register_plugin('xep_0249')  # Direct MUC Invitations

    self.connected_event = asyncio.Event()
    self.add_event_handler('session_start', self.onSessionStart)
    self.add_event_handler('message', self.message)

  async def onSessionStart(self, event):
    self.send_presence()
    await self.get_roster()
    print('---------------------------------------->', self.client_roster)
    print('---------------------------------------->', self.roster)

  # --------------------------------- Mensajeria
  def message(self, msg):
    print('MENSAJEEEEEE', msg)


if __name__ == '__main__':
  logging.basicConfig(level=logging.DEBUG, format='%(levelname)-8s %(message)s')
  client = AccountController2('brandontest@alumchat.fun', 'gallos')
  client.connect()
  client.process(forever=True)
