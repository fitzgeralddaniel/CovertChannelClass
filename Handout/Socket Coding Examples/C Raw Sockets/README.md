# C Raw Socket Programming Example

You will need to run each of these in a separate terminal

This is very similar to the regular c one, but needs to be run with sudo due to it using raw sockets.

Make sure to run the receiver first, it should hang when it is running correctly and wait for you to run the sender.

To compile and run receiver.c:

```bash
sudo gcc -o receiver receiver.c
sudo ./receiver
```

To compile and run sender.c:

```bash
sudo gcc -o sender sender.c
sudo ./sender
```

To just run:

```bash
./receiver
./sender
```
