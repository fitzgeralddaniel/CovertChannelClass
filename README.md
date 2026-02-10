# Covert Channel Class

**Course Description:** Intro to covert channels class taught for the AFRL Advanced Course in Engineering (ACE) internship. It is largely based on Professor Steffen Wendzel's work you can find here: [website](https://www.wendzel.de/) and [github](https://github.com/cdpxe).

**Learning Objectives:** Upon completion of this course, future leaders will be able to:

* Identify and analyze common network protocols.
* Understand the different types of covert channels.
* Detect and analyze covert channels in network traffic.
* Create their own covert channels.

**Prerequisites:**

* Basic understanding of networking protocols (TCP/IP, HTTP, DNS).
* Wireshark and your preferred IDE installed.
* Familiarity with Python and/or C programming.

**Course Content:**

* Introduction to Covert Channels
* Networking Review
* Wireshark Review
* Types of Covert Channels
* Evaluating Covert Channels
* Detection
* Cobalt Strike Integration Example
* Hands-on Exercises

**Tools:**

* Wireshark
* Python


**Assignments:**

* Future leaders will complete a series of hands-on exercises to reinforce concepts during lecture.
* Future leaders will develop their own covert channel for their weekly assignment.

## Getting Started

To make it easy to run the examples and exercises, we have provided a Docker environment and a Makefile.

### Prerequisites

* Docker installed on your machine.

### Building the Environment

1.  Build the Docker image:
    ```bash
    docker build -t covert-channel .
    ```

### Running the Environment

The container needs raw socket permissions to run the examples. You can run it with the `--cap-add=NET_RAW` flag.

1.  Start the container:
    ```bash
    docker run --cap-add=NET_RAW -it -v $(pwd):/app covert-channel bash
    ```
    *   `-v $(pwd):/app`: Mounts your current directory to `/app` inside the container, so you can edit files on your host and run them in the container.
    *   `--cap-add=NET_RAW`: Grants permission to use raw sockets.

### Compiling Code

Once inside the container (or on your local machine if you have dependencies installed), you can verify and compile all C examples using the master Makefile:

```bash
make all
```

To clean up compiled binaries:

```bash
make clean
```