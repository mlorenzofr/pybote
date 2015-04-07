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

__module_name__ = 'botFerrolterra-pyBOTe'
__module_version__ = '0.4.5'
__module_date__ = '2007/03/26'
__module_author__ = 'Manuel Lorenzo Frieiro'
__module_description__ = 'Módulo principal del bot. Aquí se encuentran las órdenes básicas del bot.'

# Módulos necesarios
#====================

import irc
import re

# Variables Globales
#====================

# Clases
#========

class DCCObject(irc.DCCObject):
    # Saturación del método DCCinterpreter
    def DCCinterpreter(self):
	 messageWords = re.split(' ', self.line.lower())
	 if '' in messageWords:
	      messageWords.remove('')
         if len(messageWords) > 0:
	      if self.ircObject.db.hasPermission(self.client.lower(), messageWords[0]):
                   if messageWords[0] == 'join':
                        if len(messageWords) > 1:
			     if messageWords[1] not in self.ircObject.channels:
			          self.write(u'¿? %s ¿? Ahí no pinto nada ¬_¬ .' % messageWords[1])
			     else:
			          self.ircObject.join(messageWords[1])
                   elif messageWords[0] == 'msg':
                        if len(messageWords) > 2:
		             self.ircObject.msg(messageWords[1], ' '.join(messageWords[2:]))
                   elif messageWords[0] == 'onotice':
                        if len(messageWords) > 2:
			     self.ircObject.onotice(messageWords[1], ' '.join(messageWords[2:]))
                   elif messageWords[0] == 'kick':
                        if len(messageWords) > 3:
			     self.ircObject.kick(messageWords[1], messageWords[2], ' '.join(messageWords[3:]))
                   elif messageWords[0] == 'kickban':
                        if len(messageWords) > 3:
		             if self.ircObject.isLoaded('address') and self.ircObject.moduleList['address'].isChanUser(messageWords[1], messageWords[2]) and self.ircObject.moduleList['address'][messageWords[1]][messageWords[2]].ipAddr != '':
			          self.ircObject.cmode(messageWords[1], '+b', '*!*@%s' % self.ircObject.moduleList['address'][messageWords[1]][messageWords[2]].ipAddr)
			     else:     
			          self.ircObject.cmode(messageWords[1], '+b', '%s!*@*' % messageWords[2])
			     self.ircObject.kick(messageWords[1], messageWords[2], ' '.join(messageWords[3:]))
	           elif messageWords[0] == 'unban':
		        if len(messageWords) > 2:
			     self.ircObject.cmode(messageWords[1], '-b', '%s' % messageWords[2])
                   elif messageWords[0] == 'mode':
                        if len(messageWords) > 3:
			     self.ircObject.cmode(messageWords[1], messageWords[2], ' '.join(messageWords[3:]))
	           elif messageWords[0] == 'akick':
		        if len(messageWords) == 2:
			     if self.ircObject.db.modAkicks('add', messageWords[1]):
			          if re.search('^@.+', messageWords[1], re.I) != None:
			               self.write(u'%s%s%s ha sido añadido a la lista de AKICK.' % (irc.BOLD, messageWords[1][1:], irc.BOLD))
			          else:
			               self.write(u'%s%s%s ha sido añadido a la lista de AKICK.' % (irc.BOLD, messageWords[1], irc.BOLD))
				       self.ircObject.watch('+%s' % messageWords[1])
  	                elif len(messageWords) > 2:
		             if self.ircObject.db.modAkicks('add', messageWords[1], ' '.join(messageWords[2:])):
		                  if re.search('^@.+', messageWords[1], re.I) != None:
			               self.write(u'%s%s%s ha sido añadido a la lista de AKICK.' % (irc.BOLD, messageWords[1][1:], irc.BOLD))
			          else:
			               self.write(u'%s%s%s ha sido añadido a la lista de AKICK.' % (irc.BOLD, messageWords[1], irc.BOLD))
			               self.ircObject.watch('+%s' % messageWords[1])
	           elif messageWords[0] == 'user':
	                if len(messageWords) > 1:
		             if self.ircObject.db.modUsers('add', messageWords[1]):
			          self.write(u'%s%s%s ha sido dado de alta en el bot.' % (irc.BOLD, messageWords[1], irc.BOLD))
	           elif messageWords[0] == 'no':
	                if len(messageWords) > 2:
		             if messageWords[1] == 'akick':
			          if self.ircObject.db.modAkicks('del', messageWords[2]):
				       self.write(u'%s%s%s ha sido borrado de la lista de AKICK.' % (irc.BOLD, messageWords[2], irc.BOLD))
				       self.ircObject.watch('-%s' % messageWords[2])
			     elif messageWords[1] == 'user':
			          if self.ircObject.db.modUsers('del', messageWords[2]):
			               self.write(u'%s%s%s ha sido dado de baja en el bot.' % (irc.BOLD, messageWords[2], irc.BOLD))
		             if messageWords[1] == 'spam':
			          if self.ircObject.db.modSpammers('del', messageWords[2]):
				       self.write(u'%s%s%s ha sido borrado de la lista de SPAMMERS.' % (irc.BOLD, messageWords[2], irc.BOLD))
	           elif messageWords[0] == 'show':
		        if len(messageWords) > 1:
		             if messageWords[1] == 'akick':
			          i = 1
				  akicks = self.ircObject.db.getAkicks()
				  sortedKeyList = akicks.keys()
				  sortedKeyList.sort()
			          # for akicked, reason in self.ircObject.db.getAkicks().iteritems():
			          #     self.write(u'%i.- %s%s%s :: %s' % (i, irc.BOLD, akicked, irc.BOLD, reason))
				  #     i += 1
			          for akicked in sortedKeyList:
			               self.write(u'%i.- %s%s%s :: %s' % (i, irc.BOLD, akicked, irc.BOLD, akicks[akicked]))
				       i += 1
				  akicks = self.ircObject.db.getREAkicks()
				  sortedKeyList = akicks.keys()
				  sortedKeyList.sort()
			          for regexp in sortedKeyList:
				       self.write(u'%i.- (RegExp) %s%s%s :: %s' % (i, irc.BOLD, regexp, irc.BOLD, akicks[regexp]))
				       i += 1
		             if messageWords[1] == 'spam':
			          i = 1
				  spammers = self.ircObject.db.getSpammers()
				  sortedKeyList = spammers.keys()
				  sortedKeyList.sort()
			          # for nick, date in self.ircObject.db.getSpammers().iteritems():
			          #     self.write(u'%i.- (Nick) %s%s%s [%s]' % (i, irc.BOLD, nick, irc.BOLD, date))
				  #     i += 1
			          for nick in sortedKeyList:
			               self.write(u'%i.- (Nick) %s%s%s [%s]' % (i, irc.BOLD, nick, irc.BOLD, spammers[nick]))
				       i += 1
			          # for regexp, date in self.ircObject.db.getRESpammers().iteritems():
			          #     self.write(u'%i.- (RegExp) %s%s%s [%s]' % (i, irc.BOLD, regexp, irc.BOLD, date))
				  #     i += 1
				  spammers = self.ircObject.db.getRESpammers()
				  sortedKeyList = spammers.keys()
				  sortedKeyList.sort()
			          for regexp in sortedKeyList:
			               self.write(u'%i.- (RegExp) %s%s%s [%s]' % (i, irc.BOLD, regexp, irc.BOLD, spammers[regexp]))
				       i += 1
	           elif messageWords[0] == 'spam':
		        if len(messageWords) == 2:
			     if self.ircObject.db.modSpammers('add', messageWords[1]):
			          if re.search('^@.+', messageWords[1], re.I) != None:
			               self.write(u'%s%s%s ha sido añadido a la lista de SPAMMERS.' % (irc.BOLD, messageWords[1][1:], irc.BOLD))
			          else:
			               self.write(u'%s%s%s ha sido añadido a la lista de SPAMMERS.' % (irc.BOLD, messageWords[1], irc.BOLD))
	           elif messageWords[0] == 'load':
		        if len(messageWords) > 1:
			     if self.ircObject.loadModule(messageWords[1].lower()):
			          self.write(u'Módulo %s%s%s cargado correctamente.' % (irc.BOLD, messageWords[1], irc.BOLD))
	           elif messageWords[0] == 'quit':
		        if len(messageWords) > 1:
			     self.ircObject.quit(' '.join(messageWords[1:]))
		        else:
			     self.ircObject.quit('')
	           elif messageWords[0] == 'ctcp':
		        if len(messageWords) > 2:
			     self.ircObject.ctcp(messageWords[1], ' '.join(messageWords[2:]))
	           elif messageWords[0] == 'help':
	                self.write(u'Órdenes disponibles:')
		        self.write(u'%shelp%s: Muestra este mensaje de ayuda.' % (irc.BOLD, irc.BOLD))
		        self.write(u'%sjoin%s %s#canal%s: Mete el bot en el canal indicado.' % (irc.BOLD, irc.BOLD, irc.BLUE, irc.COLOR))
		        self.write(u'%smsg%s %snick o #canal%s %smensaje%s: Manda un mensaje a un nick o canal indicado.' % (irc.BOLD, irc.BOLD, irc.BLUE, irc.COLOR, irc.GREEN, irc.COLOR))
		        self.write(u'%sonotice%s %s#canal%s %smensaje%s: Manda un onotice al canal indicado.' % (irc.BOLD, irc.BOLD, irc.BLUE, irc.COLOR, irc.GREEN, irc.COLOR))
		        self.write(u'%skick%s %s#canal%s %snick%s %smotivo%s: Expulsa a un nick del canal con el motivo indicado.' % (irc.BOLD, irc.BOLD, irc.BLUE, irc.COLOR, irc.RED, irc.COLOR, irc.GREEN, irc.COLOR))
		        self.write(u'%skickban%s %s#canal%s %snick%s %smotivo%s: Expulsa y banea a un nick del canal con el motivo indicado.' % (irc.BOLD, irc.BOLD, irc.BLUE, irc.COLOR, irc.RED, irc.COLOR, irc.GREEN, irc.COLOR))
		        self.write(u'%sunban%s %s#canal%s %smáscara%s: Elimina el baneo en el canal indicado.' % (irc.BOLD, irc.BOLD, irc.BLUE, irc.COLOR, irc.GREEN, irc.COLOR))
		        self.write(u'%smode%s %s#canal%s %s[+|-]modo%s: Pone un modo en el canal indicado.' % (irc.BOLD, irc.BOLD, irc.BLUE, irc.COLOR, irc.GREEN, irc.COLOR))
		        self.write(u'%sakick%s %snick o @Expresion_regular%s %smotivo%s: Pone un akick en el canal del bot al nick o al patrón con expresiones regulares facilitado.' % (irc.BOLD, irc.BOLD, irc.BLUE, irc.COLOR, irc.GREEN, irc.COLOR))
		        self.write(u'%sno akick%s %snick o @Expresion_regular%s: Borra el akick especificado.' % (irc.BOLD, irc.BOLD, irc.BLUE, irc.COLOR))
		        self.write(u'%sno spam%s %snick o @Expresion_regular%s: Borra el nick o expresión regular indicado de la lista de spammers.' % (irc.BOLD, irc.BOLD, irc.BLUE, irc.COLOR))
		        self.write(u'%sshow akick%s: Muestra la lista de akicks.' % (irc.BOLD, irc.BOLD))
		        self.write(u'%sshow spam%s: Muestra la lista de spammers.' % (irc.BOLD, irc.BOLD))
		        self.write(u'%sspam%s %snick o @Expresion_regular%s: Añade un nick o expresión regular a la lista de spammers que serán expulsados de los canales.' % (irc.BOLD, irc.BOLD, irc.BLUE, irc.COLOR))
	           elif messageWords[0] == 'reload':
		        if self.ircObject.readConfig(False):
		             self.write(u'Configuración de %s%s%s recargada.' % (irc.BOLD, self.ircObject.configFile, irc.BOLD))
         return
    # Saturación del método startMessage
    def startMessage(self):
         self.write(u'Te leo %s.' % self.client)
	 users = self.getConnectedUsers()
	 self.write(u'Conectados al bot: %s' % ', '.join(users))
	 self.write(u'Escribe %shelp%s si necesitas ayuda.' % (irc.BOLD, irc.BOLD))
         return

class botFerrolterra(irc.ircConnection):
    # Saturación del método interpreter
    def interpreter(self):
         if re.search('^PING :', self.line) != None:
	      self.pong(re.search(':(?P<pong>.*)$', self.line).group('pong'))
	 elif re.search('^:[^ ]+ NOTICE IP_LOOKUP', self.line) != None:
	      self.user()
	      self.nick(self.nickname, self.getPassword())
	 elif re.search('^:[^ ]+ 001', self.line) != None:
	      self.usermode(self.nickname, self.modes)
	      self.userip(self.nickname)
              for channel in self.channels:
		   self.join(channel)
	 elif re.search('^:[^ ]+ 340', self.line) != None:
	      self.ownIP = re.search(':.*@(?P<ip>.*)$', self.line).group('ip')
	 elif re.search('^:[^ ]+ 474', self.line) != None:
	      regExpElements = re.search('^:[^ ]+ [^ ]+ [^ ]+ (?P<channel>[^ ]+)', self.line)
	      if regExpElements != None and regExpElements.group('channel').lower() in self.channels:
	           self.msg('CHaN@deep.space', 'invite %s' % regExpElements.group('channel'))
	 elif re.search('^:[^ ]+ KICK', self.line) != None:
	      regExpElements = re.search('^:[^ ]+ [^ ]+ (?P<channel>[^ ]+) (?P<nick>[^ ]+).*$', self.line)
	      if regExpElements.group('nick') == self.nickname.lower() and self.configuration.getboolean('irc', 'rejoin_on_kick'):
		   self.join(regExpElements.group('channel'))
	 elif re.search('^:[^ ]+ INVITE', self.line) != None:
	      regExpElements = re.search('^:CHaN!-@- INVITE [^ ]+ :(?P<channel>#[^ ]+)$', self.line, re.I)
	      if regExpElements != None:
	           self.join(regExpElements.group('channel'))
	 elif re.search('^[^ ]+ MODE #', self.line) != None:
	      regExpElements = re.search('^:[^ ]+ [^ ]+ (?P<channel>[^ ]+) (?P<modes>[^ ]+) *(?P<targets>.*$)', self.line.lower())
	      channel, modes, targets = regExpElements.group('channel'), regExpElements.group('modes'), regExpElements.group('targets')
	      if self.nickname in targets and channel in self.channels and self.configuration.getboolean('irc', 'op_protection'):
	           modeList = []
		   plus = ''
		   callOp = False
		   for pos in range(0, len(modes)):
		        if modes[pos] == '+':
			     plus = '+'
			elif modes[pos] == '-':
			     plus = '-'
			elif modes[pos] == 'o':
			     modeList.append('%so' % plus)
			elif modes[pos] == 'v':
			     modeList.append('%sv' % plus)
	           for target, mode in zip(re.split(' ', targets), modeList):
		        if mode == '-o' and target == self.nickname:
			     callOp = True
		        if mode == '+o' and target == self.nickname:
			     callOp = False
                   if callOp:
			     self.msg('chan', 'op %s %s' % (channel, self.nickname))
	 elif re.search('^:[^ ]+ (PRIVMSG|NOTICE)', self.line):
	      regExpElements = re.search('^:(?P<sender>[^ ]+)!(?P<ident>[^ ]+)@(?P<ip>[^ ]+) [^ ]+ (?P<target>[^ ]+) :(?P<message>.*)$', self.line.lower())
	      if regExpElements != None:
	           nick, ident, host = regExpElements.group('sender'), regExpElements.group('ident'), regExpElements.group('ip')
	           if regExpElements.group('target') == self.nickname.lower():
			if re.search('^%s.*VERSION.*%s$' % (irc.CTCP, irc.CTCP), regExpElements.group('message'), re.I) != None and self.db.hasPermission(nick.lower(), 'version'):
			     version = 'VERSION %s %s' % (__module_name__, __module_version__)
			     for mod in self.moduleList:
			          version += ' + %s' % self.moduleList[mod].version()
			     self.ctcpreply(nick, version)
			else:
			     self.consoleMessage('%s<%s!%s@%s> %s%s' % (irc.REVERSE, nick, ident, host, regExpElements.group('message'), irc.REVERSE))
			     checkChat = re.search('^%s.*DCC CHAT chat (?P<ip>[^ ]+) (?P<port>[^ ]+).*%s$' % (irc.CTCP, irc.CTCP), regExpElements.group('message'), re.I)
                             if self.db.hasPermission(nick.lower(), 'console'):
			          if not self.hasDCCConnection(nick):
			               if checkChat != None:
				            self.DCC_Connections.append(DCCObject(nick, int(checkChat.group('port')), self, False, checkChat.group('ip')))
				       else:
				            DCCPort = self.getDCCPort()
				            if not DCCPort:
				                 self.msg(nick, 'No quedan conexiones al bot disponibles en este momento.')
				                 self.msg(nick, 'Espera 10 minutos y prueba de nuevo.')
				            else:
			                         self.DCC_Connections.append(DCCObject(nick, DCCPort, self))
				                 self.ctcp(nick, 'DCC CHAT chat %s %s' % (self.humanIP2int(), DCCPort))
         for module in self.moduleList:
	      self.moduleList[module].interpreter(self.line)
         return
    # version: devuelve el nombre y version del módulo
    def version(self):
         return u'%s %s (%s)' % (__module_name__, __module_version__, __module_date__)
