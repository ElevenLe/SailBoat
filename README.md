# Seeet
Seeet is web application developed using Kismet, python and Flask. Seeet shows population in the one area
## Website
please visit
http://howfull.us-west-2.elasticbeanstalk.com/
## Building
[build.md](/build.md) 
## Seeet finds area population
Using kismet, we are able to see the wifi packages flow between clinets and 
Access Points(APs). Ususally, in the home or library, one AP is responsed all 
devices in that area. By measuring the numbers macs, which is unique while 
connected to target AP, we are able to know how many devices is active in this
area, and then devided the number of devices by 2, the Seeet knows approximate
population in this area. [Finds more information here](/info/kis_info.md)
## Kismet find the wifi packages
WiFi layer packages shows mac address and other basic information publicly in
order to let router to transfer the packages. Seeets only use the public information,
and commit that will never decrypt the encrypt data.
## Architecture
Frontend: HTML, javaScript

Server: Flask

Backend: Kismet, python, sqlite3, Flask

While analysing the packages from database gernated by Kismet, backend sends data
to the Server. Then Server show the population to the front end by color.
## Limitations and Missing
The original goal for Seeet is show the population in the library to help students
find seats easier. By depoling kismet in a raspberry Pi and send data from it, server
is able to know the population density of the library, and recommand people to go
to free area. However, due to covid-19, the school is close and everything online.
This means we cannot go to library and set up or experimenting. Thus, Seeet currently
will depoly locally and only show the population at home

The difference between home and library is that the population density. In library, there
could be 50-100 person in one area, which is under one AP. However, there is only 1-5 people
in home. In fact, due to delay from kismet and analysis process, the error is between 1-3 people. Meanwhile,
people in the library have higher chances using two devices, where in home, it really depend on situation. 
In conclution, Seeet to home is not high accuracy, where not applies to library.

## Seeet in future
1. Communicating with library and getting permit to use raspberry pie
2. Imporving the analysis algorithm to increase the accuracy no matter in home or library
3. Update the frontend to have better look interface and support library
4. Detecing the AP in the library to generate area algorithm

## External Resources
* **Kismet**: tools for wifi packages analysis

## Contributors
* Zhengyi Li (zl1499@nyu.edu)
* Christopher Verch （cv932@nyu.edu）
* Rachel （qw724@nyu.edu）
* James
