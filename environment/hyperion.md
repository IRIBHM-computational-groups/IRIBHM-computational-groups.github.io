---
description: >-
  Welcome to the heart of our lab's digital ecosystem! In this section, we'll
  describe the essential components of our computing environment.
---

# 💻 Hyperion

<details>

<summary>What is Hyperion ? </summary>

Hyperion is an HPC cluster( High Performance Computing). A cluster is a network of connected computers, working together to tackle complex tasks. It's like a digital powerhouse that amplifies our ability to process data and run computationally intensive simulations.

</details>

<details>

<summary>How to connect to Hyperion?</summary>



Our cluster comprises five distinct servers, each with its own set of capabilities:

1.  **Himm Server:**

    * Packed with numerous CPUs, the Himm server is a computational powerhouse, although it doesn't house GPUs. Ideal for CPU-intensive tasks, this server awaits your commands.

    URL command line : iribhm-himm01.hpda.ulb.ac.be\
    Jupyter Lab adress : [http://iribhm-himm01.hpda.ulb.ac.be:8000/jupyter/hub/login](http://iribhm-himm01.hpda.ulb.ac.be:8000/jupyter/hub/login)\

2.  **GPU01 Server:**

    * Equipped with both CPUs and GPUs, GPU01 is your go-to for tasks that demand the parallel processing might of graphical processing units.&#x20;

    URL command line : iribhm-gpu01.hpda.ulb.ac.be\
    Jupyter Lab adress : [http://so-iribhm-gpu01.hpda.ulb.ac.be:8000/jupyter/hub/login](http://so-iribhm-gpu01.hpda.ulb.ac.be:8000/jupyter/hub/login)\

3.  **GPU02 Server:**

    * Similar to GPU01, this server boasts a combination of CPUs and GPUs, providing you with additional resources for parallel computing.&#x20;

    URL command line : iribhm-gpu02.hpda.ulb.ac.be\
    Jupyter Lab adress : [http://iribhm-gpu02.hpda.ulb.ac.be:8000/jupyter/hub/login](http://iribhm-gpu02.hpda.ulb.ac.be:8000/jupyter/hub/login)\

4.  **GPU03 Server:**

    * Another hub for combined CPU and GPU capabilities.

    URL command line : iribhm-gpu03.hpda.ulb.ac.be\
    Jupyter Lab adress : [https://iribhm-gpu03.hpda.ulb.ac.be:8000/jupyter/hub/login](https://iribhm-gpu03.hpda.ulb.ac.be:8000/jupyter/hub/login)\

5.  **Builder Server:**

    * Dedicated to the construction of containers (a topic we'll delve into in the next sections), the Builder server plays a crucial role in crafting environments tailored to your specific needs.

    URL command line : iribhm-builder.hpda.ulb.ac.be\
    Jupyter Lab adress : [https://iribhm-builder.hpda.ulb.ac.be:8000/jupyter/hub/login ](https://iribhm-gpu03.hpda.ulb.ac.be:8000/jupyter/hub/login)\


To connect in one of these server, first of all, you will need to connect to the ulb VPN Global Protect, connection steps are taken in [https://support.ulb.be/fr/web/support/-/comment-utiliser-ulb-vpn-](https://support.ulb.be/fr/web/support/-/comment-utiliser-ulb-vpn-)

Next, once connected to the VPN, different options are opened to you. Either, you connect through your basic command line interface.&#x20;

```bash
user:~$ ssh ulbid@<url>
```

your ulbid is the same used to connect to the "Virtual University".&#x20;

Next, depending on which server you want to connect, different urls can be used. These are taken in the bullet section under the corresponding server.



The second option, is to connect throught the jupyter lab interface. Therefore, just paste the link provided in your browser and connect with your ulb creditentials.

</details>

