---
description: 'Good computational practices : working efficiently and reproducibly'
---

# ✅ GCP's

When working in bioinformatics wrong practices can make you lose time, make other lose time or confidence in your work, or even lead to disaster. To avoid these you must adopt good habits that include making backups, versioning your code and adopting a coding style that will make it more readable for others ... or even yourself when you have to read it again a few months later.

## Backups

The most obvious error leading to disaster is forgetting about backups.

Please make backups.

Please make backups.

The obvious candidate to backup your code is git versioning because it offers several other advantages. This is described below. To backup your other files feel free to use any combination of method(s) that best suits your needs and preferences, e.g. :

* The ULB provides 1TB of Onedrive storage and 20GB of Owncloud storage
* Personal cloud storage
* Manual backups on external disks
* ...

The IRIBHM mount directory is protected against hardware failure but not human errors. If you rm a file there is no trash to get it back from afterwards. You can create an alias for your rm command to make it ask for confirmation by default with the -i argument if you wish.

## Git versioning

### Why using git ?

Regular backup methods are not the most efficient way to handle your code. For instance the iterative development of your code might make you think that method B is better than method A. If you do not delete the code related to method A your code might become unreadable over time. But if you do delete it you might realize later that method A was actually better for a reason you couldn't envision early on. Without code versioning deleted segments of code are lost and you'll have to do the work twice. With code versioning you can just go back to the commit containing method A and carry on.

On top of code versioning, using github will also allow you to share your code and collaborate on shared projects with the rest of the team seamlessly. The commit/backup process can be automated if you wish and pushing to the team's github constitutes an effective form of cloud backups.

### What is git ?

Git is an open source software of distributed version control. It allows to track changes and variants of your code and synchronize it between different directories, called repositories. It is the most widely used software for version control and it can be freely used and modified by anyone on any machine, whether it is a local machine or a cloud server.

Here is the git project's web page : [https://git-scm.com/](https://git-scm.com/)

It is very often used with a cloud-based storage that serve as a central point to share the modifications across machines. One of the most popular hosting solution is github, and it is the solution chosen by the team. Github allows you to create an account and credentials to access and store your code safely, to create groups (called organizations) to share code between multiple user accounts, and to consult your code or any public code on their website.

Here is github's web page : [https://github.com/](https://github.com/)

### How to use git ?

To use it properly the best is to follow one of the basics tutorials, e.g. : [https://git-scm.com/doc](https://git-scm.com/doc)

Please find [here ](https://learngitbranching.js.org/?locale=fr\_FR)a little game to learn more about git.

Git is already installed on the hyperion VMs, so all you have to do is configure your profile, configure your repos (if they are not already configured by someone else), and follow this sequence to share your modifications :&#x20;

1. git add
2. git commit
3. git push

Checkout the tips & tricks sections for example ways to automate this process.

If you want to share a repository with the team when you set it up all you have to do is to point it towards the group's github page instead of your own. When working with github the preferred authentication method are ssh keys, and github has a tutorial explaining how to set them up : [https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)

When you want to pull or push don't forget that the way you write the repo's address implies the way you want to connect to it. If you want to use ssh you need to copy-paste the ssh-dedicated address, e.g. : git@github.com:IRIBHM-computational-groups/container-definition-files.git

## Coding style

Coding styles are a way to format your code so that it is easily readable and understandable both by others ... and yourself down the line. It consists of some very simple rules on the way a variable/function/constant should be named, how the code should be commented, etc. To benefit the most from it, the ideal would be for the whole team to adopt the same coding styles in order to maximize the code's readability by the team as a whole.

Here is the coding style that was adopted for R :

[http://web.stanford.edu/class/cs109l/unrestricted/resources/google-style.html](http://web.stanford.edu/class/cs109l/unrestricted/resources/google-style.html)
