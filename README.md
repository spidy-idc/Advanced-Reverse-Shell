# Advanced-Reverse-Shell

This is a very advanced Reverse Shell! It is same as the `HTTP-Reverse-Shell` with new added feature that makes it more powerful and helps it to evade corporate Firewalls
A lot of corporate firewalls have a whitelist of programs that can connect to the internet so when our `malware.exe` executes there the Firewall won't allow it to connect to
web traffic as outgoing web traffic will be whitelisted for only few applications. According to our assumption web traffic privilge will most probably be enabled on Web Browsers

So to evade this type of Firewall, We take help of Microsoft COM Objects that allow us to launch and interact with Microsoft applications like Word, Excel, Internet Explorer programitically from our program
So we'll launch internet explorer from our python script or `malware.exe` in invisible (headless) mode using Win32 COM Python Library and then force our HTTP communications through the browser instead of directly
doing it through our python script

This way the malware will work properly without any issues
