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
    
__module_name__ = 'mod-noBots'
__module_version__ = '0.3.1'
__module_date__ = '2007/04/01'
__module_author__ = 'Manuel Lorenzo Frieiro'
__module_description__ = 'Módulo para detectar los bots que entran en los canales.'

# Módulos necesarios
#====================

import re
import irc
import time
import threading
import random

# Variables Globales
#====================

# Clases
#========

class nobots:
    # Variables locales
    kickList = [u'Spam',
    u'Inserte aquí su publicidad.',
    u'Busca otra vía para publicitarte. >:@',
    u'Oh my god another computer hacked !!!',
    u'La publicidad se paga, cada día más cara.',
    u'Nuestra sección de anuncios por palabras aún está en construcción.',
    u'Si los bots pudiesen volar esto se convertiría en un aeropuerto.',
    u'Ahora los bots actúan (pateando, no metiendo la mano en el bolsillo a los ciudadanos).',
    u'Yo soy un bot, 2 añitos, torre exuberante, muy calentito. Si te interesa privado.',
    u'Di NO a la publicidad.',
    u'Te pillé ;) (bot)']
    # Constructores de la clase:
    def __init__(self, botObject):
         self.botObj = botObject
	 self.dictKicked = { }
         return
    # Métodos
    # ========
    # delBan: Elimina el baneo impuesto a un bot
    def delBan(self, channel, host):
         self.botObj.cmode(channel, '-b', u'*!*@%s' % host)
         return
    # interpreter: necesario para la comunicación del bot con el módulo
    def interpreter(self, textLine):
         if re.search('^:[^ ]+ JOIN', textLine) != None:
	      regExpElements = re.search('^:(?P<nick>[^ ]+)!(?P<ident>[^ ]+)@(?P<ip>[^ ]+).*:(?P<channel>.+)$', textLine)
	      nick, ident, host = regExpElements.group('nick'), regExpElements.group('ident'), regExpElements.group('ip')
	      for kicked in self.dictKicked.keys():
	           if (time.time() - self.dictKicked[kicked]) > 86400:
		        del self.dictKicked[kicked]
	      if regExpElements.group('channel').lower() in self.botObj.channels and nick.lower() != self.botObj.nickname.lower() and not self.botObj.db.isGod(regExpElements.group('nick'), regExpElements.group('ip')):
	           if self.botObj.db.isSpammer(nick) or self.botObj.db.isSpammer(ident):
		        self.botObj.cmode(regExpElements.group('channel'), '+b', u'*!*@%s' % host)
			self.botObj.kick(regExpElements.group('channel'), nick, random.choice(self.kickList))
			# Elimina el baneo después de 1 hora
			unbanThread = threading.Timer(3600.0, self.delBan, [regExpElements.group('channel'), host])
			unbanThread.setName('nobots_unban_%s-Thread' % host)
			unbanThread.setDaemon(True)
			unbanThread.start()
			return
	           if nick.isalpha() and nick.islower() and ident.isalpha() and ident.islower() and 'virtual' in host and nick[:4] <> ident[:4] and len(nick) >= 3 and len(ident) >= 3:
		        self.botObj.who(nick)
	 elif re.search('^:[^ ]+ 352', textLine):
	      regExpElements = re.search('^:[^ ]+ [^ ]+ [^ ]+ (?P<channel>[^ ]+) (?P<ident>[^ ]+) (?P<host>[^ ]+) [^ ]+ (?P<nick>[^ ]+) (?P<modes>[^ ]+) :[0-9] (?P<realname>.*)$', textLine)
	      if regExpElements.group('modes') == 'Hx' and regExpElements.group('realname').isalpha() and regExpElements.group('realname').islower() and regExpElements.group('ident')[:4] <> regExpElements.group('realname')[:4] and regExpElements.group('nick')[:4] <> regExpElements.group('realname')[:4]:
	           for channel in self.botObj.channels:
		        if self.dictKicked.has_key(regExpElements.group('nick').lower()):
			     self.dictKicked[regExpElements.group('nick').lower()] = 9999999999
			else:
			     self.dictKicked[regExpElements.group('nick').lower()] = time.time()
		             if self.botObj.configuration.get('nobots', 'action') == 'onotice':
		                  self.botObj.onotice(channel, u'Creo que %s%s%s es un bot ...' % (irc.BOLD, regExpElements.group('nick'), irc.BOLD))
			     elif self.botObj.configuration.get('nobots', 'action') == 'kick':
			          self.botObj.kick(channel, regExpElements.group('nick'), u'Me has parecido un bot. Si me he equivocado vuelve a entrar y no serás expulsado.')
	 return
    # version: devuelve el nombre y version del módulo
    def version(self):
         return u'%s %s (%s)' % (__module_name__, __module_version__, __module_date__)
