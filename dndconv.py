# dndconv (Drag&Drop convertor)
import sys, os, math, shlex, queue, threading, subprocess, multiprocessing
from PyQt4 import QtGui, QtCore
import ui_settings

# todo: ukladaj settingsi
# todo: implementuj file-dialog (v settingsoch)
# todo: pridaj notifikacie do desktop-menu
# todo: prejdi na multiprocessing

class main_window(QtGui.QMainWindow):
	def __init__(self):
		QtGui.QMainWindow.__init__(self, None)
		# gui
		self.setAcceptDrops(True)
		self.resize(120, 90)

		self._animation = animated_widget('audio-x-generic.png')

		self._counter = QtGui.QLabel('Drag&Drop files here!')
		self._counter.setAlignment(QtCore.Qt.AlignHCenter)

		vbox = QtGui.QVBoxLayout()
		vbox.addWidget(self._animation)
		vbox.addWidget(self._counter)
		widget = QtGui.QWidget()
		widget.setLayout(vbox)
		self.setCentralWidget(widget)

		self._nfiles_to_extract = 0
		self._ndone_files = 0

		# actions
		self._settings_act = QtGui.QAction('Settings ...', self)
		self._settings_act.triggered.connect(self._open_settings_dialog)
		self.addAction(self._settings_act)
		self.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)

		# settings
		self._settings_dlg = settings_dialog()

		# concurent
		self._jobs = queue.Queue()  # job queue
		self._workers = self._hire_workers()
		self._run_workers()

	def dropEvent(self, event):
		'\param event je typu QDropEvent'
		mime = event.mimeData()
		if mime.hasUrls():
			urls = mime.urls()
			local_files = [url.toLocalFile() for url in urls]
			if len(local_files) > 0:
				self._extract(local_files)
				self._nfiles_to_extract = len(local_files)
				self._event_extraction_start()

	def dragEnterEvent(self, event):
		event.acceptProposedAction()

	def closeEvent(self, event):
		for w in self._workers:
			w.retire()
		QtGui.QMainWindow.closeEvent(self, event)

	def _event_extraction_start(self):
		self._counter.setText('%d/%d' % (self._ndone_files, self._nfiles_to_extract))
		self._animation.start_animation()

	def _event_extraction_stop(self):
		self._counter.setText('Done!')
		self._animation.restore()

	def _event_job_done(self):
		self._ndone_files += 1
		self._counter.setText('%d/%d' % (self._ndone_files, self._nfiles_to_extract))

	def _create_extract_job(self, video_file):
		out_dir = os.path.expanduser(self._settings_dlg.output_directory())
		out_file = os.path.join(out_dir,	os.path.splitext(os.path.basename(video_file))[0] + '.mp3')
		profile = {
			'vfile':video_file,
			'ofile':out_file,
			'bitrate':self._settings_dlg.bitrate(),
			'format':self._settings_dlg.format()
		}
		cmdline = 'avconv -i "%(vfile)s" -f %(format)s -ab %(bitrate)s -vn "%(ofile)s"' % profile
		self._append_new_job(shlex.split(cmdline))

	def _extract(self, videos):
		for v in videos:
			self._create_extract_job(v)

	def _run_workers(self):
		for w in self._workers:
			w.start()

	def _hire_workers(self):
		ncores = min(multiprocessing.cpu_count(), 1)
		workers = []
		for n in range(0, ncores):
			w = worker(self._jobs)
			self.connect(w, QtCore.SIGNAL('nojobs'), self._event_extraction_stop)
			self.connect(w, QtCore.SIGNAL('jobdone'), self._event_job_done)
			workers.append(w)
		return workers

	def _append_new_job(self, command):
		self._jobs.put(job(command))

	def _open_settings_dialog(self):
		self._settings_dlg.setModal(True)
		self._settings_dlg.show()

class job:
	def __init__(self, command):
		self._command = command
		self._proc = None

	def run(self):
		self._proc = subprocess.Popen(self._command)
		self._proc.wait()
		self._proc = None

	def cancel(self):
		if self._proc:
			self._proc.kill()

class worker(threading.Thread, QtCore.QObject):
	'abstrakcia pre vlakno'
	def __init__(self, jobs):
		threading.Thread.__init__(self), QtCore.QObject.__init__(self)
		self._jobs = jobs
		self._current_job = None
		self._retire = False

	def run(self):
		while not self._retire:
			try:
				j = self._jobs.get(timeout=1)
				self._current_job = j
				j.run()
				self._notify_job_done()
				if self._jobs.empty():
					self._notify_no_jobs()
			except queue.Empty as e:
				if not self._retire:
					continue  # len vyprsal timeout, znovu cakaj na job
				else:
					return  # skonci, thread je ukonceny

	def retire(self):
		self._retire = True
		if self._current_job:
			self._current_job.cancel()

	def _notify_no_jobs(self):
		self.emit(QtCore.SIGNAL('nojobs'))

	def _notify_job_done(self):
		self.emit(QtCore.SIGNAL('jobdone'))

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

class settings_dialog(QtGui.QDialog, ui_settings.Ui_Settings):
	def __init__(self):
		QtGui.QDialog.__init__(self)
		self.setupUi(self)

	def bitrate(self):
		return int(self.lineEditBitrate.text())*1000

	def format(self):
		return str(self.lineEditFormat.text())

	def output_directory(self):
		return str(self.lineEditDir.text())

	def command_line(self):
		return str(self.lineEditCmd.text())

def main(args):
	app = QtGui.QApplication(args)
	w = main_window()
	w.show()
	app.exec_()

if __name__ == '__main__':
	main(sys.argv)
