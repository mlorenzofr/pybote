#!/usr/bin/python
# -*- coding: latin_1 -*-

# =========={ INICIO DE LA LICENCIA DE ESTE SOFTWARE }==========
#
#  Copyright (c) 2005-2006, Manuel Lorenzo Frieiro
#  All rights reserved.
#
#  Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
#
#  * Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
#  * Neither the name of the Manuel Lorenzo Frieiro nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# =========={ FIN DE LA LICENCIA DE ESTE SOFTWARE }==========


# Información del módulo
#========================

__module_name__ = 'IRC-pyBOTe'
__module_version__ = '0.5.2'
__module_date__ = '2007/03/12'
__module_author__ = 'Manuel Lorenzo Frieiro'
__module_description__ = 'Módulo para la gestión de comunicaciones con el servidor de IRC.'

# Módulos necesarios
#====================

import socket
import threading
import ConfigParser
import xmlDB
import re
import time
import logs

# Variables Globales
#====================

COLOR = '\003'
BOLD = '\002'
UNDERLINE = '\037'
REVERSE = '\026'
CLEAR = '\017'
CTCP = '\001'

WHITE = '%s0' % COLOR
BLACK = '%s1' % COLOR
NAVY_BLUE = '%s2' % COLOR
GREEN = '%s3' % COLOR
RED = '%s4' % COLOR
BROWN = '%s5' % COLOR
PURPLE = '%s6' % COLOR
ORANGE = '%s7' % COLOR
YELLOW = '%s8' % COLOR
LIME_GREEN = '%s9' % COLOR
TEAL = '%s10' % COLOR
CYAN = '%s11' % COLOR
BLUE = '%s12' % COLOR
PINK = '%s13' % COLOR
DARK_GRAY = '%s14' % COLOR
GRAY = '%s15' % COLOR

# Clases
#========

# DCCObject: objeto que contiene los datos necesarios para una comunicación DCC
class DCCObject:
    def __init__(self, client, port, ircObj, local=True, IPaddr=''):
         self.ircObject = ircObj
	 self.firstSocket = ''
	 self.secondSocket = ''
	 self.ip = IPaddr
	 self.client = client
	 self.port = int(port)
	 self.line = u''
	 self.listenerThread = ''
	 self.isAlive = True
	 self.local = local
	 self.start()
	 return
    def DCCinterpreter(self):
         return
    def getConnectedUsers(self):
         userList = []
         for DCCCon in self.ircObject.DCC_Connections:
	      userList.append(DCCCon.client)
	 return userList
    def readSocket(self):
	 self.ircObject.logger.log(1, 'DCC', u'Conexión establecida con %s@%s.' % (self.client, self.ircObject.int2HumanIP(self.ip)))
         self.startMessage()
         while self.isAlive:
	      try:
	           char = self.secondSocket.recv(1)
	      except socket.timeout:
		   self.ircObject.logger.log(1, 'DCC', u'Conexión cerrada con %s@%s por \"timeout\".' % (self.client, self.ircObject.int2HumanIP(self.ip)))
	           self.isAlive = False
	      if not char:
		   self.ircObject.logger.log(1, 'DCC', u'Conexión cerrada con %s@%s por el par.' % (self.client, self.ircObject.int2HumanIP(self.ip)))
	           self.isAlive = False
	      else:   
	           if char == '\n':
		        self.ircObject.logger.log(1, 'DCC', '<%s> %s' % (self.client, self.line))
	                self.DCCinterpreter()
	                self.line = u''
	           elif not char == '\r':
	                self.line += unicode(char, 'iso-8859-1')
	 return
    def start(self):
         if self.local:
              self.firstSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	      self.firstSocket.settimeout(60.0)
	      try:
	           self.firstSocket.bind(('', self.port))
	      except:
	           self.isAlive = False
	           self.client = 'ERROR.BINDING.SOCKET'
	           self.ircObject.logger.log(0, 'DEBUG', u'[DCC]: Error manipulando el socket %i' % self.port)
	           return False
	      self.firstSocket.listen(1)
	      self.threadAccept()
	 else:
	      parms = True
	      if self.port < 1024 or self.port > 65535:
	           self.ircObject.logger.log(0, 'DEBUG', u'[DCC]: Error en el puerto')
	           parms = False
              if int(self.ip) < 0 or int(self.ip) > 4294967296:
	           self.ircObject.logger.log(0, 'DEBUG', u'[DCC]: Error en la IP')
	           parms = False
	      if parms:
	           self.threadConnect()
	      else:
	           self.isAlive = False
		   self.client = 'ERROR.DCC.PARAMETERS'
	           self.ircObject.logger.log(0, 'DEBUG', u'Parámetros del DCC Chat ofrecidos incorrectos (IP: %s / Puerto: %s)' % (self.ircObject.int2HumanIP(self.ip), self.port))
		   return False
	 return True
    def startMessage(self):
         return
    def threadAccept(self):
         listenerThread = threading.Timer(0.0, self.waitAccept)
	 listenerThread.setName('DCC_Connection_%s-accept-Thread' % self.client)
	 listenerThread.setDaemon(True)
	 listenerThread.start()
         return
    def threadConnect(self):
         listenerThread = threading.Timer(0.0, self.tryConnect)
	 listenerThread.setName('DCC_Connection_%s-connect-Thread' % self.client)
	 listenerThread.setDaemon(True)
	 listenerThread.start()
	 return
    def threadListener(self):
         listenerThread = threading.Timer(0.0, self.readSocket)
	 listenerThread.setName('DCC_Connection_%s-listener-Thread' % self.client)
	 listenerThread.setDaemon(True)
	 listenerThread.start()
	 return listenerThread
    def tryConnect(self):
	 self.secondSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	 self.secondSocket.settimeout(300.0)
	 try:
	      self.secondSocket.connect((self.ip, int(self.port)))
	 except socket.error:
	      self.isAlive = False
	      self.client = 'ERROR.CONNECTING.SOCKET'
	      self.ircObject.logger.log(0, 'DEBUG', u'[DCC]: Error conectándose a %s:%i' % (self.ircObject.int2HumanIP(self.ip), self.port))
	      return False
	 self.listenerThread = self.threadListener()
         return True
    def waitAccept(self):
         try:
              self.secondSocket, ipTuple = self.firstSocket.accept()
	 except socket.timeout:
	      self.isAlive = False
	      self.ircObject.logger.log(0, 'DEBUG', u'Timeout esperando la conexión DCC de %s.' % self.client)
	      self.client = 'ERROR.ACCEPT.SOCKET'
	      return False
	 ip, port = ipTuple
	 self.ip = self.ircObject.humanIP2int(ip)
	 self.listenerThread = self.threadListener()
	 self.firstSocket.close()
	 self.secondSocket.settimeout(300.0)
	 return
    def write(self, message):
         self.ircObject.logger.log(2, 'DCC', u'(%s) <%s> %s' % (self.client, self.ircObject.nickname, message))
         try:
	      self.secondSocket.send((u'%s\n' % message).encode('iso-8859-1'))
	 except:
	      self.ircObject.logger.log(0, 'DEBUG', u'Error escribiendo en el socket de %s (%s).' % (self.client, message))
	      return False
         return True

# ircConnection : superclase de los diferentes bots
class ircConnection:
    # Constructor de la clase
    def __init__(self, configFile):
         self.sock = ''
         self.recvThread = ''
         self.line = u''
	 self.exit = False
	 self.moduleList = { }
	 self.DCC_Connections = [ ]
	 self.configFile = configFile
         self.configuration = ConfigParser.ConfigParser()
	 self.configuration.read(self.configFile)
	 self.threadConfig()
	 self.threadChkDCCs()
	 self.DCC_ports = re.split(',', self.configuration.get('irc', 'dcc_ports'))
	 self.ownIP = ''
	 self.logger = logs.logger(self.configuration.get('logs', 'loglevel'), self.configuration.get('logs', 'coding'), self.configuration.get('logs', 'channel'), \
	                                                  self.configuration.get('logs', 'dcc'), self.configuration.get('logs', 'debug'), \
							  self.configuration.get('logs', 'irc'), self.configuration.get('logs', 'private'))
	 self.server = self.configuration.get('irc', 'server')
	 self.port = self.configuration.get('irc', 'port')
	 self.nickname = self.configuration.get('irc', 'nickname').lower()
	 self.__password__ = self.configuration.get('irc', 'password')
	 self.ident = self.configuration.get('irc', 'ident')
	 self.realname = self.configuration.get('irc', 'realname')
	 self.modes = self.configuration.get('irc', 'modes')
	 self.db = xmlDB.dbXML(self.configuration.get('database', 'user'), self.configuration.get('database', 'akick'), self.configuration.get('database', 'service'), self.configuration.get('database', 'spam'))
	 self.channels = re.split(',', self.configuration.get('irc', 'channels'))
	 for section in self.configuration.sections():
	      if self.configuration.has_option(section, 'enable') and self.configuration.getboolean(section, 'enable'):
	           self.loadModule(section)
	 return

    # Métodos disponibles
    #---------------------
    # readConfig: lee el fichero e configuración del bot cada 5 minutos
    def readConfig(self, sleep=True):
         while True:
	      self.configuration.read(self.configFile)
	      if sleep:
	           time.sleep(300)
	      else:
	           return True
	 return False
    # threadConfig: crea un thread que se encargará de ir releyendo la configuración del bot
    def threadConfig(self):
         configThread = threading.Timer(0.0, self.readConfig)
	 configThread.setName('readConfig-Thread')
	 configThread.setDaemon(True)
	 configThread.start()
	 return
    # threadChkDCCs: comprueba si las conexiones DCC están vivas
    def threadChkDCCs(self):
         configThread = threading.Timer(0.0, self.chkDCCs)
	 configThread.setName('chkDCCs-Thread')
	 configThread.setDaemon(True)
	 configThread.start()
	 return
    # getPassword: devuelve la variable interna __password__
    def getPassword(self):
         return self.__password__
    # setPassword: fija el valor de la variable interna __password__
    def setPassword(self, passwd):
         self.__password__ = passwd
	 return
    # chkDCCs: comprueba en la lista de DCCs si están vivos y los cierra si están muertos
    def chkDCCs(self):
         while True:
              tmpList = self.DCC_Connections
              for DCC_conn in self.DCC_Connections:
	           if not DCC_conn.isAlive:
		        if DCC_conn.client not in ['ERROR.BINDING.SOCKET', 'ERROR.ACCEPT.SOCKET', 'ERROR.DCC.PARAMETERS']:
			     DCC_conn.secondSocket.close()
	                tmpList.remove(DCC_conn)
	      self.DCC_Connections = tmpList
	      time.sleep(10)
	 return
    # connect: se conecta a un servidor de IRC y obtiene el objeto socket
    def connect(self):
         self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	 self.sock.settimeout(300.0)
	 while True:
	      try:
	           self.sock.connect((self.server, int(self.port)))
	      except:
	           time.sleep(60)
	      else:
	           return True
         return
    # recvData: recibe datos del servidor de IRC
    def recvData(self):
         while True:
	      try:
	           char = self.sock.recv(1)
	      except socket.timeout:
	           self.connect()
	      if not char:
	           if not self.exit:
	                self.connect()
		   else:
		        return True
	      else:   
	           if char == '\n':
		        self.logger.parseIrcData(self.line)
	                self.interpreter()
	                self.line = u''
	           elif not char == '\r':
	                self.line += unicode(char, 'iso-8859-1')
         return True
    # sendData: envía datos al servidor de IRC
    def sendData(self, data):
         try:
	      self.sock.send((u'%s\n' % data).encode('iso-8859-1'))
	 except:
	      return False
         return True
    # start: Inicia el funcionamiento del bot
    def start(self):
         self.connect()
	 self.recvThread = threading.Timer(0.0, self.recvData)
	 self.recvThread.setName('%s-Thread' % self.nickname)
	 self.recvThread.start()
         return True
    # interpreter: será sobrecargado en las subclases para hacer diferentes bots
    def interpreter(self):
         return
    # loadModule: carga en la lista de modulos un nuevo objeto modular que posteriormente usará el bot
    def loadModule(self, moduleName):
	 try:
              if moduleName == 'nospam':
		   import nospam
		   modObject = nospam.nospam(self)
	      elif moduleName == 'noflood':
		   import noflood
		   modObject = noflood.noflood(self)
	      elif moduleName == 'address':
	           import address
		   modObject = address.address(self)
	      elif moduleName == 'akick':
	           import akick
		   modObject = akick.akick(self)
	      elif moduleName == 'nobots':
	           import nobots
		   modObject = nobots.nobots(self)
	      elif moduleName == 'noinsult':
	           import noinsult
		   modObject = noinsult.noinsult(self)
	      else:
		   self.logger.log(0, 'DEBUG', u'[Función loadModule]: El módulo %s no existe.' % moduleName)
		   return False
	 except ImportError:
	      return False
	 self.moduleList[moduleName] = modObject
	 return True
    # unloadModule: descarga de la lista de módulos un objeto modular
    def unloadModule(self, moduleName):
         if self.moduleList.has_key(moduleName):
	      del self.moduleList[moduleName]
	      return True
	 return False
    # isLoaded: devuelve True si un módulo está cargado, de lo contrario devuelve false
    def isLoaded(self, moduleName):
         if self.moduleList.has_key(moduleName):
	      return True
         return False
    # version: devuelve el nombre y version del módulo
    def version(self):
	 return u'%s %s (%s)' % (__module_name__, __module_version__, __module_date__)
    # humanIP2int: transforma una IPv4 en formato "humano" (los 4 octetos) a su nomenclatura en formato entero
    def humanIP2int(self, ipAddr=''):
         if ipAddr == '':
	      octects = re.split('\.', self.ownIP)
	 else:
	      octects = re.split('\.', ipAddr)
         bits = [ ]
         integer = 0
         for octect in octects:
              binOct = []
              dividendo = int(octect)
              resto = 0
              while dividendo > 1:
                   resto = dividendo%2
                   dividendo = dividendo/2
                   binOct.append(resto)
              binOct.append(1)
              pos = 7
              while pos >= 0:
                   if (len(binOct)-1) < pos:
                        bits.append(0)
                   else:
                        bits.append(binOct[pos])
                   pos -= 1
         pos = 0
         while pos <= 31:
              integer += bits[pos]*pow(2,31-pos)
              pos += 1
         return integer
    # int2HumanIP: transforma un número entero en una dirección IPv4 visible de manera "humana"
    def int2HumanIP(self, integer):
         IP = []
	 bits = []
	 dividendo = int(integer)
         while dividendo > 1:
              resto = dividendo%2
	      dividendo = dividendo/2
	      bits.insert(0,resto)
	 bits.insert(0,1)
	 while len(bits) < 32:
	      bits.insert(0,0)
	 powValue = 7
	 octect = 0
	 for bit in bits:
	      octect += bit*pow(2,powValue)
	      powValue -= 1
	      if powValue < 0:
	           IP.append(str(octect))
	           powValue = 7
		   octect = 0
         return '.'.join(IP)
    # hasDCCConnection: Devuelve True si el usuario ya tiene abierta una conexión DCC, False en otro caso
    def hasDCCConnection(self, nick):
         for DCCconn in self.DCC_Connections:
	      if DCCconn.client.lower() == nick.lower():
	           return True
         return False
    # getDCCPort: Devuelve un puerto libre para la conexión DCC
    def getDCCPort(self):
         for port in self.DCC_ports:
	      free = True
	      for DCCconn in self.DCC_Connections:
	           if DCCconn.port == int(port):
		        free = False
	      if free:
	           return port
	 return False
    # consoleMessage: Manda un mensaje a los usuarios conectados por consola
    def consoleMessage(self, message):
         for DCCconn in self.DCC_Connections:
	      DCCconn.write(message)
         return

    # Órdenes del IRC
    #~~~~~~~~~~~~~~~~~
    # away: pone o saca del estado de away
    def away(self, state, reason=''):
         if state:
	      if reason == '':
	           reason = 'away'
	      self.logger.log(3, 'IRC', u'%s -> AWAY %s' % (self.nickname, reason))
	      return self.sendData('AWAY %s' % reason)
	 else:
	      self.logger.log(3, 'IRC', u'%s -> AWAY' % self.nickname)
	      return self.sendData('AWAY')
    # cmode: cambia un modo de un canal
    def cmode(self, channel, modes, args=''):
         self.logger.log(3, 'IRC', u'%s -> MODE %s %s %s' % (self.nickname, channel, modes, args))
         return self.sendData('MODE %s %s %s' % (channel, modes, args))
    # ctcp: envía un CTCP a un objetivo
    def ctcp(self, target, message):
         if re.search('^#.*', target) != None:
	      self.logger.log(1, 'CHANNEL', u'$%s@localhost$ %s' % (self.nickname, message))
	 else:
	      self.logger.log(2, 'PRIVATE', u'(%s) $%s$ %s' % (target, self.nickname, message))
         return self.sendData('PRIVMSG %s :%s%s%s' % (target, CTCP, message, CTCP))
    # ctcpreply: envía una respuesta CTCP a un objetivo
    def ctcpreply(self, target, message):
         if re.search('^#.*', target) != None:
	      self.logger.log(1, 'CHANNEL', u'$R$%s@localhost$ %s' % (self.nickname, message))
	 else:
	      self.logger.log(2, 'PRIVATE', u'(%s) $R$%s$ %s' % (target, self.nickname, message))
         return self.sendData('NOTICE %s :%s%s%s' % (target, CTCP, message, CTCP))
    # ghost: desconecta un nick registrado en el servidor
    def ghost(self, nick, password):
         self.logger.log(3, 'IRC', u'%s -> GHOST %s %s' % (self.nickname, nick, password))
         return self.sendData('GHOST %s %s' % (nick, password))
    # invite: invita a un nick a un canal
    def invite(self, channel, nick):
         self.logger.log(3, 'IRC', u'%s -> INVITE %s %s' % (self.nickname, nick, channel))
         return self.sendData('INVITE %s %s' % (nick, channel))
    # join: entra en un canal
    def join(self, channel, password=''):
         self.logger.log(3, 'IRC', u'%s -> JOIN %s %s' % (self.nickname, channel, password))
         return self.sendData('JOIN %s %s' % (channel, password))
    # kick: 'patea' a un nick de un canal
    def kick(self, channel, target, reason=''):
         if reason == '':
	      reason = target
	 self.logger.log(3, 'IRC', u'%s -> KICK %s %s :%s' % (self.nickname, channel, target, reason))
	 return self.sendData('KICK %s %s :%s' % (channel, target, reason))
    # msg: manda un mensaje privado (privmsg)
    def msg(self, target, message):
         if re.search('^#.*', target) != None:
	      self.logger.log(1, 'CHANNEL', u'<%s@localhost> %s' % (self.nickname, message))
	 else:
	      self.logger.log(2, 'PRIVATE', u'(%s) <%s> %s' % (target, self.nickname, message))
         return self.sendData('PRIVMSG %s :%s' % (target, message))
    # names: obtiene los nicks en un canal
    def names(self, channel):
         self.logger.log(3, 'IRC', u'%s -> NAMES %s' % (self.nickname, channel))
         return self.sendData('NAMES %s' % channel)
    # nick: especifica el 'nickname' usado
    def nick(self, nick, password=''):
         self.logger.log(3, 'IRC', u'%s -> NICK %s! %s' % (self.nickname, nick, password))
         return self.sendData('NICK %s! %s' % (nick, password))
    # notice: manda un notice a un objetivo
    def notice(self, target, message):
         if re.search('^#.*', target) != None:
	      self.logger.log(1, 'CHANNEL', u'-%s@localhost- %s' % (self.nickname, message))
	 else:
	      self.logger.log(2, 'PRIVATE', u'(%s) -%s- %s' % (target, self.nickname, message))
         return self.sendData('NOTICE %s :%s' % (target, message))
    # onotice: manda un onotice a un canal
    def onotice(self, channel, message):
         self.logger.log(1, 'CHANNEL', u'(Ops: %s) -%s@localhost- %s' % (channel, self.nickname, message))
         return self.sendData('NOTICE @%s :%s' % (channel, message))
    # part: sale de un canal
    def part(self, channel, message=''):
         self.logger.log(3, 'IRC', u'%s -> PART %s :%s' % (self.nickname, channel, message))
         return self.sendData('PART %s :%s' % (channel, message))
    # pong: envía un PONG! al servidor para evitar caerse por 'ping timeout'
    def pong(self, id):
         self.logger.log(3, 'IRC', u'%s -> PONG %s' % (self.nickname, id))
         return self.sendData('PONG %s' % id)
    # quit: desconecta del servidor de IRC
    def quit(self, message=''):
         self.exit = True
	 self.logger.log(0, 'IRC', u'%s -> QUIT :%s' % (self.nickname, message))
         return self.sendData('QUIT :%s' % message)
    # silence: añade o quita un nick de la lista de ignorados en el servidor
    def silence(self, mask, add=True):
         if add:
	      self.logger.log(3, 'IRC', u'%s -> SILENCE +%s' % (self.nickname, mask))
	      return self.sendData('SILENCE +%s' % mask)
	 else:
	      self.logger.log(3, 'IRC', u'%s -> SILENCE -%s' % (self.nickname, mask))
	      return self.sendData('SILENCE -%s' % mask)
    # topic: cambia el topic de un canal
    def topic(self, channel, newTopic=''):
         self.logger.log(3, 'IRC', u'%s -> TOPIC %s %s' % (self.nickname, channel, newTopic))
         return self.sendData('TOPIC %s %s' % (channel, newTopic))
    # user: se envía en la conexión para definir el 'ident' y el 'realname'
    def user(self):
         self.logger.log(3, 'IRC', u'%s -> USER %s x x :%s' % (self.nickname, self.ident, self.realname))
         return self.sendData('USER %s x x :%s' % (self.ident, self.realname))
    # userhost: solicita los datos del host de un usuario
    def userhost(self, nickList):
         self.logger.log(3, 'IRC', u'%s -> USERHOST %s' % (self.nickname, nickList))
         return self.sendData('USERHOST %s' % nickList)
    # userip: solicita los datos de la IP de un usuario
    def userip(self, nickList):
         self.logger.log(3, 'IRC', u'%s -> USERIP %s' % (self.nickname, nickList))
         return self.sendData('USERIP %s' % nickList)
    # usermode: cambia los modos de un usuario
    def usermode(self, nick, modes):
         self.logger.log(3, 'IRC', u'%s -> MODE %s %s' % (self.nickname, nick, modes))
         return self.sendData('MODE %s %s' % (nick, modes))
    # watch: fija una lista de 'observación' en el IRC
    def watch(self, list):
         self.logger.log(3, 'IRC', u'%s -> WATCH %s' % (self.nickname, list))
         return self.sendData('WATCH %s' % list)
    # who: obtiene información sobre direcciones de IRC
    def who(self, mask, flags=''):
         self.logger.log(3, 'IRC', u'%s -> WHO %s %s' % (self.nickname, mask, flags))
         return self.sendData('WHO %s %s' % (mask, flags))
    # whois: obtiene información sobre un nick
    def whois(self, nick):
         self.logger.log(3, 'IRC', u'%s -> WHOIS %s %s' % (self.nickname, nick))
         return self.sendData('WHOIS %s %s' % nick)
    # whowas: obtiene información sobre un nick recientemente desconectado
    def whowas(self, nick):
         self.logger.log(3, 'IRC', u'%s -> WHOWAS %s %s' % (self.nickname, nick))
         return self.sendData('WHOWAS %s' % nick)
