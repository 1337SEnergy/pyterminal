#TODO: CommandSet.replaceCommand(replace_what, replace_with);

class CommandSet():
	def __init__(self, commands = []):
		self.commands = {};
		commands.extend([Help(), Commands(), Exit()]);
		
		for command in commands:
			self.addCommand(command);
	
	def findCommand(self, command):
		if (type(command) != str and type(command) != unicode) or command not in self.commands:
			return None;
		
		return self.commands[command];
	
	def getCommands(self):
		return self.commands;
	
	def addCommand(self, command):
		if not isinstance(command, Command) or command.getName() in self.commands:
			return False;
		
		self.commands[command.getName()] = command;
		command.setCommandSet(self);
		
		return True;
	
	def removeCommand(self, command):
		if (type(command) != str and type(command) != unicode) or command not in self.commands:
			return False;
		
		self.commands[command].setCommandSet(None);
		del self.commands[command];
		
		return True;

class Command():
	def __init__(self):
		self.name = "";
		self.help = {"full":"", "brief":""};
		self.commandSet = None;
		self.arguments = 0;
	
	def getName(self):
		return self.name;
	
	def getHelp(self, type = None):
		if type == None:
			return self.help["full"];
		
		return self.help[type] if type in self.help else "";
	
	def getCommandSet(self):
		return self.commandSet;
	
	def setCommandSet(self, commandSet):
		if isinstance(commandSet, CommandSet) or commandSet == None:
			self.commandSet = commandSet;
	
	def checkArguments(self, arguments):
		if len(arguments) != self.arguments:
			raise Command.ArgumentException(self, len(arguments), self.arguments);
	
	def checkCommandSet(self):
		if not isinstance(self.commandSet, CommandSet):
			raise Command.CommandSetException(self);
	
	def execute(self, arguments = []):
		pass;
	
	#EXCEPTIONS
	class Error(Exception):
		pass;
	
	class ArgumentException(Error):
		def __init__(self, command, given, required):
			Command.Error.__init__(self, "ERROR: Command '{}' takes exactly {} {} ({} given)".format(command.getName(), required, "argument" if required == 1 else "arguments", given));
		
	class CommandSetException(Error):
		def __init__(self, command):
			Command.Error.__init__(self, "\t{}\nERROR: Command '{}' currently isn't part of a command set.".format(command.getHelp(), command.getName()));
		
	class CommandException(Error):
		def __init__(self, command):
			Command.Error.__init__(self, "ERROR: No command '{}' has been found.".format(command));

###	DEFAULT COMMANDS ###
class Commands(Command):
	def __init__(self):
		Command.__init__(self);
		
		self.name = "commands";
		self.help = {"full":"Displays all available commands in a command set.", "brief":"Display all available commands in a command set"};
	
	def execute(self, arguments = []):
		self.checkArguments(arguments);
		self.checkCommandSet();
		
		commands = self.getCommandSet().getCommands();
		commands_sorted = [command for command in commands];
		commands_sorted.sort();
		
		for cmd in commands_sorted:
			print "\t{} -> {}".format(cmd, commands[cmd].getHelp("brief"));

class Help(Command):
	def __init__(self):
		Command.__init__(self);
		
		self.name = "help";
		self.help = {"full":"Displays help for a command.\n\tUsage: help <command>", "brief":"Display help for a command"};
		self.arguments = 1;
	
	def execute(self, arguments = []):
		self.checkCommandSet();
		
		if len(arguments) == 0:
			print "\t{}".format(self.getHelp());
			return;
		
		self.checkArguments(arguments);
		
		cmd = self.getCommandSet().findCommand(arguments[0]);		
		if cmd == None:
			raise Command.CommandException(arguments[0]);
		
		print "\t{}".format(cmd.getHelp());

class Exit(Command):
	def __init__(self):
		Command.__init__(self);
		
		self.name = "exit";
		self.help = {"full":"Exits terminal and calls STOP function, if any.", "brief":"Exit terminal"};
	
	def execute(self, arguments = []):
		self.checkArguments(arguments);
		
		commandSet = self.getCommandSet();
		if commandSet != None:
			stop = commandSet.findCommand("stop");
			if stop != None:
				stop.execute();
		
		raise SystemExit;