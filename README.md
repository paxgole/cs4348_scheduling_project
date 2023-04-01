# README

To run this program:
1. Ensure that you have the lastest python and pip installed
2. Run "**python main.py**" - no additional packages are required so there is no virtual environment

A copy of the output can be written out at each execution to output.txt with the command "**python main.py > output.txt**". The last run from my machine is already there.

## Some observations:

Implementing the algorithms wasn't nearly as difficult after the first one was done (FCFS). The main difference was with the select functions with each and when and how there were called. On my machine, the execution was pretty much instant, even with the hefty 150 values and long performance calculation. (I suppose I have the creators of the actual OS's we use to thank for that efficiency!) I did feel as though there could be some improvements to the algorithms: RR's select function could use some basic priority or ageing rather than simply going down the list. And of course it would've been more efficient with a larger time quantum. The same regarding ageing could be said for SRT, but as with any change like that overhead will increase.

When looking at the output for the algorithms, what shocked me was how very early processes were being starved till the end, and only completed because there hadn't been any new incoming processes in a long, long time. RR doesn't feel very fair in that regard. In that way, SRT and FCFS (despite its own flaws) had early processes complete early rather than being held on pause till almost the end. Even HRRN had a few processes being held longer than felt necessary.