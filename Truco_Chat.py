#!/usr/bin/env python
# -*- coding: utf-8 -*-
# generated by wxGlade 0.6.4 on Wed Oct 10 15:20:53 2012
#creado por Agresta G. Franco

# begin wxGlade: extracode
# end wxGlade

import socket
import thread
from threading import Thread
import wx
import time

class Cliente(Thread):#anteriormente class Cliente(object), adaptado para correr en otro hilo
    def __init__(self, conectar, yoenvio):#se piden los parametros: el host y el objeto donde se mostarán las conversaciones 
        Thread.__init__(self)#Se inicia el thread

        self.aconectar = conectar###
#                                #### se copian los valores para usarlos fuera del constructor
        self.yoenvio = yoenvio######

        self._socket = socket.socket()#se crea un objeto socket para usarlo en la clase cliente

        self._socket.connect((str(self.aconectar), 6969))#se conecta el socket con el server en base al host que se ingresó por la variable conectar(ahora llamada self.aconectar)

        self.start()#Inicia la funcion run |>>(chan!)<<|, asi aparecen los ejemplos de threads y por ahora funciona.. asique dejalo esto así

    
    def teclado(self, algo):#Se le pasa como parametro la variable a enviar via socket

        self._socket.send(algo)#Envia el dato por socket(esto es una funcion del objeto socket)

    def printear(self, datoaenviar):#Esta funcion es la dedicada a que el cuadro de conversacion muestre lo que habia antes y lo nuevo que se quiere mostrar(a lo nuevo que se quiere mostrar se lo pasa como unico parámetro)
        habia_antes = self.yoenvio.GetValue()
        setear = str(datoaenviar) + "\n" + str(habia_antes) 
        self.yoenvio.SetValue(str(setear))
            
    def run(self):
        # hilo es para poder leer el teclado y el socket
        # al mismo tiempo, ya que los dos métodos se bloquean.

        self.printear("Conectado.")
        while 1:

            dato = self._socket.recv(2048) ## Esta linea..ESTA LINEA...\|/ recv es una funcion de los objetos socket que es para recibir datos y como parámetro se le envia "un tamaño de dato", este parametro debe ser el mismo en los archivos cliente y servidor

            if dato == "":#el cliente interpretara este dato cuando no haya coneccion con el server
                self.printear("\nEl server se ha desconectado.")
                break
            self.printear(dato)#agrega a la conversacion el dato recibido
        
        self.printear("\nCerrando...")
        self._socket.close()#cierra la coneccion del objeto socket
        self.printear("Cerrado.")


class Chat(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: Chat.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.frame_1_menubar = wx.MenuBar()#Menu
        self.lblAyuda = wx.Menu()#Menu

        self.lblComandos = wx.MenuItem(self.lblAyuda, wx.NewId(), "&Comandos", "Ayuda", wx.ITEM_NORMAL)#Menu
        self.lblAcerca = wx.MenuItem(self.lblAyuda, wx.NewId(), "&Acerca de...", "Ayuda", wx.ITEM_NORMAL)#Menu
        self.lblUso_Comandos = wx.MenuItem(self.lblAyuda, wx.NewId(), "&Modo de uso", "Ayuda", wx.ITEM_NORMAL)#Menu


        self.lblAyuda.AppendItem(self.lblAcerca)#Menu
        self.lblAyuda.AppendItem(self.lblComandos)#Menu
        self.lblAyuda.AppendItem(self.lblUso_Comandos)#Menu)#Menu
        self.frame_1_menubar.Append(self.lblAyuda, "&Ayuda")#Menu
        self.SetMenuBar(self.frame_1_menubar)#Menu

        self.Host = wx.StaticText(self, -1, "Host:")
        self.txtb_host = wx.TextCtrl(self, -1, "")
        self.btn_host = wx.Button(self, -1, "Conectar")
        self.label_2 = wx.StaticText(self, -1, u"Converación:")
        self.txtb_Conversacion = wx.TextCtrl(self, -1, "", style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.panel_1 = wx.Panel(self, -1)
        self.label_3 = wx.StaticText(self, -1, "Enviar:")
        self.txtb_Enviar = wx.TextCtrl(self, -1, "")
        self.btn_enviar = wx.Button(self, -1, "Enviar")

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.conectar, self.btn_host)
        self.Bind(wx.EVT_TEXT_ENTER, self.evtenter, self.txtb_Enviar)
        self.Bind(wx.EVT_BUTTON, self.enviar, self.btn_enviar)
        self.Bind(wx.EVT_MENU, self.EnComandos, self.lblComandos)
        self.Bind(wx.EVT_MENU, self.EnAcerca, self.lblAcerca)
        self.Bind(wx.EVT_MENU, self.EnUso_Comandos, self.lblUso_Comandos)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: Chat.__set_properties
        self.SetTitle("Truco Chat")
        self.txtb_host.SetMinSize((450, 27))
        self.txtb_Conversacion.SetMinSize((450, 340))
        self.txtb_Enviar.SetMinSize((450, 27))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: Chat.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        grid_sizer_1 = wx.FlexGridSizer(3, 3, 0, 0)
        grid_sizer_1.Add(self.Host, 0, 0, 0)
        grid_sizer_1.Add(self.txtb_host, 0, 0, 0)
        grid_sizer_1.Add(self.btn_host, 0, 0, 0)
        grid_sizer_1.Add(self.label_2, 0, 0, 0)
        grid_sizer_1.Add(self.txtb_Conversacion, 0, 0, 0)
        grid_sizer_1.Add(self.panel_1, 1, wx.EXPAND, 0)
        grid_sizer_1.Add(self.label_3, 0, 0, 0)
        grid_sizer_1.Add(self.txtb_Enviar, 0, 0, 0)
        grid_sizer_1.Add(self.btn_enviar, 0, 0, 0)
        sizer_1.Add(grid_sizer_1, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        self.Layout()
        # end wxGlade

    def conectar(self, event):  # wxGlade: Chat.<event_handler>
        host = self.txtb_host.GetValue()
        self.cli = Cliente(host, self.txtb_Conversacion)

    def evtenter(self, event):  # wxGlade: Chat.<event_handler>
        print "Event handler `evtenter' not implemented!"
        event.Skip()

    def enviar(self, event):  # wxGlade: Chat.<event_handler>
        noc = self.txtb_Enviar.GetValue()
        self.txtb_Enviar.SetValue("")
        self.cli.teclado(noc)

    def EnComandos(self, event): # wxGlade: MyFrame.<event_handler>
        ayuda = 'Chat Truco\n Comandos:\n         desconectar\n         cantar:\n         puntaje\n         terminar\n         pedir:\n         tirar:\n         nick:\n         decir_cartas\n         nueva_partida\n'
        dlg = wx.MessageDialog(self, ayuda, u'Comandos Chat Truco',wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()


    def EnAcerca(self, event): # wxGlade: MyFrame.<event_handler>
        ayuda = 'Chat con conección por LAN, con comandos para jugar al Truco argentino.\n         Creado por Agresta G. Franco (ITS Villada).\n                                        Versión: 2.2\n                              Hecho en Argentina.'
        dlg = wx.MessageDialog(self, ayuda, u'Acerca de: Chat Truco',wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

    def EnUso_Comandos(self, event): # wxGlade: MyFrame.<event_handler>
        ayuda = 'Conectarse con el host: Ingresar la direccion de intranet (de la computadora que esta corriendo el archivo server) en el cuadro de arriba y luego presionar conectar. Si todo salió bien deberia decir el cuador de conversación "conectado".\n\n'
        ayuda = ayuda + str("Enviar un mensaje: Ingresar el mensaje(o comando) en el cuadro de Enviar y presionar el botón enviar.\n\n")
        ayuda = ayuda + str("Uso de Comandos:\n\n")
        ayuda = ayuda + str("*'desconectar' :Este comando se usa para desconectarse del servidor\n")
        ayuda = ayuda + str("*'cantar:' :Luego de este comando se escribe la proposicion(truco, envido, etc)  para decirla y proponerla de una manera formal.\n")
        ayuda = ayuda + str("*'puntaje' :Este comando le dice el puntaje de los dos jugadores.\n")
        ayuda = ayuda + str("*'terminar':Hace que se termine la ronda. Cabe destacar que el otro jugador, luego de que se haya ejecutado el comando, debe escribir 'n'(para no terminar la ronda) o 's' (para terminar la ronda).\n")
        ayuda = ayuda + str("*'pedir:' :Luego de este comando se escribe los puntos(en numeros) que el jugador reclama. Cabe destacar que el otro jugador, luego de que se haya ejecutado el comando, debe escribir 'n'(para no entregar los puntos) o 's' (para entregar los puntos).\n")
        ayuda = ayuda + str("*'tirar:' :Luego de este comando se escribe el numero de carta que el jugador  usa en la 'mesa'(no podra usarla de nuevo).\n")
        ayuda = ayuda + str("*'nick:' :Luego de este comando se escribe el nick que el usuario quiere ponerse.\n")
        ayuda = ayuda + str("*'decir_cartas' :Le dice las respectivas cartas que posee a cada jugador.\n")
        ayuda = ayuda + str("*'nueva_partida' :Inicia una nueva ronda.\n")

        dlg = wx.MessageDialog(self, ayuda, u'Modo de uso de: Chat Truco',wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

# end of class Chat
if __name__ == "__main__":
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    frame_1 = Chat(None, -1, "")
    app.SetTopWindow(frame_1)
    frame_1.Show()
    app.MainLoop()