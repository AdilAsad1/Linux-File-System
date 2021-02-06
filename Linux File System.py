import sys
import pickle

class Cursor:
    def __init__(self):
        self.CurDir = 0
        self.tempDir = 0
        self.tempDir1 = 0

        
class Node:
    def __init__(self,name,type = 'dir',data = None):
        self.name = name
        self.type = type
        self.data = data
        self.parent = None
        self.children = []


output = ''
lst = []

class Tree:
    def __init__(self):
        self.root = Node('/')
        self.nodes = []

    def mkDir(self,name):
        n = Node(name)
        self.AddChild(C.CurDir,n)

    def mkDir1(self,name):
        n = Node(name)
        self.AddChild(C.tempDir,n)

    def AddChild(self, Pnode, Cnode):
        if Cnode != None:
            Pnode.children.append(Cnode)
            Cnode.parent = Pnode

    def Find(self,node,Cname):
        if node.children == []:
            return
        for i in node.children:
            if i.name == Cname:
                C.tempDir = i


    def touch(self,name,type = 'file',data=None):
        n = Node(name,type,data)
        self.AddChild(C.tempDir,n)

    def touch1(self,name,type = 'file',data=None):
        n = Node(name,type,data)
        self.AddChild(C.CurDir,n)

    def remove(self,Pnode,Cnode):
        if Cnode != None:
            self.Find(Pnode,Cnode)
            if C.tempDir.name == Cnode:
                Pnode.children.remove(C.tempDir)
    
    def PrintPathFromRoot(self, node):
        global output
        if node != None and node == self.root:
            output = output + '/'
        else:
            self.PrintPathFromRoot(node.parent)
            output += str(node.name) + '/'

        if output == '/':
            return output
        else:
            return output[0:-1]

    def compute_height(self,tree):
        if len(tree.children) == 0:
            return 0
        else:
            max_values = []
            for child in tree.children:
                max_values.append(self.compute_height(child))
            return 1 + max(max_values)

    def find(self,node,key):
        global lst
        if node.children == []:
            return
        else:
            for i in node.children:
                lst.append(i)
                self.find(i,key)
    
    def find1(self,key):
        global lst
        for i in lst:
            if i.name == key:
                global output
                output = ''
                print(tree.PrintPathFromRoot(i))

    def find2(self,key):
        global lst
        for i in lst:
            if i.data == key:
                count = 1
                data = i.data.split(' ')
                for i in data:
                    if i == '/n':
                        count += 1
                print('line',count)
                
                
            
            


def Save(obj,filename):
    with open(filename,'wb') as output:
        pickle.dump(obj,output)


def Load(filename):
    with open(filename,'rb') as input:
        t = pickle.load(input)


    
C = Cursor()
tree = Tree()

def main():
    
    C.CurDir = tree.root
    C.tempDir = tree.root
    C.tempDir1 = tree.root

    print('===================================')
    print('DSA Project 3')
    print('-----------------------------------')
    print('Virtual File System Emulator')
    print('===================================')
    
    while True:
        inStr = input('adil:~$ ')

        if inStr == 'exit':
            print('Terminating current session. Bye...')
            sys.exit(0)

        if inStr[0:5] == 'mkdir':
            error_msg = 'mkdir:'
            inStr2 = inStr.split(' ')
            
            if len(inStr2) < 2:
                print('mkdir: Too few arguments')
            if len(inStr2) > 2:
                print('mkdir: Too many arguments')
            if len(inStr2) == 2:
                if inStr2[1][0] == '/':
                    error_msg1 = inStr2[1]
                    inStr2 = str(inStr2[1])
                    inStr2 = inStr2[1:]
                    inStr2 = inStr2.split('/')
                    if len(inStr2) == 1:
                        print(error_msg,error_msg1,'directory name cannot begin with "/"')
                    else:
                        inStr3 = inStr2
                        C.tempDir = tree.root
                        while len(inStr2) != 1:
                            tree.Find(C.tempDir,inStr2[0])
                            inStr2 = inStr2[1:]
                        if C.tempDir.name == inStr3[-2] and C.tempDir.type == 'dir':
                            tree.mkDir1(inStr3[-1])
                        else:
                            print(error_msg,error_msg1,'No such file or directory')
                else:
                    if C.CurDir.type == 'dir':
                        tree.mkDir(inStr2[1])
            
        elif inStr[0:2] == 'ls' and len(inStr) == 2:
            for i in C.CurDir.children:
                if i.type == 'file':
                    print('-f-',i.name)
                else:
                    print('-d-',i.name)
            
        elif inStr[0:2] == 'ls' and len(inStr) > 2:
            inStr2 = inStr.split(' ')
            error_msg1 = inStr2[1]
            if len(inStr2) > 2:
                print('ls: Too many arguments')
            if len(inStr2) == 2:
                if inStr2[1][0] == '/':
                    inStr2 = str(inStr2[1])
                    error_msg = inStr2
                    inStr2 = inStr2[1:]
                    inStr2 = inStr2.split('/')
                    inStr3 = inStr2
                    C.tempDir = tree.root
                    while len(inStr2) != 0:
                        tree.Find(C.tempDir,inStr2[0])
                        inStr2 = inStr2[1:]
                    if C.tempDir.name == inStr3[-1]:
                        for i in C.tempDir.children:
                            if i.type == 'file':
                                print('-f-',i.name)
                            else:
                                print('-d-',i.name)
                    else:
                        print('ls:',error_msg,'No such file or directory')
                            
                else:
                    print('ls:',error_msg1,'invalid path')

        elif inStr[0:5] == 'touch':
            inStr2 = inStr.split(' ',1)
            if len(inStr2) == 2:
                if inStr2[1][0] == '/':
                    inStr2 = str(inStr2[1])
                    error_msg = inStr2
                    inStr2 = inStr2[1:]
                    inStr2 = inStr2.split(' ',1)
                    if len(inStr2) == 1:
                        inStr2 = str(inStr2[0])
                        
                        inStr2 = inStr2.split('/')
                        inStr3 = inStr2
                        C.tempDir = tree.root
                        while len(inStr2) != 1:
                            tree.Find(C.tempDir,inStr2[0])
                            inStr2 = inStr2[1:]
                        if C.tempDir.name == inStr3[-1] and C.tempDir.type == 'dir':
                            tree.touch(inStr2[-1])
                        else:
                            print('touch:',error_msg,'no such file or directory')
                    
                    else:
                        data = inStr2[1]
                        inStr2 = str(inStr2[0])
                        error_msg = '/'+str(inStr2)
                        inStr2 = inStr2.split('/')
                        inStr3 = inStr2
                        C.tempDir = tree.root
                        while len(inStr2) != 1:
                            tree.Find(C.tempDir,inStr2[0])
                            inStr2 = inStr2[1:]
                        if C.tempDir.name == inStr3[-2] and C.tempDir.type == 'dir':
                            tree.touch(inStr2[-1],'file',data)

                        else:
                            print('touch:',error_msg,'no such file or directory')

                else:
                    inStr2 = inStr2[1:]
                    inStr2 = str(inStr2[0])
                    inStr2 = inStr2.split(' ',1)
                    if len(inStr2) == 1:
                        tree.touch1(inStr2[0])
                    else:
                        tree.touch1(inStr2[0],'file',inStr2[1])
            else:
                print('touch: Too few arguments')

                
        elif inStr[0:3]== 'cat':
            inStr2 = inStr.split(' ')
            if len(inStr2) == 1:
                print('cat: Too few arguments')
            else:
                if inStr2[1][0] == '/':
                    inStr2 = str(inStr2[1])
                    error_msg = inStr2
                    inStr2 = inStr2[1:]
                    inStr2 = inStr2.split('/')
                    if len(inStr2) == 1:
                        C.tempDir = tree.root
                        tree.Find(C.tempDir,inStr2[0])
                        if C.tempDir.type == 'file' and C.tempDir.name == inStr2[0]:
                            print(C.tempDir.data)
                        else:
                            print('cat:',str(error_msg),'is a directory')
                    else:
                        inStr3 = inStr2
                        C.tempDir = tree.root
                        while len(inStr2) != 0:
                            tree.Find(C.tempDir,inStr2[0])
                            inStr2 = inStr2[1:]
                        if C.tempDir.name == inStr3[-1]:
                            print(C.tempDir.data)
                        else:
                            print('cat:',str(error_msg),'no such file or directory')
                else:
                    C.tempDir = tree.root
                    tree.Find(C.CurDir,inStr2[1])
                    if C.tempDir.name == inStr2[1] and C.tempDir.type == 'file':
                        print(C.tempDir.data)
                    else:
                        print('cat:',str(inStr2[1]),'no such file in current directory')


        elif inStr[0:2] == 'cd':
            inStr2 = inStr.split(' ')
            if len(inStr2) == 1:
                print('cd: Too few arguments')
            else:
                
                if inStr2[1] == '..':
                    if C.CurDir.parent != None:
                        C.CurDir = C.CurDir.parent
                        
                
                elif inStr2[1][0:2] == './':
                    inStr3 = str(inStr2[1])
                    inStr3 = inStr3.split('/')
                    inStr3 = inStr3[1:]
                    inStr4 = inStr3
                    if len(inStr3) == 1:
                        C.tempDir = C.CurDir
                        tree.Find(C.tempDir,inStr3[0])
                        if C.tempDir.type == 'dir' and C.tempDir.name == inStr4[0]:
                            C.CurDir = C.tempDir
                        else:
                            print('cd:',str(inStr2[1]),'no such file or directory')
                    else:
                        C.tempDir = C.CurDir
                        while len(inStr3) != 0:
                            tree.Find(C.tempDir,inStr3[0])
                            inStr3 = inStr3[1:]
                        if C.tempDir.name == inStr4[-1] and C.tempDir.type == 'dir':
                            C.CurDir = C.tempDir
                        else:
                            print('cd:',str(inStr2[1]),'no such file or directory')
                        
                    
                elif inStr2[1] == '~':
                    C.CurDir = tree.root
                    
                elif inStr2[1][0] == '/':
                    error_msg = inStr2[1]
                    inStr2 = str(inStr2[1])
                    inStr2 = inStr2[1:]
                    inStr2 = inStr2.split('/')
                    inStr3 = inStr2
                    if len(inStr2) == 1:
                        C.tempDir = tree.root
                        tree.Find(C.tempDir,inStr2[0])
                        if C.tempDir.type == 'dir' and C.tempDir.name == inStr2[0]:
                            C.CurDir = C.tempDir
                        else:
                            print('cd:',str(error_msg),'no such file or directory')
                    else:
                        C.tempDir = tree.root
                        while len(inStr2) != 0:
                            tree.Find(C.tempDir,inStr2[0])
                            inStr2 = inStr2[1:]
                        if C.tempDir.name == inStr3[-1] and C.tempDir.type == 'dir':
                            C.CurDir = C.tempDir
                        else:
                            print('cd:',str(error_msg),'no such file or directory')
                else:
                    error_msg = inStr2[1]
                    C.tempDir = tree.root
                    fname = inStr2[1]
                    tree.Find(C.CurDir,fname)
                    if C.tempDir.name == fname and C.tempDir.type == 'dir':
                        C.CurDir = C.tempDir
                    else:
                        print('cd:',str(error_msg),'no such file or directory')

        elif inStr == 'pwd':
            global output
            output = ''
            print(tree.PrintPathFromRoot(C.CurDir))
            
            
            
            
            
        
        elif inStr[0:2] == 'rm':
            inStr2 = inStr.split(' ')
            if len(inStr2) == 1:
                print('rm: Too few arguments')

            else:
                if inStr2[1][0] == '/':
                    inStr2 = str(inStr2[1])
                    error_msg = inStr2
                    inStr2 = inStr2[1:]
                    inStr2 = inStr2.split('/')
                    inStr3 = inStr2
                    if len(inStr2) == 1:
                        C.tempDir = tree.root
                        tree.Find(C.tempDir,inStr2[0])
                        if C.tempDir.name == inStr2[0]:
                            tree.remove(tree.root,inStr2[0])
                        else:
                            print('rm:',error_msg,'no such file or directory')
                    else:
                        C.tempDir = tree.root
                        while len(inStr2) != 1:
                            tree.Find(C.tempDir,inStr2[0])
                            inStr2 = inStr2[1:]
                        if C.tempDir.name == inStr3[-2]:
                            tree.remove(C.tempDir,inStr2[0])
                        else:
                            print('rm:',error_msg,'no such file or directory')

                else:
                    error_msg = inStr2[1]
                    C.tempDir = tree.root
                    tree.Find(C.tempDir,inStr2[1])
                    if C.tempDir.name == inStr2[1]:
                        tree.remove(C.CurDir,inStr2[1])
                    else:
                        print('rm:',str(error_msg),'no such file or directory')
                        
        elif inStr[0:2] == 'cp' or inStr[0:2] == 'mv':
            inStr2 = inStr.split(' ')
            if inStr[0:2] == 'cp':
                error_msg = 'cp:'
            else:
                error_msg = 'mv:'
            if len(inStr2) < 3:
                if inStr[0:2] == 'cp':
                    print('cp: Too few arguments')
                else:
                    print('mv: Too few arguments')
            else:
                if inStr2[1][0] == '/' and inStr2[2][0] == '/':
                    inStr3 = inStr2[1]
                    inStr4 = inStr2[2]
                    
                    inStr3 = str(inStr3)
                    inStr3 = inStr3[1:]
                    inStr3 = inStr3.split('/')
                    inStr3_1 = inStr3

                    if len(inStr3) == 1:
                        C.tempDir = tree.root
                        tree.Find(C.tempDir,inStr3[0])

                    else:
                        C.tempDir = tree.root
                        while len(inStr3) != 0:
                            tree.Find(C.tempDir,inStr3[0])
                            inStr3 = inStr3[1:]
                        print(C.tempDir.name)

                    if C.tempDir.name == inStr3_1[-1]:
                        file_to_move = C.tempDir
                        
                    else:
                        print(error_msg,'No such file pr directory')
                        
                    inStr4 = str(inStr4)
                    inStr4 = inStr4[1:]
                    inStr4 = inStr4.split('/')
                    inStr4_1 = inStr4

                    if len(inStr4) == 1:
                        C.tempDir = tree.root
                        tree.Find(C.tempDir,inStr4[0])

                    else:
                        C.tempDir = tree.root
                        while len(inStr4) != 0:
                            tree.Find(C.tempDir,inStr4[0])
                            inStr4 = inStr4[1:]

                    if C.tempDir.name == inStr4_1[-1]:
                        dir_to_move = C.tempDir
                    else:
                        print(error_msg,'No such file pr directory')

                    for i in dir_to_move.children:
                        if i.name == file_to_move.name:
                            tree.remove(dir_to_move,i.name)
                    Pnode = file_to_move.parent
                    tree.AddChild(dir_to_move,file_to_move)
                    if inStr[0:2] == 'mv':
                        tree.remove(Pnode,file_to_move.name)
                        

                else:
                    if inStr2[1][0] != '/' and inStr2[2][0] == '/':
                        inStr3 = inStr2[1]
                        inStr4 = inStr2[2]
                        C.tempDir = tree.root
                        tree.Find(C.CurDir,inStr3)
                        if C.tempDir.name == inStr3:
                            file_to_move = C.tempDir
                        else:
                            print(error_msg,'No such file pr directory')

                        inStr4 = str(inStr4)
                        inStr4 = inStr4[1:]
                        inStr4 = inStr4.split('/')
                        inStr4_1 = inStr4

                        if len(inStr4) == 1:
                            C.tempDir = tree.root
                            tree.Find(C.tempDir,inStr4[0])

                        else:
                            C.tempDir = tree.root
                            while len(inStr4) != 0:
                                tree.Find(C.tempDir,inStr4[0])
                                inStr4 = inStr4[1:]

                        if C.tempDir.name == inStr4_1[-1]:
                            dir_to_move = C.tempDir
                        else:
                            print(error_msg,'No such file pr directory')

                        for i in dir_to_move.children:
                            if i.name == file_to_move.name:
                                tree.remove(dir_to_move,i.name)

                        tree.AddChild(dir_to_move,file_to_move)
                        if inStr[0:2] == 'mv':
                            tree.remove(file_to_move.parent.parent,file_to_move.name)
                        
                        
                        
             


        elif inStr[0:4] == 'find':
            global lst
            lst = []
            inStr2 = inStr.split(' ',2)
            if len(inStr2) != 3:
                print('find: Too few arguments')

            elif len(inStr2) == 3 and inStr2[1] == '/':
                tree.find(tree.root,inStr2[2])
                print('Search Results')
                tree.find1(inStr2[2])

            elif len(inStr2) == 3 and inStr2[1][0] == '/' and len(inStr2[1]) > 1:
                inStr3 = str(inStr2[1])
                inStr3 = inStr3.split('/')
                inStr4 = inStr3
                if len(inStr3) == 1:
                    C.tempDir = tree.root
                    tree.Find(C.tempDir,inStr3[0])
                else:
                    C.tempDir = tree.root
                    while len(inStr3) != 0:
                        tree.Find(C.tempDir,inStr3[0])
                        inStr3 = inStr3[1:]
                    
                if C.tempDir.name == inStr4[-1]:
                    
                    tree.find(C.tempDir,inStr2[2])
                    print('Search Results')
                    tree.find1(inStr2[2])

                else:
                    print('find:',inStr2[1],'no such file or directory')

            elif len(inStr2) == 4:
                inStr3 = str(inStr2[1])
                inStr3 = inStr3.split('/')
                inStr4 = inStr3
                data = instr2[-1]
                if len(inStr3) == 1:
                    C.tempDir = tree.root
                    tree.Find(C.tempDir,inStr3[0])
                else:
                    C.tempDir = tree.root
                    while len(inStr3) != 0:
                        tree.Find(C.tempDir,inStr3[0])
                        inStr3 = inStr3[1:]
                    
                if C.tempDir.name == inStr4[-1]:
                    
                    tree.find(C.tempDir,inStr2[2])
                    print('Search Results')
                    tree.find2(inStr2[3])

                else:
                    print('find:',inStr2[1],'no such file or directory')
                
            

        elif inStr[0:4] == 'save':
            inStr2 = inStr.split(' ')
            if len(inStr2) == 2:
                filename = inStr2[1]
                Save(tree,filename)
                print('Virtual File System Saved in',filename)
            else:
                print('save: Too few arguments')

        elif inStr[0:4] == 'load':
            inStr2 = inStr.split(' ')
            if len(inStr2) == 2:
                filename = inStr2[1]
                Load(filename)
                print('Virtual File System Loaded') 

            else:
                print('load: Too few arguments')

        else:
            print('Invalid Command')
            
main()
