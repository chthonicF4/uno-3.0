import os ,pickle

def runSetup():
    print('running one time setup\n')
    print('installing required librays')
    os.system('cmd /c pip install pillow')
    print('loading assets')
    import main.card_gen

data = {
        'setup' : False
    }

try :
    file = open('setup.json','rb')
except FileNotFoundError :
    file = open('setup.json','wb')
    pickle.dump(data,file)
    file.close()
    file = open('setup.json','rb')

data = pickle.load(file)
if data['setup'] == True :
    pass
else:
    runSetup()
    print('\n')
    data['setup'] = True
    print('DONE !')


file.close()

file = open('setup.json','wb')
pickle.dump(data,file)
file.close()