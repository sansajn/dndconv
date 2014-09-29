# multiproc bez nekonezneho loopu
import multiprocessing

def worker_func(jobs):
	while not jobs.empty():
		j = jobs.get()
		j.run()

class job:
	def __init__(self, name):
		self._name = name

	def run(self):
		print('Hello %s!' % self._name)

def main():
	jobs = multiprocessing.Queue()
	characters = ('Lisbon', 'Jane', 'Cho', 'Rigsby', 'Van Pelt')
	for ch in characters:
		jobs.put(job(ch))

	workers = []
	for i in range(0, multiprocessing.cpu_count()):
		w = multiprocessing.Process(target=worker_func, args=(jobs, ))
		w.start()
		workers.append(w)

	for w in workers:  # wait for all
		w.join()

	print('done!')

if __name__ == '__main__':
	main()
