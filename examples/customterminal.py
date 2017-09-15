import sys, pyterminal;

def main():
	terminal = pyterminal.Terminal(commandset = pyterminal.CommandSet(), commands = sys.argv[1:]);
	terminal.run();
	
if __name__ == "__main__":
	main();