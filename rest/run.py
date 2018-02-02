from eve import Eve
import platform
import psutil
from flask import jsonify

app = Eve()

#Processor name
@app.route('/performance/getProcessorName')
def processor():
    name = platform.processor()
    return name

#Version name
@app.route('/performance/version')
def version():
    verName = platform.version()
    return verName

#Node info
@app.route('/performance/nodeInfo')
def nodeInfo():
    nodeInfo = platform.node()
    return nodeInfo

#System name
@app.route('/performance/getSysName')
def sys_Name():
    sysName = platform.system()
    return sysName

#Disk partition
@app.route('/performance/getDiskPartitionInfo')
def disk_partition():
    diskPartition = psutil.disk_partitions()
    diskPartition_json = jsonify(diskPartition)
    return diskPartition_json

#Disk usage
@app.route('/performance/getDiskUsage')
def disk_usage():
    usage = psutil.disk_usage('/') 
    diskUsage_json = jsonify(usage)
    return diskUsage_json

#Disk I/O statistics
@app.route('/performance/getDiskIOStats')
def diskIO_Stats():
    diskIOStats = psutil.disk_io_counters(perdisk=True)
    diskIOStats_json = jsonify(diskIOStats)
    return diskIOStats_json

#System memory usage statistics
@app.route('/performance/getMemoryUsage')
def memory_usage():
    memoryUsage = psutil.virtual_memory()
    memoryUsage_json = jsonify(memoryUsage)
    return memoryUsage_json

#CPU Percent
@app.route('/performance/getCPUPercent')
def getCPUPercent():
    cpuPercent = psutil.cpu_times()
    cpuPercent_json = jsonify(cpuPercent)
    return cpuPercent_json
   
if __name__ == '__main__':
    app.run() 
