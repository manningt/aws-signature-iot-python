#!/usr/local/bin/micropython
# AWS Version 4 signing tester: makes requests to AWS-IOT based on command line args


import sys, os
import argparse
from time import gmtime
#import utime
import urequests

import awsiot_sign


def main(argv=None):
    if argv is None:
        argv = sys.argv

    parser = argparse.ArgumentParser(description='AWS IOT REST IO')
    parser.add_argument('-k','--secret_key', required=True)
    parser.add_argument('-a','--access_key', required=True)
    parser.add_argument('-e','--endpt_prefix', required=True)
    parser.add_argument('-s','--shadow_id', required=True)
    parser.add_argument('-m','--method', help='method: GET/POST', choices=['GET', 'POST'], default='GET')
    parser.add_argument('-r','--region', help='AWS region; eg us-west-1', default='us-east-1')
    parser.add_argument('-b','--body', help='shadow state, in json format', default='')
    parser.add_argument('-d','--do_request', help='set to False to disable sending request to AWS: True/False', type=bool, default=True)
    args = parser.parse_args()

    # Create a date for headers and the credential string
    #    the following doesn't work in micropython & utime doesn't support gmtime()
    #    amzdate = time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())
    # so using gmtime and then doing a format
    t = gmtime()
    # Date w/o time, used in credential scope
    datestamp = '{0}{1:02d}{2:02d}'.format(t[0],t[1],t[2])
    #datestamp = utime.strftime('%Y%m%d')

    DUMMY_TOD_FOR_AMZDATE = False
    if (DUMMY_TOD_FOR_AMZDATE == True):
        time_now_utc = "T12:34:56Z"
    else:
        time_now_utc = 'T{0:02d}{1:02d}{2:02d}Z'.format(t[3],t[4],t[5])
    amzdate = datestamp + time_now_utc

    request_dict = awsiot_sign.request_gen(args.endpt_prefix, args.shadow_id, args.access_key, args.secret_key, amzdate, method=args.method, region=args.region, body=args.body)

    endpoint = 'https://' + request_dict["host"] + request_dict["uri"]

    if (args.do_request == True):
        print('\nBEGIN REQUEST++++++++++++++++++++++++++++++++++++')
        print('Request URL = ' + endpoint)
        if (args.method == 'GET'):
            r = urequests.get(endpoint, headers=request_dict["headers"])
        else:
            r = urequests.post(endpoint, headers=request_dict["headers"], data=args.body)
        
        print('\nRESPONSE++++++++++++++++++++++++++++++++++++')
        print('Response code: %d\n' % r.status_code)
        #print(r.reason)
        #print(r.headers)
        print(r.json())

if __name__ == "__main__":
     sys.exit(main())
