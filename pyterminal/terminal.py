import npyscreen, sys;
import commandset;

class ActionControllerConsole(npyscreen.ActionControllerSimple):
	def create(self):
		self.add_action("", self.exec_command, False);
	
	def exec_command(self, command_line, widget_proxy, live):
		if len(command_line) == 0:
			return;
		
		while command_line.find("  ") != -1:
			command_line = command_line.replace("  ", " ");
		
		try:
			if command_line[0] == " ":
				command_line = command_line[1:];
			if command_line[-1] == " ":
				command_line = command_line[:-1];
		except IndexError:
			return;
		
		command_line = command_line.split(" ");
		
		try:
			#self.parent.wCommand.value = "";
			#self.parent.wCommand.display();
			
			print "{}: {}".format(self.parent.wStatus2.value, " ".join(command_line));
			if self.parent.commandSet == None:
				raise Exception("\tERROR: Terminal currently has no command set!");
			
			cmd = self.parent.commandSet.findCommand(command_line[0]);
			if cmd == None:
				raise commandset.Command.CommandException(command_line[0]);
			
			cmd.execute(command_line[1:]);
		except Exception as e:
			print str(e);
		
		print "";
		self.parent.wMain.display();

class Console(npyscreen.FormMuttActive):
	MAIN_WIDGET_CLASS = npyscreen.BufferPager;
	ACTION_CONTROLLER = ActionControllerConsole;
	
	def consolePrint(self, s):
		if len(s) == 1 and (s == "\n" or s == " "):
			if len(self.wMain.values) > 0:
				if isinstance(self.wMain, npyscreen.BufferPager):
					self.wMain.buffer([], scroll_end = True);
		else:			
			newLine = s.find("\n");
			sNext = "";
			if newLine > -1:
				sNext = s[newLine+1:];
				s = s[:newLine];
			
			if isinstance(self.wMain, npyscreen.MultiLine):
				self.wMain.values.append(s);
			elif isinstance(self.wMain, npyscreen.BufferPager):
				self.wMain.buffer([s], scroll_end = True);
			elif isinstance(self.wMain, npyscreen.Pager):
				self.wMain.values.append(s);
			
			if len(sNext) > 0:
				self.consolePrint(sNext);
		
		self.wMain.display();

class Terminal(npyscreen.NPSAppManaged):	
	def __init__(self, **kwargs):
		self.inputName = kwargs["input"] if "input" in kwargs else "Input ";
		self.outputName = kwargs["output"] if "output" in kwargs else "Output ";
		
		self.commandSet = kwargs["commandset"] if "commandset" in kwargs else None;
		self.commands = kwargs["commands"] if "commands" in kwargs else None;
		
		npyscreen.NPSAppManaged.__init__(self);
	
	def main(self):
		self.form = Console();
		sys.stdout = Terminal.Writer(self.form);
		
		self.form.wStatus1.value = self.outputName;
		self.form.wStatus2.value = self.inputName;
		self.form.wMain.editable = False;
		
		self.form.commandSet = self.commandSet;
		if self.commands != None:
			for command in self.commands:
				self.form.wCommand.value = command;
				self.form.wCommand.h_execute_command();
		
		self.form.edit();
	
	class Writer():
		def __init__(self, console):
			self.console = None;
			if isinstance(console, Console):
				self.console = console;
		
		def write(self, s):
			if isinstance(self.console, Console):
				self.console.consolePrint(s);