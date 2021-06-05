import sys

'''
## descript to this file ###
2021-05-12 by Artificial_Lua

this file is for import file

setup() -> load and split system arguments
    if you have incorrect option then python will exit
    correct option will split to tuple likes (True / False , argumentValue)

get(opt) -> return correct option's value
    if you have correct option, return tuple likes (True, value)
    you have no any correct option, return tuple(False, None)

## descript to this file ###
'''

class option():
    def __init__(self) -> None:
        self.options = []
        self.value = []

    def setup(self, opts) :
        self.options = opts
        for arg in range(1, len(sys.argv) // 2 + 1):
            i = arg * 2 - 1
            if sys.argv[i] in self.options:
                if(sys.argv[i] == "--help"):
                    return "help"
                self.value.append([sys.argv[i], sys.argv[i + 1]])
            else :
                print("Option error : %s is not in option" % sys.argv[i])
                quit()
    
    def get(self, opt):
        for i in range(0, (len(self.value))):
            if self.value[i][0] == opt:
                
                return (True, self.value[i][1])
        return (False, None)