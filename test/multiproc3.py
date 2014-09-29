# test zdielaneho slovnika
import multiprocessing, time

def worker(d, wait):
	time.sleep(wait)
	d['count'] += 1

def main():
	mgr = multiprocessing.Manager()

	d = mgr.dict()
	d['count'] = 0

	workers = []
	for i in range(0, 10):
		w = multiprocessing.Process(target=worker, args=(d, i))
		w.start()
		workers.append(w)

	while d['count'] < 9:
		time.sleep(1)
		print(d['count'])

	print('done!')


if __name__ == '__main__':
	main()
