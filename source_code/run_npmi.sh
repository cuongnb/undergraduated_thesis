#!/usr/bin/env bash
taskset -c 40 python NPMI.py ../dataset/twitter/tweet.txt.sf ../dataset/twitter/models/DropOBTMVB01 &
taskset -c 41 python NPMI.py ../dataset/twitter/tweet.txt.sf ../dataset/twitter/models/DropOBTMVB02 &
taskset -c 42 python NPMI.py ../dataset/twitter/tweet.txt.sf ../dataset/twitter/models/DropOBTMVB03 &
taskset -c 43 python NPMI.py ../dataset/twitter/tweet.txt.sf ../dataset/twitter/models/DropOBTMVB04 &
taskset -c 44 python NPMI.py ../dataset/twitter/tweet.txt.sf ../dataset/twitter/models/DropOBTMVB05 &
taskset -c 45 python NPMI.py ../dataset/twitter/tweet.txt.sf ../dataset/twitter/models/DropOBTMVB06 &
taskset -c 46 python NPMI.py ../dataset/twitter/tweet.txt.sf ../dataset/twitter/models/DropOBTMVB07 &
taskset -c 47 python NPMI.py ../dataset/twitter/tweet.txt.sf ../dataset/twitter/models/DropOBTMVB08 &
taskset -c 48 python NPMI.py ../dataset/twitter/tweet.txt.sf ../dataset/twitter/models/DropOBTMVB09 &
wait