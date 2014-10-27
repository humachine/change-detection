import pickle
from PIL import Image
from scipy.misc import toimage, imsave
def picklethis(data, filename='newpickle.pkl'):
    if '.pkl' in filename:
        pickle.dump(data, open( filename, "wb" ) )
    else:
        pickle.dump(data, open(filename + '.pkl', 'wb'))
    
def pickleload(filename):
    if '.pkl' in filename:
        return pickle.load( open( filename, "rb" ) )
    else:
        return pickle.load (open(filename + '.pkl', 'rb'))

def show(x):
    toimage(x).show()
    
def iswhitebg(x):
    imsave('temptemptemp.png', x)
    a=Image.open('temptemptemp.png')
    a= a.convert('1')
    data = a.load()
    if data[0,0]>=1:
        return True
    else:
        return False

