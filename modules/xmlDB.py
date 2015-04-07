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

__module_name__ = 'mod-xmlDB'
__module_version__ = '0.4.1r2'
__module_author__ = 'Manuel Lorenzo Frieiro'
__module_description__ = 'Módulo encargado de la gestión de las bases de datos XML del bot.'
__module_date__ = '2007/03/26'

# Módulos necesarios
#====================

import xml.sax
import re
import codecs
import time

# Variables Globales
#====================

# Clases
#========

class akickXML(xml.sax.ContentHandler):
    # Constructores de la clase
    def __init__(self):
         self.nick, self.reason = False, False
	 self.tmpNick, self.tmpReason, self.tmpType = '', '', ''
         self.akickList = { }
	 self.akickRE = { }
         return
    # Métodos
    # =======
    # startElement: análisis de la etiqueta de inicio
    def startElement(self, name, attrs):
         if name == 'nick':
	      self.tmpNick = ''
	      self.nick = True
	 elif name == 'reason':
	      self.tmpReason = ''
	      self.reason = True
	 elif name == 'akick':
	      atts = attrs.copy()
	      if atts.has_key('type'):
	           self.tmpType = atts.getValue('type')
	      else:
	           self.tmpType = 'nickname'
	 return
    # characters: lee un caracter incluído dentro de una etiqueta
    def characters(self, char):
         if self.nick:
	      self.tmpNick += char
	 elif self.reason:
	      self.tmpReason += char
	 return
    # endElement: se obtiene el cierre de etiqueta
    def endElement(self, name):
         if name == 'nick':
	      self.nick = False
	 elif name == 'reason':
	      self.reason = False
	 elif name == 'akick':
	      if self.tmpType == 'nickname':
	           self.akickList[self.tmpNick] = self.tmpReason
	      elif self.tmpType == 'regexp':
	           self.akickRE[self.tmpNick] = self.tmpReason
	      self.tmpNick, self.tmpReason, self.tmpType = '', '', ''
	 return
    # getAkickList: devuelve la variable akickList
    def getAkickList(self):
         return self.akickList
    # getREakicks: devuelve la lista de akicks con expresiones regulares
    def getREakicks(self):
         return self.akickRE

class userXML(xml.sax.ContentHandler):
    # Constructores de la clase
    def __init__(self):
         self.userList = { }
	 self.nickFlag, self.cmdFlag, self.insultFlag = False, False, False
	 self.tmpNick, self.tmpCmd, self.tmpInsult = '', '', ''
         self.tmpCmdList, self.tmpInsultList = [], []
         return
    # Métodos
    # ========
    # startElement: análisis de la etiqueta de inicio
    def startElement(self, name, attrs):
         if name == 'nick':
	      self.tmpNick = ''
	      self.nickFlag = True
	 elif name == 'command':
	      self.tmpCmd = ''
	      self.cmdFlag = True
	 elif name == 'insult':
	      self.tmpInsult = ''
	      self.insultFlag = True
	 return
    # characters: lee un caracter incluído dentro de una etiqueta
    def characters(self, char):
         if self.nickFlag:
	      self.tmpNick += char
	 elif self.cmdFlag:
	      self.tmpCmd += char
	 elif self.insultFlag:
	      self.tmpInsult += char
	 return
    # endElement: se obtiene el cierre de etiqueta
    def endElement(self, name):
         if name == 'nick':
	      self.nickFlag = False
	 elif name == 'command':
	      self.cmdFlag = False
	      self.tmpCmdList.append(self.tmpCmd)
	      self.tmpCmd = ''
	 elif name == 'insult':
	      self.insultFlag = False
	      self.tmpInsultList.append(self.tmpInsult)
	      self.tmpInsult = ''
	 elif name == 'user':
	      self.userList[self.tmpNick] = [self.tmpCmdList, self.tmpInsultList]
	      self.tmpNick, self.tmpCmd, self.tmpInsult = '', '', ''
	      self.tmpCmdList, self.tmpInsultList = [], []
	 return
    # getUserList: devuelve la variable akickList
    def getUserList(self):
         return self.userList

class serviceXML(xml.sax.ContentHandler):
    # Constructores de la clase
    def __init__(self):
         self.godList = []
	 self.tmpGod, self.tmpType = '', ''
	 return
    # startElement: análisis de la etiqueta de inicio
    def startElement(self, name, attrs):
         if name == 'service':
	      atts = attrs.copy()
	      if atts.has_key('type'):
	           self.tmpType = atts.getValue('type')
	      else:
	           self.tmpType = 'nickname'
	 return
    # characters: lee un caracter incluído dentro de una etiqueta
    def characters(self, char):
         self.tmpGod += char
	 return
    # endElement: se obtiene el cierre de etiqueta
    def endElement(self, name):
         if name == 'service':
	      self.godList.append([self.tmpType, self.tmpGod])
	      self.tmpGod, self.tmpType = '', ''
	 return
    # getGodList: devuelve la lista de intocables
    def getGodList(self):
         return self.godList

class spammerXML(xml.sax.ContentHandler):
    # Constructores de la clase
    def __init__(self):
         self.spammersList = { }
	 self.spammersREList = { }
	 self.nick, self.date = False, False
	 self.tmpSpammer, self.tmpType, self.tmpDate = '', '', ''
         return
    # startElement: análisis de la etiqueta de inicio
    def startElement(self, name, attrs):
         if name == 'spammer':
	      atts = attrs.copy()
	      if atts.has_key('type'):
	           self.tmpType = atts.getValue('type')
	      else:
	           self.tmpType = 'nickname'
	 elif name == 'nick':
	      self.nick = True
	      self.tmpSpammer = ''
	 elif name == 'date':
	      self.date = True
	      self.tmpDate = ''
         return
    # characters: lee un caracter incluído dentro de una etiqueta
    def characters(self, char):
         if self.nick:
              self.tmpSpammer += char
	 elif self.date:
	      self.tmpDate += char
	 return
    # endElement: se obtiene el cierre de etiqueta
    def endElement(self, name):
         if name == 'spammer':
	      if self.tmpType == 'nickname':
	           self.spammersList[self.tmpSpammer] = self.tmpDate
	      elif self.tmpType == 'regexp':
	           self.spammersREList[self.tmpSpammer] = self.tmpDate
	 elif name == 'nick':
	      self.nick = False
	 elif name == 'date':
	      self.date = False
	 return
    # getSpammerList: devuelve la lista de spammers
    def getSpammerList(self):
         return self.spammersList
    # getSpammerREList: devuelve la lista de spammers
    def getSpammerREList(self):
         return self.spammersREList

class dbXML:
    # Constructores de la clase
    def __init__(self, usersDB, akicksDB, servicesDB, spammersDB):
         self.usersFile = usersDB
	 self.akicksFile = akicksDB
	 self.servicesFile = servicesDB
	 self.spammersFile = spammersDB
         return
    # Métodos
    # =======
    # isAkicked: devuelve True si el nick indicado está en el akick, False en otro caso
    def isAkicked(self, nickname):
         XMLHandler = akickXML()
	 XMLParser = xml.sax.make_parser()
	 XMLParser.setContentHandler(XMLHandler)
	 XMLParser.parse(self.akicksFile)
	 if XMLHandler.getAkickList().has_key(nickname):
	      return True
	 else:
	      for regexp in XMLHandler.getREakicks().keys():
	           if re.search(regexp, nickname, re.I) != None:
		        return True
	 return False
    # isUser: devuelve True si el nick es usuario del bot, False en otro caso
    def isUser(self, nickname):
         XMLHandler = userXML()
         XMLParser = xml.sax.make_parser()
         XMLParser.setContentHandler(XMLHandler)
         XMLParser.parse(self.usersFile)
         if XMLHandler.getUserList.has_key(nickname):
	      return True
	 return False
    # isGod: devuelve True si la dirección pasada como parámetro está en la lista de usuarios a los que no se castigará
    def isGod(self, nickname, host):
         XMLHandler = serviceXML()
	 XMLParser = xml.sax.make_parser()
	 XMLParser.setContentHandler(XMLHandler)
	 XMLParser.parse(self.servicesFile)
	 for reg in XMLHandler.getGodList():
	      if reg[0] == 'nickname':
	           if re.search(reg[1], nickname) != None:
		        return True
	      elif reg[0] == 'host':
	           if re.search(reg[1], host) != None:
		        return True
	 return False
    # isSpammer: devuelve True si el nick indicado está en la lista de spammers, False en otro caso
    def isSpammer(self, nickname):
         XMLHandler = spammerXML()
	 XMLParser = xml.sax.make_parser()
	 XMLParser.setContentHandler(XMLHandler)
	 XMLParser.parse(self.spammersFile)
	 if nickname.lower() in XMLHandler.getSpammerList():
	      return True
	 else:
	      for regexp in XMLHandler.getSpammerREList():
	           if re.search(regexp, nickname, re.I) != None:
		        return True
         return False
    # hasPermission: devuelve True si el usuario puede ejecutar la orden, False en otro caso
    def hasPermission(self, nickname, command):
         XMLHandler = userXML()
	 XMLParser = xml.sax.make_parser()
	 XMLParser.setContentHandler(XMLHandler)
	 XMLParser.parse(self.usersFile)
	 userList = XMLHandler.getUserList()
	 if userList.has_key(nickname):
	      # if unicode(command, 'iso-8859-1', 'replace') in userList[nickname][0]:
	      if command in userList[nickname][0]:
	           return True
	 return False
    # getAkickReason: devuelve el motivo del akick de un nick
    def getAkickReason(self, nickname):
         XMLHandler = akickXML()
	 XMLParser = xml.sax.make_parser()
         XMLParser.setContentHandler(XMLHandler)
	 XMLParser.parse(self.akicksFile)
	 akickList = XMLHandler.getAkickList()
         if akickList.has_key(nickname):
              return akickList[nickname]
	 else:
	    for regexp in XMLHandler.getREakicks().keys():
	           if re.search(regexp, nickname, re.I) != None:
		        return XMLHandler.getREakicks()[regexp]
	 return False
    # isInsulted: devuelve True si en la cadena de texto pasada como parámetro aparece un nick y alguno de sus insultos
    def isInsulted(self, nickname, line):
         XMLHandler = userXML()
	 XMLParser = xml.sax.make_parser()
         XMLParser.setContentHandler(XMLHandler)
	 XMLParser.parse(self.usersFile)
	 userList = XMLHandler.getUserList()
         if userList.has_key(nickname):
	      for insult in userList[nickname][1]:
	           if re.search(nickname, line, re.I) != None and re.search(insult, line, re.I) != None:
		        return True
	 return False
    # modAkicks: modifica la bd de akicks
    def modAkicks(self, operation, nickname, reason=''):
         XMLHandler = akickXML()
	 XMLParser = xml.sax.make_parser()
         XMLParser.setContentHandler(XMLHandler)
         XMLParser.parse(self.akicksFile)
         akickList = XMLHandler.getAkickList()
	 akickREList = XMLHandler.getREakicks()
	 if operation == 'add':
	      if re.search('^@.+', nickname):
	           akickREList[nickname[1:]] = reason
	      else:
	           akickList[nickname] = reason
	 elif operation == 'del':
	      if akickList.has_key(nickname):
	           del akickList[nickname]
	      elif akickREList.has_key(nickname):
	           del akickREList[nickname]
	      else:
	           return False
	 else:
	      return False
	 outputHandle = codecs.open(self.akicksFile, 'w', 'iso-8859-1')
	 outputHandle.write('<?xml version=\'1.0\' encoding=\'ISO-8859-1\' ?>\n\n')
	 outputHandle.write('<akicks version=\'2.0\'>\n')
	 for nick, kick in akickList.iteritems():
	      outputHandle.write(' <akick type=\'nickname\'>\n  <nick>%s</nick>\n  <reason>%s</reason>\n </akick>\n' % (nick, kick))
	 for regexp, kick in akickREList.iteritems():
	      outputHandle.write(' <akick type=\'regexp\'>\n  <nick>%s</nick>\n  <reason>%s</reason>\n </akick>\n' % (regexp, kick))
	 outputHandle.write('</akicks>\n')
	 outputHandle.close()
	 return True
    # modSpammers: modifica la bd de spammers
    def modSpammers(self, operation, nickname):
         XMLHandler = spammerXML()
	 XMLParser = xml.sax.make_parser()
	 XMLParser.setContentHandler(XMLHandler)
	 XMLParser.parse(self.spammersFile)
	 spammersList = XMLHandler.getSpammerList()
	 spammersREList = XMLHandler.getSpammerREList()
	 if operation == 'add':
	      if re.search('^@.+', nickname):
	           spammersREList[nickname[1:]] = time.strftime('%d/%m/%Y', time.localtime())
	      else:
	           spammersList[nickname] = time.strftime('%d/%m/%Y', time.localtime())
	 elif operation == 'del':
	      if spammersList.has_key(nickname):
	           del spammersList[nickname]
	      elif spammersREList.has_key(nickname):
	           del spammersREList[nickname]
	      else:
	           return False
	 else:
	      return False
	 outputHandle = codecs.open(self.spammersFile, 'w', 'iso-8859-1')
	 outputHandle.write('<?xml version=\'1.0\' encoding=\'ISO-8859-1\' ?>\n\n')
	 outputHandle.write('<spammers version=\'1.0\'>\n')
	 for nick, date in spammersList.iteritems():
	      outputHandle.write(' <spammer type=\'nickname\'>\n  <nick>%s</nick>\n  <date>%s</date>\n </spammer>\n' % (nick, date))
	 for regexp, date in spammersREList.iteritems():
	      outputHandle.write(' <spammer type=\'regexp\'>\n  <nick>%s</nick>\n  <date>%s</date>\n </spammer>\n' % (regexp, date))
	 outputHandle.write('</spammers>\n')
	 outputHandle.close()
	 return True
    # modUsers: modifica la bd de usuarios
    def modUsers(self, operation, nickname, commands=['show'], insults=[]):
         XMLHandler = userXML()
	 XMLParser = xml.sax.make_parser()
         XMLParser.setContentHandler(XMLHandler)
         XMLParser.parse(self.usersFile)
         userList = XMLHandler.getUserList()
	 if operation == 'add':
	      userList[nickname] = [commands, insults]
	 elif operation == 'del':
	      del userList[nickname]
	 else:
	      return False
	 outputHandle = codecs.open(self.usersFile, 'w', 'iso-8859-1')
	 outputHandle.write('<?xml version=\'1.0\' encoding=\'ISO-8859-1\' ?>\n\n')
	 outputHandle.write('<users version=\'1.0\'>\n')
	 for nick, lists in userList.iteritems():
	      outputHandle.write(' <user>\n  <nick>%s</nick>\n' % nick)
	      for command in lists[0]:
	           outputHandle.write('  <command>%s</command>\n' % command)
	      for insult in lists[1]:
	           outputHandle.write('  <insult>%s</insult>\n' % insult)
	      outputHandle.write(' </user>\n')
	 outputHandle.write('</users>\n')
	 outputHandle.close()
	 return True
    # getAkickList: devuelve la lista con los nicks en la lista de akicks
    def getAkickNicks(self):
         XMLHandler = akickXML()
         XMLParser = xml.sax.make_parser()
         XMLParser.setContentHandler(XMLHandler)
         XMLParser.parse(self.akicksFile)
	 return XMLHandler.getAkickList().keys()
    # getUserNicks: devuelve la lista con los nicks en la lista de usuarios
    def getUserNicks(self):
         XMLHandler = userXML()
	 XMLParser = xml.sax.make_parser()
	 XMLParser.setContentHandler(XMLHandler)
	 XMLParser.parse(self.usersFile)
	 return XMLHandler.getUserList().keys()
    # getAkicks: devuelve el diccionario con los akicks y sus motivos
    def getAkicks(self):
         XMLHandler = akickXML()
         XMLParser = xml.sax.make_parser()
         XMLParser.setContentHandler(XMLHandler)
         XMLParser.parse(self.akicksFile)
         return XMLHandler.getAkickList()
    # getREAkicks: devuelve el diccionario con las expresiones regulares de los akicks y sus motivos
    def getREAkicks(self):
         XMLHandler = akickXML()
	 XMLParser = xml.sax.make_parser()
         XMLParser.setContentHandler(XMLHandler)
         XMLParser.parse(self.akicksFile) 
         return XMLHandler.getREakicks()
    # getSpammers: devuelve la lista de spammers
    def getSpammers(self):
         XMLHandler = spammerXML()
         XMLParser = xml.sax.make_parser()
         XMLParser.setContentHandler(XMLHandler)
         XMLParser.parse(self.spammersFile)
         return XMLHandler.getSpammerList()
    # getRESpammers: devuelve la lista de spammers como expresiones regulares
    def getRESpammers(self):
         XMLHandler = spammerXML()
	 XMLParser = xml.sax.make_parser()
         XMLParser.setContentHandler(XMLHandler)
         XMLParser.parse(self.spammersFile) 
         return XMLHandler.getSpammerREList()
    # version: devuelve el nombre y version del módulo
    def version(self):
	 return u'%s %s (%s)' % (__module_name__, __module_version__, __module_date__)
