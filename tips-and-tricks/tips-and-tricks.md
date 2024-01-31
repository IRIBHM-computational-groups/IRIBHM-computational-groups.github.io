---
description: A few essential tips for bioinformatics
---

# 🧠 Tips & tricks

## Useful commands

Here is a list of useful commands that you'll find on most linux distributions. Feel free to question other lab members about them or check their official documentation (google search, man command or --help argument).

* htop (look at RAM and CPU usage)
* nvidia-smi (look at GPU usage)
* killall -u ${USER} (kill all your processes, to clean up)
* kill (when a process stops responding, killall also works)
* screen or tmux (terminal multiplexers, keep your processes running in background)
* rsync or scp (transfer files or folders between machines)
* chmod (define permissions for a file/folder)
* df (statistics on disks)
* du (evalutate folder/file size, do not use on /mnt/iribhm)
* getfattr -n ceph.dir.rbytes /mnt/iribhm/blabla (evaluate size of folder on /mnt/iribhm)

Here is an example of how to use the getfattr command to list the folder sizes in /mnt/iribhm :&#x20;

```
for i in $(ls /mnt/iribhm); do getfattr -n ceph.dir.rbytes /mnt/iribhm/$i; done
```

## Speedup your ssh connections

If you're not a jupyterlab addict you'll probably connect to hyperion with ssh a lot. Thus speeding up that process will make you save lots of time down the line. The most obvious speedup will come from your ${HOME}/.ssh/config file where you can define hostnames and a series of other variables for each host. Here is an example of config file for hyperion VMs :&#x20;

```
# ULB cluster ----------------------------------------------------------------------
Host gpu01 gpu02 gpu03 himem
    User atourneu
    ForwardX11 yes
Host builder
    User atourneu
    Hostname iribhm-builder.hpda.ulb.ac.be
Host gpu03
    Hostname iribhm-gpu03.hpda.ulb.ac.be
Host gpu02
    Hostname iribhm-gpu02.hpda.ulb.ac.be
Host gpu01
    Hostname so-iribhm-gpu01.hpda.ulb.ac.be
Host himem
    Hostname iribhm-himm01.hpda.ulb.ac.be
```

The other major speedup comes from ssh keys. They allow you to connect to the host in a more secure way, and you can do it without being prompted for a password if you don't set a password when you create your keys. You can easily find tutorials online to set up your ssh keys, here is an example :&#x20;

[https://www.cyberciti.biz/faq/how-to-set-up-ssh-keys-on-linux-unix/](https://www.cyberciti.biz/faq/how-to-set-up-ssh-keys-on-linux-unix/)

## Configure your bashrc profile

The file ${HOME}/.bashrc is automatically sourced every time you start a terminal. You can thus use it both to define useful helper functions and variable, or semi-automate certain tasks. For instance if there's a command you use very often you can define an alias for it :&#x20;

```
alias csi='cd /mnt/iribhm/software/singularity'
alias singuR='singularity exec /mnt/iribhm/homes/atourneu/r_full.sif R'
```

A variable you need :&#x20;

```
export PATH=${PATH}:/mnt/iribhm/software/bin
```

A task you want to automate upon each terminal startup :&#x20;

```
chmod -R 750 ${HOME}
chmod 600 ${HOME}/.ssh/*
```

Here is how I backup my code with git :&#x20;

```
eval $(ssh-agent)
ssh-add ${HOME}/.ssh/id_rsa.github
cd ${HOME}/scripts/
git add -A
git commit -m "$(date)"
git push
```

Automating storage checks to anticipate /mnt/iribhm saturation :&#x20;

```
PERCENTIRIBHM=`df -k /mnt/iribhm | grep "/mnt/iribhm" | awk '{print $(NF-1)}'`
if [ ${PERCENTIRIBHM::-1} -gt 95 ]; then echo '### WARNING ### IRIBHM STORAGE HAS REACHED 95 PERCENT CAPACITY ### CLEANING IS ADVISED'; fi
```
