# Puzzlingly Accountable

```
We need to find a password. It's likely that the updated passwords were sent over the network. Let's see if that's true: data.pcap. Update 16:26 EST 1 Apr If you feel that you are close, make a private piazza post with what you have, and an admin will help out. The ones and sevens unfortunately look like each other.
HINTS
How does an image end up on your computer? What type of packets are involved?
```

I found the GETS that go to /secret/xxxxxxxxx in wireshark, yielding two results.  For each of these I followed the TCP Stream, and saved the data as raw, then deleted everything up until the PNG header in a hex editor, saved as a PNG, and opened.  I then proceeded to make a Piazza post because I couldn't tell the difference between the 1s and 7s in the final image.


[data.pcap](https://webshell2017.picoctf.com/static/5f7b893f22f274c7298cb7be4d36eed8/data.pcap)


We found the GETS that go to /secret/xxxxxxxxx in wireshark, yielding two results. For each of these results, we followed the TCP stream, and saved the data as raw. Then we deleted everything up until the PNG header in a hex editor, saved as a PNG, and opened. We had difficulty distinguishing 7's from 1's in the final image but the instructors on the Piazza Forum were happy to help us figure that out.


Final images:

![1](1.png)

![2](2.png)

```
flag: 60967a1aff716c1d7369fdf95bce0a30
```
