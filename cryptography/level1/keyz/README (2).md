# Keys

```
While webshells are nice, it'd be nice to be able to login directly. To do so, please add your own public key to ~/.ssh/authorized_keys, using the webshell. Make sure to copy it correctly! The key is in the ssh banner, displayed when you login remotely with ssh, to shell2017.picoctf.com
HINTS
There are plenty of tutorials out there. This one covers key generation: https://confluence.atlassian.com/bitbucketserver/creating-ssh-keys-776639788.html
Then, use the web shell to copy/paste it, and use the appropriate tool to ssh to the server using your key
```

This problem is simply to set up ssh authentication to connect to the ssh server on ```shell2017.picoctf.com```.

First we generate an ssh private/public keypair on our client machine. On linux, we do this with the following linux command.

```
ssh-keygen -t rsa
```

Then we take the contents of the ```id_rsa.pub``` and put them in a file on the ssh server at ```~/.ssh/authorized_keys```. Then we simply connect from our linux box via the ssh command.

```
ssh user@shell2017.picoctf.com
```

If you are on windows, you can use a linux virtual machine, powershell, putty or some other software. If you use putty you will need to generate a .ppk file with puttygen. Then you will need to add the .ppk file as an authentication method in the session configuration. You can find more information on how to this [here](https://www.digitalocean.com/community/tutorials/how-to-use-ssh-keys-with-putty-on-digitalocean-droplets-windows-users).