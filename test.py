import pickle

RECENTS = 'recents.pkl'

def add(path):
    with open(RECENTS, 'rb') as file:
        stack = pickle.load(file)
    if path not in stack:
        stack.append(path)
    else:
        stack.remove(path)
        stack.append(path)
    stack = stack[-4:]
    print(len(stack))
    with open(RECENTS, 'wb') as file:
        pickle.dump(stack, file)

def change(oldpath, newpath):
    with open(RECENTS, 'rb') as file:
        stack = pickle.load(file)
    stack.remove(oldpath)
    stack.append(newpath)
    stack = stack[-4:]
    print(len(stack))
    with open(RECENTS, 'wb') as file:
        pickle.dump(stack, file)

def get():
    with open(RECENTS, 'rb') as file:
        stack = pickle.load(file)
    return stack