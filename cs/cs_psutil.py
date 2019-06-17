import psutil
import wat

# for proc in psutil.process_iter():
#     wat.d(proc)

# CPU逻辑数量
wat.d(psutil.cpu_count())
# CPU物理核心
wat.d(psutil.cpu_count(logical=False))

# filter1 =[p.info for p in psutil.process_iter(attrs=['pid', 'name']) if 'python' in p.info['name']]
# wat.d(filter1)



from subprocess import check_output
def get_pid(name):
    return check_output(["pidof",name])

wat.d(get_pid('python'))
