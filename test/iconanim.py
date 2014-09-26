import sys, math
from PyQt4 import QtCore, QtGui

class animated_widget(QtGui.QWidget):
	def __init__(self, image_name):
		QtGui.QWidget.__init__(self)
		self._img = QtGui.QImage(image_name)

		self._animation = False

		self._t = 0.0
		self._dt = 1000.0/5.0
		self._anim_time = 5000.0

		anim_timer = QtCore.QTimer()
		anim_timer.timeout.connect(self._timeout_event)
		anim_timer.start(self._dt)
		self._anim_timer = anim_timer

	def start_animation(self):
		self._animation = True

	def restore(self):
		self._animation = False

	def paintEvent(self, QPaintEvent):
		painter = QtGui.QPainter()
		painter.begin(self)
		w, h = (self.size().width(), self.size().height())
		iw, ih = (self._img.width(), self._img.height())
		p0 = (w/2.0 - iw/2.0, h/2.0 - ih/2.0)
		if self._animation:
			anim_t = self._anim_time
			part = (self._t - int(self._t/anim_t)*anim_t) / anim_t
			self._draw_image(p0, painter, self._img, part)
		else:
			painter.drawImage(QtCore.QPointF(p0[0], p0[1]), self._img)
		painter.end()

	def sizeHint(self):
		return QtCore.QSize(self._img.width(), self._img.height())

	def _timeout_event(self):
		self._t += self._dt
		self.update()

	def _draw_image(self, point, painter, image, part):
		'part je s rozsahu [0,1] kde 1 znamena vykreslenie celeho obrazku'
		iw, ih = (image.width(), image.height())
		ipart = QtGui.QImage(iw, ih, QtGui.QImage.Format_ARGB32)
		ipart.fill(0x00000000)

		npix = int(iw*ih*part)
		for r in range(0, int(npix/iw)):
			for c in range(0, iw):
				ipart.setPixel(c, r, image.pixel(c, r))

		r = math.ceil(npix/iw)-1
		for c in range(0, npix%iw):
			ipart.setPixel(c, r, image.pixel(c, r))

		painter.drawImage(QtCore.QPointF(point[0], point[1]), ipart)


class main_window(QtGui.QMainWindow):
	def __init__(self):
		QtGui.QMainWindow.__init__(self)
		self._animation = animated_widget('audio-x-generic.png')

		self._counter = QtGui.QLabel('0/0')
		self._counter.setAlignment(QtCore.Qt.AlignHCenter)

		vbox = QtGui.QVBoxLayout()
		vbox.addWidget(self._animation)
		vbox.addWidget(self._counter)
		widget = QtGui.QWidget()
		widget.setLayout(vbox)
		self.setCentralWidget(widget)

		self._animation.start_animation()


def main(args):
	app = QtGui.QApplication(args)
	w = main_window()
	w.show()
	app.exec_()

if __name__ == '__main__':
	main(sys.argv)
