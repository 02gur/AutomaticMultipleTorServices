
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

and use ..
Testing
curl --socks5 127.0.0.1:9050 https://api.myip.com
  {"ip":"107.189.31.33","country":"Unknown","cc":"XX"}
curl --socks5 127.0.0.1:9060 https://api.myip.com
  {"ip":"104.244.73.193","country":"Unknown","cc":"XX"}
</pre>
