#!/usr/bin/python3
from ast import arg
import cmd
from models.base_model import BaseModel
from models.user import User
from models import storage


class HBNBCommand(cmd.Cmd):

    prompt = '(hbnb) '
    classes = ['BaseModel', 'User']

    def do_quit(self, args):
        'Quit command to exit the program\n'
        return True

    def do_EOF(self, args):
        'Quit command to exit the program\n'
        return True

    def postcmd(self, stop, line):
        if line == 'EOF':
            return True
        return stop

    def emptyline(self):
        pass

    def do_create(self, arg):
        """
        Creates a new instance of a class,
        saves it (to the JSON file) and prints the id
        Usage: create <class_name>
        """
        if not arg:
            print("** class name missing **")
        elif arg not in HBNBCommand.classes:
            print("** class doesn't exist **")
        else:
            new = eval(arg+"()")
            print(new.id)
            storage.save()

    def do_show(self, arg):
        """
        Prints the string representation of an instance
        based on the class name and id
        Usage: show <class_name> <id>
        """
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** class id missing **")
        else:
            try:
                print(storage.all()[args[0]+"."+args[1]])
            except KeyError:
                print("** no instance found **")

    def do_destroy(self, arg):
        """
        Deletes an instance based on the class name and id
        (save the change into the JSON file).
        Usage: destroy <class_name> <id>
        """
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** class id missing **")
        else:
            try:
                del storage.all()[args[0]+"."+args[1]]
                storage.save()
            except KeyError:
                print("** no instance found **")

    def do_all(self, arg):
        """
        Prints all string representation of all instances
        based or not on the class name.
        Usage: all [<class_name>]
        class_name is an optional parameter
        """
        if arg != "":
            args = arg.split(' ')
            className = args[0]
            if className not in HBNBCommand.classes:
                print("** class doesn't exist **")
            else:
                output = []
                for key, value in storage.all().items():
                    if type(value).__name__ == className:
                        output.append(str(value))
                print(output)
        else:
            print([str(value) for key, value in storage.all().items()])

    def do_update(self, arg):
        """
        Updates an instance
        Usage: update <class name> <id> <attribute name> "<attribute value>"
        """
        args = arg.split()
        # looks ugly hahaha
        classname = args[0] if len(args) > 0 else None
        uid = args[1] if len(args) > 1 else None
        attribute = args[2] if len(args) > 2 else None
        value = args[3] if len(args) > 3 else None

        if not classname:
            print("** class name missing **")
        elif classname not in HBNBCommand.classes:
            print("** class doesn't exist **")
        elif not uid:
            print("** instance id missing **")
        else:
            key = "{}.{}".format(classname, uid)
            if key not in storage.all():
                print("** no instance found **")
            elif not attribute:
                print("** attribute name missing **")
            elif not value:
                print("** value missing **")
            else:
                storage.all()[key].__dict__[attribute] = value.replace('"', "")
                storage.save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
