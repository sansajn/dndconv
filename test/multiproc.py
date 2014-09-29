# pouzitie multiprocessing a queue
import multiprocessing

class job:
	def __init__(self, name):
		self._name = name

	def run(self):
		print('Hello %s!' % self._name)

def worker_funct(jobs):
	while True:
		j = jobs.get()
		j.run()

def main():
	jobs = multiprocessing.Queue()
	workers = []
	for i in range(0, 2):
		w = multiprocessing.Process(target=worker_funct, args=(jobs, ))
		w.start()
		workers.append(w)

	characters = ('Lisbon', 'Jane', 'Cho', 'Rigsby', 'Van Pelt')
	for ch in characters:
		jobs.put(job(ch))

	w.join()
	print('done!')

if __name__ == '__main__':
	main()


