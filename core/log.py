import time, traceback, sys, readline

""" 
	Provides logging methods and log file handling.
	Log files may be set up and added using addLogger() any output may be used.
	Log files are stored in a global list throughout program run time and will be written to each
	time a logging function is called.

	Call one of the logging functions to add a message, i.e log.panic(message) or log.notice(message).
	If no logger is set up prior to calling the function then it will silently fail.
"""
_logfiles = []
_levels = {
	'PANIC' : 0,
    'ALERT' : 1,
    'CRITICAL' : 2,
    'ERROR' : 3,
    'WARNING' : 4,
    'NOTICE' : 5,
    'INFO' : 6,
    'DEBUG' : 7,
}

def add_logger(file, level, verbose = False, screen = False):
	global _levels
	global _logfiles
	if level == None:
		return True
	if level not in _levels:
		return False
	if isinstance(file, str):
		file = open(file, 'a')
	_logfiles.append((file, level, verbose, screen))
	return True

""" 
	Gets the calling function by going down the stack trace to the defined
	point by the level. Some notes:
		level 0 - This is getCallingFunction, i.e THIS function.
		level 1 - This will be do_log because do_log called THIS.
		level 2 - This will be  one of the log calling functions, i.e 
																	log.panic()
																	log.notice()
																	log.debug()
		level 3 - This will be the true calling functions.
"""
def get_calling_function(levels):
	trace = traceback.extract_stack()
	if len(trace) > levels:
		frame = trace[-levels -1]
	else:
		frame = trace[0]
	return frame[2]

def do_log(loglevel, message):
	global _levels
	global _logfiles
	currentTime = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
	function = get_calling_function(3)
	lightMessage = "[%s] %8s: %s\n" % (currentTime, loglevel, message)
	verboseMessage = "[%s] %8s: %20s(): %s\n" % (currentTime, loglevel, function, message)
	for (file, level, verbose, screen) in _logfiles:
		if _levels[loglevel] <= _levels[level]:
			if verbose:
				file.write(verboseMessage)
				file.flush()
			else:
				if screen:
					sys.stdout.write('\r'+' '*(len(readline.get_line_buffer())+2)+'\r')
					file.write(lightMessage)
					file.flush()
					print('> ' + readline.get_line_buffer())
					# sys.stdout.flush()
				else:
					file.write(lightMessage)
					file.flush()

""" The functions which may be called to log messages. """
def panic(message):
    do_log('PANIC', message)

def alert(message):
    do_log('ALERT', message)

def critical(message):
    do_log('CRITICAL', message)

def error(message):
    do_log('ERROR', message)

def warning(message):
    do_log('WARNING', message)

def notice(message):
    do_log('NOTICE', message)

def info(message):
    do_log('INFO', message)

def debug(message):
    do_log('DEBUG', message)
