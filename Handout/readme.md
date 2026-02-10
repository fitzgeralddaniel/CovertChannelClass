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

**Recommended Dependencies & Installation:**

*   **Python 3 (+ pip):**
    ```bash
    sudo apt-get update
    sudo apt-get install python3 python3-pip
    ```

*   **Scapy:**
    ```bash
    python3 -m pip install scapy
    ```

*   **Wireshark / TShark:**
    ```bash
    sudo apt-get install wireshark tshark
    ```
    *Note: During installation, you may be asked if non-superusers should be able to capture packets. Select 'Yes' to avoid needing sudo for Wireshark.*

*   **Make & GCC (Build Essential):**
    ```bash
    sudo apt-get install build-essential
    ```

*   **Docker:**
    ```bash
    sudo apt-get install docker.io
    # Optional: Add your user to the docker group so you don't need sudo
    sudo usermod -aG docker $USER
    # You may need to log out and back in for this to take effect.
    ```