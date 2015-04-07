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
    
__module_name__ = 'mod-akick'
__module_version__ = '0.4.2' 
__module_author__ = 'Manuel Lorenzo Frieiro'
__module_description__ = 'Módulo encargado de gestionar los akicks del bot.'
__module_date__ = '2007/04/01'

# Módulos necesarios
#====================

import re
import irc
import threading

# Variables Globales
#====================

# Clases
#========

class sN:
    def __init__(self, ident='', ipAddr=''):
         self.ident = ident
	 self.ipAddr = ipAddr
	 return
	 
class akick:
    shitNick = sN
    
    # Constructores de la clase:
    def __init__(self, botObject):
         self.botObj = botObject
	 self.shitList = { }
         return

    # Métodos
    # ========
    # delBan: Elimina el baneo impuesto anteriormente 
    def delBan(self, channel, host):
	 self.botObj.cmode(channel, '-b', u'*!*@%s' % host)
         return
    # interpreter: necesario para la comunicación del bot con el módulo
    def interpreter(self, textLine):
         if re.search('^:[^ ]+ 001', textLine) != None:
	      self.botObj.watch('+%s' % ' +'.join(self.botObj.db.getAkickNicks()))
	      return
	 elif re.search('^[^ ]+ JOIN', textLine) != None:
	      regExpElements = re.search('^:(?P<nick>[^ ]+)![^ ]+@(?P<host>[^ ]+) [^ ]+ :(?P<channel>[^ ]+)', textLine.lower())
	      if regExpElements.group('channel') in self.botObj.channels and self.botObj.db.isAkicked(regExpElements.group('nick')) and not self.botObj.db.isGod(regExpElements.group('nick'), regExpElements.group('host')):
		   self.botObj.cmode(regExpElements.group('channel'), '+b', u'*!*@%s' % regExpElements.group('host'))
		   self.botObj.kick(regExpElements.group('channel'), regExpElements.group('nick'), self.botObj.db.getAkickReason(regExpElements.group('nick')))
		   # Elimina el baneo después de 1 hora
		   unbanThread = threading.Timer(3600.0, self.delBan, [regExpElements.group('channel'), regExpElements.group('host')])
                   unbanThread.setName('akick_unban_%s-Thread' % regExpElements.group('host'))
                   unbanThread.setDaemon(True)
		   unbanThread.start()
	      elif regExpElements.group('channel') in self.botObj.channels:
	           for akicked in self.shitList.keys():
		        if regExpElements.group('host') == self.shitList[akicked].ipAddr:
			     self.botObj.onotice(regExpElements.group('channel'), u'%s%s%s es un clon de un \'akickeado\' (%s%s%s)' % (irc.BOLD, regExpElements.group('nick'), irc.BOLD, irc.BOLD, akicked, irc.BOLD))
	      return
	 elif re.search('^[^ ]+ NICK', textLine) != None:
	      regExpElements = re.search('^:(?P<nick>[^ ]+)![^ ]+@(?P<host>[^ ]+) [^ ]+ :(?P<newnick>.*)$', textLine.lower())
	      for channel in self.botObj.channels:
	           if self.botObj.isLoaded('address'):
			if self.botObj.moduleList['address'].isChanUser(channel, regExpElements.group('newnick')) and self.botObj.db.isAkicked(regExpElements.group('newnick')) and not self.botObj.db.isGod(regExpElements.group('nick'), regExpElements.group('host')):
		             self.botObj.cmode(channel, '+b', u'*!*@%s' % regExpElements.group('host'))
		             self.botObj.kick(channel, regExpElements.group('newnick'), self.botObj.db.getAkickReason(regExpElements.group('newnick')))
		             # Elimina el baneo después de 1 hora
		             unbanThread = threading.Timer(3600.0, self.delBan, [channel, regExpElements.group('host')])
                             unbanThread.setName('akick_unban_%s-Thread' % regExpElements.group('host'))
                             unbanThread.setDaemon(True)
		             unbanThread.start()
			     if self.botObj.configuration.getboolean('akick', 'dyn_akick'):
			          self.botObj.db.modAkicks('add', regExpElements.group('nick'), self.botObj.db.getAkickReason(regExpElements.group('newnick')))
		   else:
		        if self.botObj.db.isAkicked(regExpElements.group('newnick')) and not self.botObj.isGod(regExpElements.group('nick'), regExpElements.group('host')):
		             self.botObj.cmode(channel, '+b', u'*!*@%s' % regExpElements.group('host'))
		             self.botObj.kick(channel, regExpElements.group('newnick'), self.botObj.db.getAkickReason(regExpElements.group('newnick')))
		             # Elimina el baneo después de 1 hora
		             unbanThread = threading.Timer(3600.0, self.delBan, [channel, regExpElements.group('host')])
                             unbanThread.setName('akick_unban_%s-Thread' % regExpElements.group('host'))
                             unbanThread.setDaemon(True)
		             unbanThread.start()
			     if self.botObj.configuration.getboolean('akick', 'dyn_akick'):
			          self.botObj.db.modAkicks('add', regExpElements.group('nick'), self.botObj.db.getAkickReason(regExpElements.group('newnick')))
	      return
	 elif re.search('^[^ ]+ (600|604)', textLine) != None:
	      regExpElements = re.search('^:[^ ]+ [^ ]+ [^ ]+ (?P<nick>[^ ]+) (?P<ident>[^ ]+) (?P<ip>[^ ]+)', textLine.lower())
	      self.shitList[regExpElements.group('nick')] = self.shitNick(regExpElements.group('ident'), regExpElements.group('ip'))
	      for channel in self.botObj.channels:
	           self.botObj.onotice(channel, u'%s%s%s (%s@%s) está en el IRC y está en el %sakick%s. Ojos bien abiertos por si entra O_O.' % (irc.BOLD, regExpElements.group('nick'), irc.BOLD, regExpElements.group('ident'), regExpElements.group('ip'), irc.BOLD, irc.BOLD))
		   if self.botObj.isLoaded('address'):
		        cloneList = self.botObj.moduleList['address'].clones(channel, regExpElements.group('ip'))
			if len(cloneList) > 0:
			     self.botObj.onotice(channel, u'%s%sClones conocidos en %s%s:%s %s' % (irc.BOLD, irc.UNDERLINE, channel, irc.UNDERLINE, irc.BOLD, ' '.join(cloneList)))
	      return
	 elif re.search('^[^ ]+ 601', textLine) != None:
	      regExpElements = re.search('^:[^ ]+ [^ ]+ [^ ]+ (?P<nick>[^ ]+)', textLine.lower())
	      del self.shitList[regExpElements.group('nick')]
	      return
	 elif re.search('^[^ ]+ 353', textLine) != None:
	      regExpElements = re.search('(=|@) (?P<channel>#[^ ]+) :(?P<nickList>.*) $', textLine.lower())
	      if regExpElements != None:
	           channel, nickList = regExpElements.group('channel'), regExpElements.group('nickList')
	           for nick in re.split(' ', nickList):
	                nickname = re.search('(?P<nickname>[^\+@]+)$', nick).group('nickname')
		        if self.botObj.db.isAkicked(nickname):
		             self.botObj.cmode(regExpElements.group('channel'), '+b', nickname)
			     self.botObj.kick(regExpElements.group('channel'), nickname, self.botObj.db.getAkickReason(nickname))
	      return
	 return

    # version: devuelve el nombre y version del módulo
    def version(self):
	 return u'%s %s (%s)' % (__module_name__, __module_version__, __module_date__)
