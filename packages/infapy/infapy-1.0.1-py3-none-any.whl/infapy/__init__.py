# Copyright (c) 2021-Present Prashanth Pradeep https://www.linkedin.com/in/prashanth-pradeep/
# All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish, dis-
# tribute, sublicense, and/or sell copies of the Software, and to permit
# persons to whom the Software is furnished to do so, subject to the fol-
# lowing conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABIL-
# ITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT
# SHALL THE AUTHOR BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
#

import requests as re

def connect_cdi(infa_user_name=None, infa_passwd=None, infa_region=None, **kwargs):
    """
    :type infa_org_id: string
    :param infa_org_id: Your Informatica Cloud Org ID
    
    :type infa_user_name: string
    :param infa_user_name: Your Informatica Cloud Username

    :type infa_passwd: string
    :param infa_passwd: Your Informatica Cloud Password
    
    :rtype: :class:`infapy.cdi.connection.CDIConnection`
    :return: A connection to Informatica Cloud CDI
    """
    
    # from infapy.cdi.connection import CDIConnection
    # return CDIConnection(infa_org_id=None, infa_user_name=None, infa_passwd=None, **kwargs)
    url="https://dm-us.informaticacloud.com/saas/public/core/v3/login"
    headers = {'Content-Type': "application/json", 'Accept': "application/json"}
    body={"username": infa_user_name,"password": infa_passwd}

    r = re.post(url=url, json=body, headers=headers)
    data = r.json()
    return data