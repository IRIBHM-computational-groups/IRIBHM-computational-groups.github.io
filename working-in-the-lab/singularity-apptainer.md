---
description: Running your analyses in a reproducible manner on Hyperion
---

# 📦 Singularity/Apptainer

## What are singularity containers ?

Singularity containers are comparable to docker containers, except that they are designed to operate on scientific clusters such as Hyperion. You can consider them as a variant of virtual machines except that their goal is to isolate applications and not computer resources. They are also easier to create and use than virtual machines. The project was originally named Singularity but it was split in november 2021 in two separate entities, and the one we use is called Apptainer. Yet the apptainer and singularity commands can both be used interchangeably. The official documentation can be found on apptainer's website : [https://apptainer.org/documentation/](https://apptainer.org/documentation/)

To verify the version currently installed on Hyperion you can use the command :

`apptainer --version`

## How to use singularity containers ?

The containers can be used either via the command line or through the jupyterlab web interface. To use them through jupyterlab just connect to the URL of your desired VM and click on the container you need when starting a new notebook.

With the command line they can be used interactively (e.g. apptainer shell) or non-interactively (e.g. apptainer exec). The documentation describing how to use them can be found here : [https://apptainer.org/docs/user/latest/quick\_start.html#interacting-with-images](https://apptainer.org/docs/user/latest/quick\_start.html#interacting-with-images)

They can of course also be used in tmux or screen sessions .

## How to build singularity containers ?

### Creating a new container on the builder VM

Containers are built on the builder VM using the "apptainer build" command. You always build a new container upon a pre-existing one, whether it is online or from one of yours. The proper way to build containers is to use definition files. These definition files are text files containing a set of instructions, very similar to the commands you would enter in your terminal to install software on a linux machine. The structure of those definition files and the proper way to use the build command is described here : [https://apptainer.org/docs/user/latest/build\_a\_container.html](https://apptainer.org/docs/user/latest/build\_a\_container.html)

Personal or development containers can be built in your home folder on the builder VM. If you want to share the definition file of one of your containers, you can put it in the /opt/common folder of the builder VM. This folder contains a git repository that is set up to sync all files with the .def extension to the team's github group.

Note : sandboxes can be useful for debugging purposes when creating complex containers but they are not reproducible, use them at your own risks. If you have to use them, make sure that you track the changes you made in a separate text file.

### Enabling the newly created container

Once a container has been created on the builder VM it can be copied on the production VMs (himm and the 3 GPU VMs) using a command such as rsync or scp. You can copy them on the IRIBHM mount which is shared among those 4 VMs, either in your home folder or in the shared singularity folder : /mnt/iribhm/software/singularity

Once they are copied they can be used directly with the command line. If you wish to use them on jupyterlab you must create a new kernel for this container. Kernels are stored in ${HOME}/.local/share/jupyter/kernels. You may need to create this folder the first time :&#x20;

`mkdir -p ${HOME}/.local/share/jupyter/kernels`

Each kernel is composed of a folder (named as you wish) containing at least a kernel.json file. You can adapt one of the examples kernel files provided below (depending on whether you want R or python). To do so just edit the path to your container in the kernel.json file as well as the display\_name variable, which is the name that will be displayed in the jupyterlab interface. You may also need to adapt the path to the executable in your container.

```
{ 
 "argv": ["/usr/bin/singularity", 
   "exec", 
   "--writable-tmpfs", 
   "/home/joerodri/software/cell2location/cell2location-v0.05-alpha.sif", 
   "/opt/conda/envs/cellpymc/bin/python", 
   "-m", 
   "ipykernel", 
   "-f", 
   "{connection_file}" 
 ], 
 "display_name": "Cell2Loc",
 "language": "python"
} 
```

```
{
  "argv": ["/usr/bin/singularity",
    "exec",
    "--writable-tmpfs",
    "--nv",
    "/mnt/iribhm/software/singularity/r_full.sif",
    "/usr/lib/R/bin/R",
    "--slave",
    "-e",
    "IRkernel::main()",
    "--args",
    "{connection_file}"],
  "display_name": "R full",
  "language": "R"
}
```

Something else to keep in mind when building your container is that if you want to use it with jupyterlab you'll need to install an extra packages to do so, IRkernel for R and ipykernel for python.
