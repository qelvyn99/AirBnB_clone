#!/usr/bin/python3

"""The cmd Module.
for building line-oriented command interpreters
"""
import cmd
from models.base_model import BaseModel
from models import storage
import re
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from datetime import datetime


class HBNBCommand(cmd.Cmd):
    prompt = "(hbnb) "

    CLASSES = {
        'BaseModel': BaseModel,
        'User': User,
        'State': State,
        'City': City,
        'Amenity': Amenity,
        'Place': Place,
        'Review': Review
    }

    def emptyline(self):
        """Do nothing on an empty line."""
        pass

    def do_EOF(self, line):
        """Exit the console on EOF (Ctrl+D) command."""
        print()
        return True

    def do_quit(self, line):
        """Quit command to exit the program."""
        return True

    def help_quit(self):
        """Help message for the quit command."""
        print("Quit command to exit the program\n")

    def handle_custom_command(self, class_name, action):
        """Handle custom commands like <class name>.all()
        or <class name>.count()."""
        parts = action.split("(")
        if len(parts) == 2 and parts[1].endswith(')'):
            action_name = parts[0]
            action_args = parts[1][:-1].split(',')

            # Remove surrounding quotes if present
            action_args = [arg.strip('\"') for arg in action_args]

            if action_name == 'show':
                key = "{}.{}".format(class_name, action_args[0])
                if key in storage.all():
                    print(storage.all()[key])
                else:
                    print(f"** no instance found **")
            elif action_name == 'all':
                instances = [
                    str(obj) for key, obj in storage.all().items()
                    if key.startswith(class_name + '.')
                ]
                print(instances)
            elif action_name == 'count':
                count = sum(
                    1 for key in storage.all()
                    if key.startswith(class_name + '.')
                )
                print(count)
            elif action_name == 'destroy':
                key = "{}.{}".format(class_name, action_args[0])
                if key in storage.all():
                    del storage.all()[key]
                    storage.save()
                else:
                    print(f"** no instance found **")
            elif action_name == 'update':
                key = "{}.{}".format(class_name, action_args[0])
                if key in storage.all():
                    obj = storage.all()[key]
                    attribute_name = action_args[1]
                    attribute_value = action_args[2]

                    # Update the attribute with the given value
                    setattr(obj, attribute_name, attribute_value)
                    obj.save()
                else:
                    print(f"** no instance found **")
            else:
                print(f"Unrecognized action: {action_name}.\
                Type 'help' for assistance.\n")
        else:
            print(f"Unrecognized action: {action}.\
            Type 'help' for assistance.\n")

    def default(self, line):
        """Handle unrecognized commands."""
        parts = line.split('.')
        if len(parts) == 2:
            class_name, action = parts
            self.handle_custom_command(class_name, action)
        else:
            print(f"Unrecognized command: {line}.\
                  Type 'help' for assistance.\n")

    def do_create(self, line):
        """Creates a new instance of BaseModel, saves it (to the JSON file)"""
        args = line.split()
        if not args:
            print("** class name missing **")
            return

        try:
            class_name = args[0]
            object = self.CLASSES[class_name]()
            object.save()
            print(object.id)
        except ImportError:
            print("** class doesn't exist **")

    def do_show(self, line):
        """Prints the string representation of an instance
        based on the class name and id."""
        args = line.split()
        if not args:
            print("** class name missing **")
        elif args[0] not in self.CLASSES:
            print("** class doesn't exist **")
        elif len(args) < 2:
            print("** instance id missing **")
        else:
            key = "{}.{}".format(args[0], args[1])
            if key not in storage.all():
                print("** no instance found **")
            else:
                print(storage.all()[key])

    def do_destroy(self, line):
        """Deletes an instance based on the class name and id
        (save the change into the JSON file)."""
        args = line.split()
        if not args:
            print("** class name missing **")
        elif args[0] not in self.CLASSES:
            print("** class doesn't exist **")
        elif len(args) < 2:
            print("** instance id missing **")
        else:
            key = "{}.{}".format(args[0], args[1])
            if key not in storage.all():
                print("** no instance found **")
            else:
                del storage.all()[key]
                storage.save()

    def do_all(self, line):
        """ Deletes an instance based on the class name and id
        (save the change into the JSON file).
        """
        args = line.split()

        if not args:
            print([str(obj) for obj in storage.all().values()])
        elif args[0] not in self.CLASSES:
            print("** class doesn't exist **")
        else:
            class_name = args[0]
            instances = [
                str(obj) for key, obj in storage.all().items()
                if key.startswith(class_name + '.')
            ]
            print(instances)

    def do_update(self, line):
        """Updates an instance based on the class name and id by adding
        or updating attribute (save the change into the JSON file).
        """
        args = line.split()

        if not args:
            print("** class name missing **")
            return

        rex = r'^(\S+)(?:\s(\S+)(?:\s(\S+)(?:\s(".*"|[^"]\S*)?)?)?)?'
        match = re.search(rex, line)

        if not match:
            print("** invalid command format **")
            return

        classname, uid, attribute, value = match.groups()

        if classname not in self.CLASSES:
            print("** class doesn't exist **")
            return
        elif not uid:
            print("** instance id missing **")
            return

        key = f"{classname}.{uid}"
        if key not in storage.all():
            print("** no instance found **")
            return
        elif not attribute:
            print("** attribute name missing **")
            return
        elif not value:
            print("** value missing **")
            return

        obj = storage.all()[key]
        setattr(obj, attribute, value)
        storage.all()[key].save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()