import sys, os, queue, threading, subprocess
from PyQt4 import QtGui

class main_window(QtGui.QMainWindow):
	def __init__(self):
		QtGui.QMainWindow.__init__(self, None)
		self.setAcceptDrops(True)
		self._jobs = queue.Queue()  # job queue
		self._workers = self._hire_workers()
		self._run_workers()

	def dragEnterEvent(self, event):
		print('drag-enter-event')
		event.acceptProposedAction()

	def dropEvent(self, event):
		'\param event je typu QDropEvent'
		print('drop-event')
		mime = event.mimeData()
		if mime.hasUrls():
			urls = mime.urls()
			self._extract([url.toLocalFile() for url in urls])

	def _create_extract_job(self, video_file):
		out_dir = '/home/ja/temp/extract_test'
		out_file = os.path.join(out_dir, os.path.basename(video_file) + '.mp3')
		command = [
			'avconv', '-i',
			'%s' % video_file,
			'-f', 'mp3', '-ab', '192000', '-vn',
			'%s' % out_file]
		self._append_new_job(command)

	def _extract(self, videos):
		for v in videos:
			self._create_extract_job(v)

	def _run_workers(self):
		for w in self._workers:
			w.start()

	def _hire_workers(self):
		return [worker(self._jobs)]

	def _append_new_job(self, command):
		self._jobs.put(job(command))


class job:
	def __init__(self, command):
		self._command = command

	def run(self):
		subprocess.call(self._command)


class worker(threading.Thread):
	'abstrakcia pre vlakno'
	def __init__(self, jobs):
		threading.Thread.__init__(self)
		self._jobs = jobs

	def run(self):
		while True:
			j = self._jobs.get()
			j.run()


def main(args):
	app = QtGui.QApplication(args)
	w = main_window()
	w.show()
	app.exec_()

if __name__ == '__main__':
	main(sys.argv)
