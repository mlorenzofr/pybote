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
    
__module_name__ = 'mod-antiFlood'
__module_version__ = '0.2' 
__module_author__ = 'Manuel Lorenzo Frieiro'
__module_description__ = 'Expulsa a aquellos nicks que repiten demasiado en el canal.'

# Módulos necesarios
#====================

import re
import time

# Variables Globales
#====================

# Clases
#========

class noflood:
    # Constructores de la clase:
    def __init__(self, botObject):
         self.botObj = botObject
	 self.floodList = {}
	 for channel in self.botObj.channels:
	      self.floodList[channel] = []
         return

    # Métodos

    # interpreter: necesario para la comunicación del bot con el módulo
    def interpreter(self, textLine):
         checkLine = re.search('^:(?P<nick>[^ ]+)![^ ]+@(?P<host>[^ ]+) (PRIVMSG|NOTICE) (?P<channel>#[^ ]+) :(?P<message>.*)$', textLine.lower(), re.I)
         if checkLine != None and checkLine.group('channel') in self.botObj.channels and not self.botObj.db.isGod(checkLine.group('nick'), checkLine.group('host')):
	      repetitions = 0
	      nick, phrase, channel, host = checkLine.group('nick'), checkLine.group('message'), checkLine.group('channel'), checkLine.group('host')
	      self.floodList[channel].append([time.time(), nick, phrase])
	      for reg in self.floodList[channel]:
	           if (time.time()-reg[0]) > 10:
		        self.floodList[channel].remove(reg)
	      for reg in self.floodList[channel]:
	           if reg[1] == nick and reg[2] == phrase:
		        repetitions += 1
	      if repetitions > 3:
	           if not self.botObj.configuration.getboolean('noflood', 'ignore_ops') or not (self.botObj.isLoaded('address') and self.botObj.moduleList['address'].isOp(channel, nick)):
	                self.botObj.cmode(channel, '+b', '*!*@%s' % host)
		        self.botObj.kick(channel, nick, 'Demasiadas repeticiones')
	 return

    # version: devuelve el nombre y version del módulo
    def version(self):
	 return u'%s %s' % (__module_name__, __module_version__)
