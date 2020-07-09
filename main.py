import nvgpu
import psutil
import socket
import time
import json
import hydra

matplotlib.use('Agg')

system_stats = {"gpu":[], "cpu": [], "memory": [], "sensor": [], "disk": []}
machine_name = socket.gethostname()

def update():
    time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    system_stats["cpu"].append([time_str, psutil.cpu_percent()]) # this gives an average
    system_stats["memory"].append(psutil.virtual_memory().percent)
    system_stats["gpu"].append(nvgpu.gpu_info())
    #system_stats["sensor"].append(psutil.sensors_temperatures())
    #system_stats["disk"].append(psutil.disk_partitions())


def generate_json(data_items):
    #print(system_stats)
    #with open('images/%s.json'%(machine_name), 'w') as f:
    filtered_stats = {}
    for key in system_stats.keys():
        filtered_stats[key] = system_stats[key][-data_items:]

    with open('%s/%s/%s.json'%(hydra.utils.get_original_cwd(), "images" ,machine_name), 'w') as f:
        json.dump(filtered_stats, f)


@hydra.main(config_path="config/config.yaml")
def sysmon_app(cfg):
    print(cfg.pretty())
    while True:
        update()
        #generate_graphs()
        generate_json(cfg.data_items)
        time.sleep(cfg.update_interval_in_s)


if __name__ == "__main__":
    sysmon_app()
