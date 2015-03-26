# udp-forward

udp-forward is a simple program for hiding the contents of certain UDP
messages. The program simply listens to a UDP port, encrypts the
datagrams and forwards them to the specified port.

The encryption scheme used is by no means cryptographically strong. It
is simply intended to hide the contents from unintelligent
spoofers/sniffers.

# DNS Forwarding

One intention of udp-forward is hiding DNS messages from DNS
spoofers. You can run udp-forward in a remote server by running
`./udp-forward.py 0.0.0.0:5353 8.8.8.8:53`. This starts listening to
port 5353, runs the encryption scheme on whatever it receives and
forwards the results to 8.8.8.8:53 (Google's public DNS server). The
reply is also encrypted when received and forwarded back.

You then need to run `sudo ./udp-forward.py 127.0.0.1:53
remote-server:5353` on your local machine. The encryption scheme, when
run twice, results in the original message, so this effectively
forwards your DNS queries to Google's public DNS server.

You can run the local instance of udp-forward on your home server and
then setup your home DHCP server to return the home server as the
local DNS server.
