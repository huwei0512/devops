#encoding:utf-8
import os,sys,argparse
def get_files(dirpath):
    _rt_list = []
    if os.path.isdir(dirpath):
        for name in os.listdir(dirpath):
            _path = dirpath + '/' + name
            if os.path.isdir(_path):
                _rt_list.extend(get_files(_path))
            elif _path.endswith('.py'):
                _rt_list.append(_path)
    return _rt_list

if __name__ == "__main__":
     _parser = argparse.ArgumentParser()
     _parser.add_argument('-H','--host',help='connect host ip address',default='localhost')
     _parser.add_argument('-P','--port',help='connect host port address',type=int,default=9090)
     _parser.add_argument('-C','--cmds',help='execute cmd',nargs='+',default=[])
     _args = _parser.parse_args()
     '''
     1.host,port必须有
     '''
     if len(_args.cmds) == 0 :
         print _parser.print_help() 
         sys.exit(-1)
     print _args
     print 'success'