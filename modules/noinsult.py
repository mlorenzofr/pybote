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
    
__module_name__ = 'mod-noInsult'
__module_version__ = '0.1' 
__module_author__ = 'Manuel Lorenzo Frieiro'
__module_description__ = 'Módulo que expulsa del canal a los nicks que insulten a un usuario del bot (según palabras prohibidas).'

# Módulos necesarios
#====================

import re
import irc

# Variables Globales
#====================

# Clases
#========

class noinsult:
    # Constructores de la clase:
    def __init__(self, botObject):
         self.botObj = botObject
         return

    # Métodos

    # interpreter: necesario para la comunicación del bot con el módulo
    def interpreter(self, textLine):
         checkLine = re.search('^:(?P<nick>[^ ]+)![^ ]+@(?P<host>[^ ]+) (PRIVMSG|NOTICE) (?P<channel>#[^ ]+) :(?P<message>.*)$', textLine.lower(), re.I)
	 if checkLine != None and checkLine.group('channel') in self.botObj.channels:
	      nick, phrase, host, channel = checkLine.group('nick'), checkLine.group('message'), checkLine.group('host'), checkLine.group('channel')
	      for user in self.botObj.db.getUserNicks():
	           if self.botObj.db.isInsulted(user, phrase):
		        if not self.botObj.configuration.getboolean('noinsult', 'ignore_ops') or not (self.botObj.isLoaded('address') and self.botObj.moduleList['address'].isOp(channel, nick)):
		             self.botObj.cmode(channel, '+b', '*!*@%s' % host)
			     self.botObj.kick(channel, nick, u'%s%seducación%s: %s(Del lat. educato, -nis)%s %s4.%s %sf.%s Cortesía, urbanidad.' % (irc.BOLD, irc.UNDERLINE, irc.CLEAR, irc.GREEN, irc.COLOR, irc.BOLD, irc.BOLD, irc.GRAY, irc.COLOR))
	 return

    # version: devuelve el nombre y version del módulo
    def version(self):
         return u'%s %s' % (__module_name__, __module_version__)
