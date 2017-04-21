# Leaf of the Tree

```
We found this annoyingly named directory tree starting at /problems/f8fc794974ad619254d983bc423608c6. It would be pretty lame to type out all of those directory names but maybe there is something in there worth finding? And maybe we dont need to type out all those names...? Follow the trunk, using cat and ls!
HINTS
Tab completion is a wonderful, wonderful thing
```

For this problem you simply need to search the directory and print the contents of the flag file. As of the time i am writing this writeup the file is blank and has been tampered with. You should've been able to get the answer by using the find command and grep and then the cat command on the result. Note the ` ` to evaluate the ```find``` and ```grep``` first and then pass that result to ```cat```.

```
$ cat `find /problems/f8fc794974ad619254d983bc423608c6 | grep flag`
flag should print here
$ 
```