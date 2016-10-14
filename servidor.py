# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtCore, QtGui, uic 

class Vivora():
	def __init__(self):	#init de prueba
		self.Id = "0"
		self.cuerpo = [(1, 0), (2, 0), (3, 0),  (4, 0),  (5, 0)]
		self.direccion = 0;
		self.color = {'b' : 70, 'r' : 100, 'g' : 150}
	
	def actualiza(self, table, col, fil):
		del self.cuerpo[0]
		lr, ud = self.cuerpo[3]
		if (self.direccion == 0  or self.direccion == 2):
			lr = ((1 if self.direccion == 0 else -1)+lr)%col
		else:
			ud = ((1 if self.direccion == 3 else -1)+ud)%fil
		self.cuerpo.append((lr, ud))

formClass , baseClass = uic.loadUiType("servidor.ui")

class ServidorApp(formClass, baseClass):
	def __init__(self, parent = None):
		formClass.__init__(self)
		baseClass.__init__(self)
		self.setupUi(self)
		self.juegoActivo = 0
		self.vivoras = []
		self.timer = QtCore.QTimer()
		self.btn_terminar = QtGui.QPushButton('Terminar Juego')	#boton para terminar el juego
		self.table.horizontalHeader().setResizeMode(1)
		self.table.verticalHeader().setResizeMode(1)
		self.table.setFocusPolicy(0x3)
		self.table.keyPressEvent = self.keyPressEventOvrr	#sobreescritura de metodo
		
		#conectamos a los botones y mas a las funciones adecuadas.
		self.timer.setInterval(self.spinBox_Wait.value())
		self.spinBox_Columnas.valueChanged.connect(self.cambiarTam)
		self.spinBox_Filas.valueChanged.connect(self.cambiarTam)
		self.spinBox_Wait.valueChanged.connect(self.cambiarEspera)
		self.btn_Juego.clicked.connect(self.cambiaEstado)
		self.btn_terminar.clicked.connect(self.acabaJuego)
		self.timer.timeout.connect(self.mainloop)
		
		self.show()
	
	#Cambia la velocidad del juego
	def cambiarEspera(self):
		self.timer.setInterval(self.spinBox_Wait.value())
	
	#cambia el numero de colas y filas en la TableWidget
	def cambiarTam(self):
		self.table.setRowCount(self.spinBox_Filas.value())
		self.table.setColumnCount(self.spinBox_Columnas.value())
	
	def keyPressEventOvrr(self, event):	#para probar los controles
		if event.key() == QtCore.Qt.Key_Up and self.vivoras[0].direccion != 3:
			self.vivoras[0].direccion = 1
		elif event.key() == QtCore.Qt.Key_Down and self.vivoras[0].direccion != 1:
			self.vivoras[0].direccion = 3
		elif event.key() == QtCore.Qt.Key_Left and self.vivoras[0].direccion != 0:
			self.vivoras[0].direccion = 2
		elif event.key() == QtCore.Qt.Key_Right and self.vivoras[0].direccion != 2:
			self.vivoras[0].direccion = 0
	
	#Cambia el estado del juego
	def cambiaEstado(self):
		if self.juegoActivo == 0:		#juego no ha comenzado
			self.btn_Juego.setText("Pausar el juego")
			self.juegoActivo = 1
			self.vivoras.append(Vivora())
			self.timer.start()
			self.btn_terminar.show()
			self.verticalLayout.addWidget(self.btn_terminar)
		elif self.juegoActivo == -1:	#juego esta en pausa
			self.btn_Juego.setText("Pausar el juego")
			self.juegoActivo = 1
			self.timer.start()
		else:							#juego esta activo
			self.btn_Juego.setText("Continuar el juego")
			self.juegoActivo = -1
			self.timer.stop()
	
	#Regresa todo al estado original
	def acabaJuego(self):
		self.juegoActivo = 0
		self.btn_Juego.setText("Inicia Juego")
		self.verticalLayout.removeWidget(self.btn_terminar)
		self.btn_terminar.hide()
		self.table.clear()
		self.vivoras.clear()
		self.timer.stop()
	
	#dibuja las serpientes
	def dibuja(self):
		for v in self.vivoras:
			for (x, y) in v.cuerpo:
				if self.table.item(y, x) == None:	#si cae en una celda llena se elimina, si no, entonces se llena.
					self.table.setItem(y, x, QtGui.QTableWidgetItem())
					self.table.item(y, x).setBackground(QtGui.QColor(v.color['r'], v.color['g'], v.color['b']))
				else:
					self.vivoras.remove(v)
					del v
					break;
	
	#actualiza las vivoras
	def actualizaVivoras(self):
		for v in self.vivoras:
			v.actualiza(self.table, self.table.columnCount(),self.table.rowCount())
	
	#loop principal del juego
	def mainloop(self):
		if self.juegoActivo == 1:
			self.table.clear()
			self.actualizaVivoras()
			self.dibuja()

if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	window = ServidorApp()
	sys.exit(app.exec_())
