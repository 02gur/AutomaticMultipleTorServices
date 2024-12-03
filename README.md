
# AutomaticMultipleTorServices
Automatic Multi-Tor Proxy Service Generator
<pre>
  
#On Debian/Ubuntu-based systems:
sudo apt update && sudo apt install tor

#On macOS (using Homebrew):
brew install tor


git clone https://github.com/02gur/AutomaticMultipleTorServices.git
cd AutomaticMultipleTorServices
* Start
python3 tor_service.py
1. Create Tor instances 
2. Start Tor instances
3. List ports
example ;
tor3 - SocksPort: 9054
tor9 - SocksPort: 9066
tor4 - SocksPort: 9056
tor7 - SocksPort: 9062
tor5 - SocksPort: 9058
tor8 - SocksPort: 9064
tor2 - SocksPort: 9052
tor10 - SocksPort: 9068
tor6 - SocksPort: 9060
tor1 - SocksPort: 9050

(Do not stop python code)
and use ..
Testing
curl --socks5 127.0.0.1:9050 https://api.myip.com
  {"ip":"107.189.31.33","country":"Unknown","cc":"XX"}
curl --socks5 127.0.0.1:9060 https://api.myip.com
  {"ip":"104.244.73.193","country":"Unknown","cc":"XX"}
</pre>
