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
    
__module_name__ = 'mod-addr'
__module_version__ = '0.2.1'
__module_date__ = '2007/03/11'
__module_author__ = 'Manuel Lorenzo Frieiro'
__module_description__ = 'Este módulo se encarga de mantener las listas usuarios de los canales en los que está el bot. Almacena los ops, direcciones IP, etc.'

# Módulos necesarios
#====================

import re

# Variables Globales
#====================

# Clases
#========

class nickname:
    # constructor de la clase:
    def __init__(self, ipAddr='', ident='', op=False, voice=False):
         self.ipAddr = ipAddr
	 self.ident = ident
	 self.op = op
	 self.voice = voice
	 return

class address:
    n = nickname
    
    # Constructores de la clase:
    def __init__(self, botObject):
         self.chanUsers = { }
         self.botObj = botObject
	 for channel in self.botObj.channels:
	      self.chanUsers[channel] = {}
         return

    # Métodos

    # interpreter: necesario para la comunicación del bot con el módulo
    def interpreter(self, textLine):
         if re.search('^[^ ]+ JOIN', textLine) != None:
	      regExpElements = re.search('^:(?P<nick>[^ ]+)!(?P<ident>[^ ]+)@(?P<ip>[^ ]+).*:(?P<channel>.+)$', textLine.lower())
              nick, ident, host, channel = regExpElements.group('nick'), regExpElements.group('ident'), regExpElements.group('ip'), regExpElements.group('channel')
	      if channel not in self.botObj.channels:
	           return
	      if self.chanUsers[channel].has_key(nick):
	           del self.chanUsers[channel][nick]
	      self.chanUsers[channel][nick] = self.n(host, ident)
	 elif re.search('^[^ ]+ PART', textLine) != None:
	      regExpElements = re.search('^:(?P<nick>[^ ]+)![^ ]+@[^ ]+ [^ ]+ (?P<channel>[^ ]+).*$', textLine.lower())
	      nick, channel = regExpElements.group('nick'), regExpElements.group('channel')
	      if channel not in self.botObj.channels:
	           return
	      if self.chanUsers[channel].has_key(nick):
	           del self.chanUsers[channel][nick]
	 elif re.search('^[^ ]+ QUIT', textLine) != None:
              regExpElements = re.search('^:(?P<nick>[^ ]+)![^ ]+@[^ ]+ .*$', textLine.lower())
	      nick = regExpElements.group('nick')
	      for channel in self.botObj.channels:
	           if self.chanUsers[channel].has_key(nick):
		        del self.chanUsers[channel][nick]
	 elif re.search('^[^ ]+ KICK', textLine) != None:
	      regExpElements = re.search('^:[^ ]+ [^ ]+ (?P<channel>[^ ]+) (?P<nick>[^ ]+).*$', textLine.lower())
	      nick, channel = regExpElements.group('nick'), regExpElements.group('channel')
	      if channel not in self.botObj.channels:
	           return
	      if self.chanUsers[channel].has_key(nick):
	           del self.chanUsers[channel][nick]
	 elif re.search('^[^ ]+ NICK', textLine) != None:
	      regExpElements = re.search('^:(?P<nick>[^ ]+)![^ ]+@[^ ]+.*:(?P<newnick>.*)$', textLine.lower())
	      nick, newnick = regExpElements.group('nick'), regExpElements.group('newnick')
	      for channel in self.botObj.channels:
	           if self.chanUsers[channel].has_key(nick):
		        del self.chanUsers[channel][nick]
	                self.chanUsers[channel][newnick] = self.n()
	      self.botObj.userhost(newnick)
         elif re.search('^[^ ]+ MODE #', textLine) != None:
	      regExpElements = re.search('^:[^ ]+ [^ ]+ (?P<channel>[^ ]+) (?P<modes>[^ ]+) *(?P<targets>.*$)', textLine.lower())
	      channel, modes, targets = regExpElements.group('channel'), regExpElements.group('modes'), regExpElements.group('targets')
	      if channel not in self.botObj.channels:
	           return
	      modeList = []
	      plus = ''
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
	           if self.chanUsers[channel].has_key(target):
		        if mode == '+o':
			     self.chanUsers[channel][target].op = True
			elif mode == '-o':
			     self.chanUsers[channel][target].op = False
			elif mode == '+v':
			     self.chanUsers[channel][target].voice = True
			elif mode == '-v':
			     self.chanUsers[channel][target].voice = False
	 elif re.search('^[^ ]+ 302', textLine) != None:
	      regExpElements = re.search(':(?P<nick>[^ ]+)=.(?P<ident>[^ ]+)@(?P<ip>[^ ]+)$', textLine.lower())
	      if regExpElements != None:
	           nick, ident, host = regExpElements.group('nick'), regExpElements.group('ident'), regExpElements.group('ip')
	           for channel in self.botObj.channels:
	                if self.chanUsers[channel].has_key(nick):
		             self.chanUsers[channel][nick].ipAddr = host
			     self.chanUsers[channel][nick].ident = ident
	 elif re.search('^[^ ]+ 353', textLine) != None:
	      regExpElements = re.search('(=|@) (?P<channel>#[^ ]+) :(?P<nickList>.*) $', textLine.lower())
	      if regExpElements != None:
	           channel, nickList = regExpElements.group('channel'), regExpElements.group('nickList')
	           if channel not in self.botObj.channels:
	                return
	           for nick in re.split(' ', nickList):
	                op, voice = False, False
	                nickname = re.search('(?P<nickname>[^\+@]+)$', nick).group('nickname')
		        if '@' in nick:
		             op = True
		        if '+' in nick:
		             voice = True
		        self.chanUsers[channel][nickname] = self.n('', '', op, voice)
	 return

    # isOp: devuelve True si el nick tiene op en el canal, False si no la tiene
    def isOp(self, channel, nickname):
         if self.chanUsers[channel].has_key(nickname.lower()):
	      return self.chanUsers[channel][nickname].op
	 return False

    # isVoice: devuelve True si el nick tiene voz en el canal, False si no la tiene
    def isVoice(self, channel, nickname):
         if self.chanUsers[channel].has_key(nickname.lower()):
	      return self.chanUsers[channel][nickname].voice
	 return False

    # clones: devuelve los clones de un nick especificado en el canal
    def clones(self, channel, host):
         cloneList = []
	 for nick in self.chanUsers[channel].keys():
	      if self.chanUsers[channel][nick].ipAddr == host:
		   cloneList.append(nick)
	 return cloneList

    # isChanUser: devuelve True si el nick está en la lista de nicks del canal
    def isChanUser(self, channel, nickname):
	 return self.chanUsers[channel].has_key(nickname.lower())

    # version: devuelve el nombre y version del módulo
    def version(self):
	 return u'%s %s (%s)' % (__module_name__, __module_version__, __module_date__)
