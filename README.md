**[UNDER DEVELOPMENT CURRENTLY!!]**

>> **Tasks** 
- better error handling 
- broadcasting all at once
- broadcasting between all peers not only server-client
- handling I/O, better interface



# X-Hall
X-Hall is a CLI-based Chatroom program hosted on Internal IIT Delhi Network

# How to Setup your own server
- Clone the repo on the device you want to host the server on
- Use the following commands

```
git clone https://github.com/Madhav-MKNC/X-Hall.git
cd X-Hall
pip install -r requirements.txt
```

- Now run the Server Program and Host it on the network
```
python server.py
```
or 
```
python3 server.py
```
 
- Do not forget to update Host IP and Port in the Client program
- Now users can run the Client program and join the Server
