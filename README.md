# aws-signature-iot-python

aws signature generator creates headers for the REST API for AWS-IOT shadows.  It runs on micropython and uses micropython libraries.

Usage:
* GET: <code>micropython awsiot_sign_test.py -a <i>yourAccessKey</i> -k <i>yourSecretKey</i> -e <i>yourEndPointId</i> -s <i>shadowName</i></code>
* POST: <code>micropython awsiot_sign_test.py -a <i>yourAccessKey</i> -k <i>yourSecretKey</i> -e <i>yourEndPointId</i> -s <i>shadowName</i> -m POST -b "{\"state\": {\"reported\": {\"status\":\"test of REST POST\"}}}"</code>

Note: escaped double-quotes have to be used in the body argument; single quotes are not valid JSON.

awsiot-sign.py is intended for an embedded environment (like the ESP) so that REST can be used to get and update AWS-IOT shadows. This an alternative to using MQTT + TLS or a webhook. It does require secure storage of the AWS secret key.

awsiot_sign_test.py provides a command line interface for the awsiot-signing function.

The micropython hmac library (as of this commit) had to be modified to work with binary (vs ASCII) keys.

And the micropython urequest library (as of this commit) had to be modified in order have the GET work: get the content-length from the header and do a socket.read of that content length.

The code has been tested on Mac OS X. The next step is to test on an ESP8266.
