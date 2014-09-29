# test funkcie is_alive()
import multiprocessing

def worker():
	pass

def main():
	p = multiprocessing.Process(target=worker)
	p.start()
	print('alive:', p.is_alive())
	p.join()
	print('alive:', p.is_alive())
	print('done!')

if __name__ == '__main__':
	main()
