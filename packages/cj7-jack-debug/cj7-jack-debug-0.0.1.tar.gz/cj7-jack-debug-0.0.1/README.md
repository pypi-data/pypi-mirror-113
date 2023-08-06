# cj7

A simple way to send TCP and UDP packets in Python without the need for sockets.

### Examples

Sending packets in UDP `sendPacketUDP(ip, port, data, showSent)`
Put the target IP as the first variable, the target port as the second, the data to be sent in the third and either True or False in the last variable for whether or not to print a message when the packet has been sent.

Sending packets in TCP `sendPackettcp(ip, port, data, showSent)`
Put the target IP as the first variable, the target port as the second, the data to be sent in the third
and either True or False in the last variable for whether or not to print a message when the packet has b
een sent.

