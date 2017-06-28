# aws-signature-iot-python

aws signature generator creates headers for the REST API for AWS-IOT shadows.  It runs on micropython and uses micropython libraries.

Usage:
* GET: <code>micropython awsiot_sign_test.py -a <i>yourAccessKey</i> -k <i>yourSecretKey</i> -e <i>yourEndPointId</i> -s <i>shadowName</i></code>
* POST: <code>micropython awsiot_sign_test.py -a <i>yourAccessKey</i> -k <i>yourSecretKey</i> -e <i>yourEndPointId</i> -s <i>shadowName</i> -m POST -b "{\"state\": {\"reported\": {\"status\":\"test of REST POST\"}}}"</code>

Note: escaped double-quotes have to be used in the body argument; single quotes are not valid JSON.

awsiot-sign.py is intended for an embedded environment (like the ESP) so that REST can be used to get and update AWS-IOT shadows. This an alternative to using MQTT + TLS or a webhook. It does require secure storage of the AWS secret key.

awsiot_sign_test.py provides a command line interface for the awsiot-signing function.

A simplified/limited hmac module which uses a subset of the hash lib is provided (the one in micropython-lib didn't handle binary keys).

Also the micropython urequest library (as of this commit) had to be modified in order have the GET work: get the content-length from the header and do a socket.read of that content length.

The code has been tested on Mac OS X, ESP8266 and ESP32 using micropython 1.8.7 and 1.9.
