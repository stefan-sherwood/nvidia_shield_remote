# nvidia_shield_remote
Python class for controlling Nvidia Shield over a network

## Prerequisites
<details>
<summary>
<b><a href="https://www.python.org/downloads/">Python 3.6</a> or higher with <a href="https://github.com/google/python-adb">python-adb</a> installed</b>
</summary>
<br/>
&emsp13;&emsp13;&emsp13; <b>Install Python</b>

&emsp13;&emsp13;&emsp13; Download and install Python from <a href="https://www.python.org/downloads/">here</a>

&emsp13;&emsp13;&emsp13; <b>Install python-adb</b>  
&emsp13;&emsp13;&emsp13; <code>pip install adb</code>
<br/>
</details>

<details>
<summary>
<b>Nvidia Shield in Developer Mode with Network Debugging turned on</b>
</summary>
<br/>
&emsp13;&emsp13;&emsp13; <b>Turn on developer mode</b><br/>
&emsp13;&emsp13;&emsp13; <i>Settings &rarr; About &rarr; Build </i> (click Build 7 times - "You are now a developer" message will pop up)
<br/><br/>

&emsp13;&emsp13;&emsp13; <b>Turn on Network debugging</b><br/>
&emsp13;&emsp13;&emsp13; <i>Settings &rarr; Developer Options &rarr; Network debugging </i>
<br/>
</details>

<details>
<summary>
<b>The DNS name <i>(recommended)</i> or IP address and the debug port of your Nvidia Shield</b>
</summary>

<br/>
&emsp13;&emsp13;&emsp13; <b>Get the DNS name</b><br/>
&emsp13;&emsp13;&emsp13; The DNS name is usually just the <i>Device name</i> of your Shield. Unless you have changed it, it is <i>SHIELD</i>.<br/>
&emsp13;&emsp13;&emsp13; The device name is found at <i>Settings &rarr; About &rarr; Device name</i>
<br/><br/>
&emsp13;&emsp13;&emsp13; <b>Get the IP address and debug port</b><br/>
&emsp13;&emsp13;&emsp13; <i>Settings &rarr; Developer Options &rarr; Network debugging</i>
<br/>
&emsp13;&emsp13;&emsp13; When you select this option the IP address and port will be shown
</details>

## Sample code

```
import nvidia
device = nvidia.shield( 'SHIELD:5555' ) # device name (or IP address) and port
device.press( 'power' ) # turn the Shield on or off
device.press( 'home' ) # press the home button
device.launch( 'hbo' ) # launch HBO Now app
```

## USAGE

There are presently two methods:

<details>
<summary>
<code>press( button )</code>
</summary>
<br/>
&emsp13;&emsp13;&emsp13; Button is one of: <code>power, sleep, wake, home, back, search, up, down, left, right, center, volume up, volume down, rewind, ff, play/pause, previous, next</code>
</details>

<details>
<summary>
<code>launch( app )</code>
</summary>
<br/>
&emsp13;&emsp13;&emsp13;App is one of:

&emsp13;&emsp13;&emsp13;&emsp13;&emsp13;&emsp13; <code>hbo, prime, music, youtube, ted, games</code>
</details>

---
<b>Questions, feedback, bug reports, and feature requests are all welcome.</b>
