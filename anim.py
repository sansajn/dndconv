import sys
from PyQt4 import QtCore, QtGui

class main_window(QtGui.QMainWindow):
	def __init__(self):
		QtGui.QMainWindow.__init__(self, None)
		# self.resize(140, 110)

		timer = QtCore.QTimer()
		timer.timeout.connect(self._timeout_event)
		timer.start(1000)
		self._anim_timer = timer

		self._workers = 3
		self._njobs = 10
		self._ndone = 3
		self._progress = self._workers*[0.0]
		self._MAXFILL = 10

		self._progmets = progress_metrics(self.font())
		self._max_progress_w = 2*self._progmets.bound_w + self._MAXFILL*self._progmets.fill_w

	def paintEvent(self, QPaintEvent):
		painter = QtGui.QPainter()
		painter.begin(self)

		w, h = (self.size().width(), self.size().height())
		fill_h = self._progmets.fill_h
		workers = self._workers
		text_h = (1+workers)*fill_h
		p0 = ((w-self._max_progress_w)/2, (h-text_h)/2+fill_h)

		for i in range(0, workers):
			self._draw_progress((p0[0], p0[1]+i*fill_h), painter, self._progress[i], self._MAXFILL)

		counter_text = '%d/%d' % (self._ndone, self._njobs)
		painter.drawText(QtCore.QPointF((w-self._progmets.fm.width(counter_text))/2,
			p0[1]+workers*fill_h), counter_text)

		painter.end()

	def _draw_progress(self, point, painter, progress, max_grids = 10):
		'progress je v rozsahu [0,1]'
		p0 = point
		bound_w, fill_w = (self._progmets.bound_w, self._progmets.fill_w)
		painter.drawText(QtCore.QPointF(p0[0], p0[1]), '[')
		grids = min(int(progress*max_grids), max_grids)
		for n in range(0, grids):
			painter.drawText(QtCore.QPointF(p0[0]+bound_w+n*fill_w, p0[1]), '#')

		prog_text = '%d%%' % (progress*100, )
		prog_text_w = self._progmets.fm.width(prog_text)
		if (bound_w+grids*fill_w+3+prog_text_w+1) < self._max_progress_w:
			# still enought place for progress value
			prog_p = (p0[0]+bound_w+grids*fill_w, p0[1])
			painter.drawText(QtCore.QPointF(prog_p[0]+3, prog_p[1]), prog_text)

		painter.drawText(QtCore.QPointF(p0[0]+bound_w+max_grids*fill_w, p0[1]), ']')

	def _timeout_event(self):
		self._progress = [self._progress[0]+0.1, self._progress[1]+0.135, self._progress[2]+0.08]
		self.update()

class progress_metrics:
	def __init__(self, font):
		self.fill_char = '#'
		self.open_bound_char = '['
		self.close_bound_char = ']'
		fm = QtGui.QFontMetricsF(font)
		self.fm = fm
		self.bound_w = fm.width(self.open_bound_char)
		self.bound_h = fm.height()
		self.fill_w = fm.width(self.fill_char)
		self.fill_h = fm.height()


def main(args):
	app = QtGui.QApplication(args)
	w = main_window()
	w.show()
	app.exec_()

if __name__ == '__main__':
	main(sys.argv)
