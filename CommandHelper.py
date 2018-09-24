
def loadSyntax():
    commands = []
    print('Command variations:')
    r = input()
    while r.lower() != 'done':
        commands.append(r)
        r = input()
    return commands


def printJavaComments(s): return print('/* {} */'.format(s))


TYPES = {
    'int': lambda n: print('argument("{}", IntegerArgumentType.integer(0))'.format(n), end=""),
    'float': lambda n: print('argument("{}", FloatArgumentType.floatArg(0.0F))'.format(n), end=""),

    # TODO
    'boolean': lambda n: print('boolean'),
    'String': lambda n: print('strings'),
    'BlockPos': lambda n: print('blockpos')
}

PARAMS = {
    'int': lambda n: ', IntegerArgumentType.getInteger(context, "{}")'.format(n),
    'float': lambda n: ', FloatArgumentType.getFloat(context, "{}")'.format(n),

    # TODO
    'boolean': lambda n: 'boolean',
    'String': lambda n: 'strings',
    'BlockPos': lambda n: 'blockpos'
}

current_params = []
current_functions = 0


def printStuff(arr):
    global current_functions, current_params
    arg = arr[0]
    if arg == '_':
        base = '.executes(context -> f{}(context.getSource()'.format(current_functions)
        current_functions += 1
        for param in current_params:
            base += param
        print(base + '))', end="")

        # Clears the current params, so you can't make a
        # "branch" after you added a non-literal argument
        current_params = []
    else:
        print('.then(', end="")
        if '_' in arg:
            argType = arg.split('_')[0]
            argName = arg.split('_')[1]
            TYPES[argType](argName)
            current_params.append(PARAMS[argType](argName))
        else:
            print('literal("{}")'.format(arg), end="")
        printStuff(arr[1:])
        print(')', end="")


def prep(cmds):
    for command in cmds:
        components = command.split(' ')[1:]
        components.append('_')
        printStuff(components)


########## INPUT ##########
commands = loadSyntax()
rootname = commands[0].split(' ')[0][1:]
print('\n')

########## REGISTER FUNCTION ##########
print(
    'public static void register(CommandDispatcher<CommandSource> dispatcher)\n{')
print('    dispatcher.register(literal("{}")'.format(rootname), end="")
prep(commands)
print(');\n}\n')
printJavaComments('Functions')
print()

########## HELPER FUNCTIONS ##########

for c, command in enumerate(commands):
    param = '(CommandSource src'

    for arg in command.split(' '):
        if '_' in arg:
            argArr = arg.split('_')
            param += ', {} {}'.format(argArr[0], argArr[1])
    param += ')'

    printJavaComments(command)
    print('private static int f' + str(c) + param + ' {return 1;}\n')


""" SOME TEST
/tps
/tps float_newTps
/tps warp int_ticks
done

/time query
/time set int_time
done
"""


""" Useless functions (parse dicctionary)

tree = parse(commands)

def parse(cmds):
    tree = {}
    for command in cmds:
        components = command.split(' ')[1:]
        components.append('_')
        tree = addComponents(tree, components)
    return tree
def addComponents(tree, arr):
    current = arr[0]
    if current == '_':
        tree[current] = 1
    elif current in tree.keys():
        tree[current] = addComponents(tree[current], arr[1:])
    else:
        tree[current] = addComponents({}, arr[1:])
    return tree
"""
