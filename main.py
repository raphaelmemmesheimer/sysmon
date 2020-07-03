import pandas as pd
import matplotlib.pyplot as plt
import nvgpu
import psutil
import socket
import time
import json

system_stats = {"gpu":[], "cpu": [], "memory": [], "sensor": [], "disk": []}
machine_name = socket.gethostname()

def update():
    time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    system_stats["cpu"].append([time_str, psutil.cpu_percent()]) # this gives an average
    system_stats["memory"].append(psutil.virtual_memory().percent)
    system_stats["gpu"].append(nvgpu.gpu_info())
    #system_stats["sensor"].append(psutil.sensors_temperatures())
    #system_stats["disk"].append(psutil.disk_partitions())

def generate_graphs():
    print(system_stats)
    # GPU
    gpu_mem_used = []
    for gpu_info in system_stats["gpu"]:
        gpu_mem_used.append(gpu_info[0]["mem_used"])
    s = pd.Series(gpu_mem_used)
    fig, ax = plt.subplots()
    s.plot.bar()
    fig.savefig('images/%s_gpu_usage.png'%(machine_name))
    plt.close()

    # CPU
    s = pd.Series(system_stats["cpu"])
    fig, ax = plt.subplots()
    s.plot.bar()
    fig.savefig('images/%s_cpu_usage.png'%(machine_name))
    plt.close()

    # Memory
    mem_used = []
    for memory_info in system_stats["memory"]:
        mem_used.append(memory_info.percent)
    s = pd.Series(mem_used)
    fig, ax = plt.subplots()
    s.plot.bar()
    fig.savefig('images/%s_memory_usage.png'%(machine_name))
    plt.close()

    # Memory
    sensor_temp = []
    for sensor_info in system_stats["sensor"]:
        sensor_temp.append(sensor_info["coretemp"][0].current)
    s = pd.Series(sensor_temp)
    fig, ax = plt.subplots()
    s.plot.bar()
    fig.savefig('images/%s_sensor_temp.png'%(machine_name))
    plt.close()

def generate_json():
    #print(system_stats)
    with open('images/%s.json'%(machine_name), 'w') as f:
        json.dump(system_stats, f)


while True:
    update()
    #generate_graphs()
    generate_json()
    time.sleep(5)
