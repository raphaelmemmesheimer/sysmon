# System Monitor

A tiny script for monitoring multiple servers. Stats currently shown are cpu, gpu, memory usage.
We use it in our lab to monitor the workload of our machine learning servers.

## Preview

![Sysmon preview](img/preview.png)

## Usage

* `pip install -r requirements.txt`
* `mkdir images`
* `sshfs <user>@<server>:<html_dir>/sysmon/images images`
* `python main.py`

Then navigate to: `https://<server>:<html_dir>/sysmon` in your browser.

