# dndconv (Drag&Drop convertor)
import sys, os, math, shlex, subprocess, multiprocessing
from PyQt4 import QtGui, QtCore
import ui_settings

# todo: uprav pocet worker-ov pri drag&drop-e
# todo: pridaj notifikacie do desktop-menu

class main_window(QtGui.QMainWindow):
	def __init__(self):
		QtGui.QMainWindow.__init__(self, None)
		# gui
		self.setAcceptDrops(True)
		self.resize(120, 90)

		self._animation = animated_widget('audio-x-generic.png')

		self._counter_label = QtGui.QLabel('Drag&Drop files here!')
		self._counter_label.setAlignment(QtCore.Qt.AlignHCenter)

		vbox = QtGui.QVBoxLayout()
		vbox.addWidget(self._animation)
		vbox.addWidget(self._counter_label)
		widget = QtGui.QWidget()
		widget.setLayout(vbox)
		self.setCentralWidget(widget)

		tm = QtCore.QTimer()
		tm.timeout.connect(self._event_gui_timer)
		tm.start(1000/60)
		self._gui_timer = tm

		self._nfiles_to_extract = 0

		# actions (context menu)
		self._settings_act = QtGui.QAction('Settings ...', self)
		self._settings_act.triggered.connect(self._open_settings_dialog)
		self.addAction(self._settings_act)
		self.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)

		# settings
		self._settings_dlg = settings_dialog()

		# concurent
		self._workers = None
		self._job_queue = multiprocessing.Queue()
		self._mgr = multiprocessing.Manager()
		self._d = self._mgr.dict()
		self._jobcounter = 0

	def dropEvent(self, event):
		'\param event je typu QDropEvent'
		working = self._num_working_jobs() > 0

		local_files = self._local_files(event)
		if len(local_files) > 0:
			jobs = self._create_extract_jobs(local_files)
			for j in jobs:
				self._job_queue.put(j)

			if not working:
				self._workers = self._hire_workers(len(jobs))
				self._run_workers()
				self._nfiles_to_extract = len(jobs)
				self._event_extraction_start()
			else:
				self._nfiles_to_extract += len(jobs)

	def dragEnterEvent(self, event):
		event.acceptProposedAction()

	def closeEvent(self, event):
		# terminate all alive processes
		if self._workers:
			for w in self._workers:
				if w.is_alive():
					w.terminate()
		QtGui.QMainWindow.closeEvent(self, event)

	def _local_files(self, event):
		mime = event.mimeData()
		if mime.hasUrls():
			urls = mime.urls()
			return [url.toLocalFile() for url in urls]
		else:
			return []

	def _hire_workers(self, njobs):
		nworkers = min(max(multiprocessing.cpu_count(), 1), njobs)
		workers = []
		for n in range(0, nworkers):
			w = multiprocessing.Process(target=worker_func, args=(self._job_queue, self._d))
			workers.append(w)
		return workers

	def _run_workers(self):
		for w in self._workers:
			w.start()

	def _create_extract_jobs(self, videos):
		'vrati zoznam jobov'
		return [self._create_extract_job(v) for v in videos]

	def _output_file_name(self, out_dir, video_file):
		audio_name = os.path.splitext(os.path.basename(video_file))[0]
		fname_path = os.path.join(out_dir, audio_name + '.mp3')
		if os.path.exists(fname_path):
			return self._generate_new_filename(out_dir, audio_name, 1)
		else:
			return fname_path

	def _generate_new_filename(self, dst_path, audio_name, num):
		audio_file = os.path.join(dst_path, audio_name+(' (%d)' % num)+'.mp3')
		if os.path.exists(audio_file):
			return self._generate_new_filename(dst_path, audio_name, num+1)
		else:
			return audio_file

	def _create_extract_job(self, video_file):
		out_dir = os.path.expanduser(self._settings_dlg.output_directory())
		out_file = self._output_file_name(out_dir, video_file)
		profile = {
			'vfile':video_file,
			'ofile':out_file,
			'bitrate':self._settings_dlg.bitrate(),
			'format':self._settings_dlg.format(),
			'command_line':self._settings_dlg.command_line()
		}
		cmdline = 'avconv -i "%(vfile)s" -f %(format)s -ab %(bitrate)s %(command_line)s "%(ofile)s"' % profile
		self._jobcounter += 1
		return job(self._jobcounter, shlex.split(cmdline))

	def _event_extraction_start(self):
		self._animation.start_animation()
		self._counter_label.setText('0/%d' % (self._nfiles_to_extract,))

	def _event_extraction_stop(self):
		self._animation.restore()
		self._d.clear()
		self._nfiles_to_extract = 0
		self._counter_label.setText('Done!')
		self._debug_check_workers_alive()

	def _event_gui_timer(self):
		if len(self._d) is 0:
			return

		ndone_files = self._num_done_jobs()
		done = ndone_files is len(self._d)

		if done:
			self._event_extraction_stop()
		else:
			self._counter_label.setText('%d/%d' % (ndone_files, self._nfiles_to_extract))

	def _num_done_jobs(self):
		ndone_jobs = 0
		for k, v in self._d.items():
			if v:
				ndone_jobs += 1
		return ndone_jobs

	def _num_working_jobs(self):
		nwork_jobs = 0
		for k, v in self._d.items():
			if not v:
				nwork_jobs += 1
		return nwork_jobs

	def _open_settings_dialog(self):
		self._settings_dlg.setModal(True)
		self._settings_dlg.show()

	def _debug_check_workers_alive(self):
		# for w in self._workers:
		# 	assert not w.is_alive(), 'some workers are still alive'
		pass

class job:
	def __init__(self, jobid, command):
		self._id = jobid
		self._command = command

	def run(self):
		subproc = subprocess.Popen(self._command)
		subproc.wait()

	def id(self):
		return self._id

def worker_func(jobs, d):
	while not jobs.empty():
		j = jobs.get()
		d[j.id()] = False  # working
		j.run()
		d[j.id()] = True  # done

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
		self._load_settings()

	def bitrate(self):
		return int(self.lineEditBitrate.text())*1000

	def format(self):
		return str(self.lineEditFormat.text())

	def output_directory(self):
		return str(self.lineEditDir.text())

	def command_line(self):
		return str(self.lineEditCmd.text())

	def hideEvent(self, event):
		self._save_settings()
		QtGui.QDialog.hideEvent(self, event)

	def on_pushButtonOutDir_released(self):
		odir = QtGui.QFileDialog.getExistingDirectory()
		self.lineEditDir.setText(odir)

	def _save_settings(self):
		s = \
			"settings = {\n" \
			"\t'output-directory':'%s',\n" \
			"\t'bitrate':%s,\n" \
			"\t'format':'%s',\n" \
			"\t'command-line':'%s'\n" \
			"}\n" % (self.output_directory(), int(self.lineEditBitrate.text()), self.format(), self.command_line())

		with open(os.path.expanduser('~/.dndconv'), 'w') as fout:
			fout.write(s)

	def _load_settings(self):
		loc = {}
		glob = {}
		try:
			with open(os.path.expanduser('~/.dndconv')) as fin:
				exec(fin.read(), glob, loc)

			settings = loc['settings']
			self.lineEditBitrate.setText(str(settings['bitrate']))
			self.lineEditFormat.setText(settings['format'])
			self.lineEditDir.setText(settings['output-directory'])
			self.lineEditCmd.setText(settings['command-line'])
		except OSError:
			pass

def main(args):
	app = QtGui.QApplication(args)
	w = main_window()
	w.show()
	app.exec_()

if __name__ == '__main__':
	main(sys.argv)
