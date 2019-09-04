import logging
import requests
import json
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    url=r'''https://taqm.epa.gov.tw/taqm/aqs.ashx?act=WebCamBox&lang=tw'''
    r = requests.get(url)
    rr = r.json()['Data']
    req_body = req.get_json()
    siteid = req_body.get('siteid')
    print('-'*10)
    print(siteid)
    response = {}
    for i in rr:
        if siteid == i['SiteId']:
            try:
                response['place'] = i['SiteText'].split(' (AQI=')[0]
                response['aqi'] = i['SiteText'].split(' (AQI=')[1]
            except:
                response['place'] = i['SiteText'].split(' (')[0]
                response['aqi'] = i['SiteText'].split(' (')[1].replace(')','')                
    return func.HttpResponse(json.dumps(response))
    # name = req.params.get('name')
    # if not name:
    #     print('A')
    #     try:
    #         print('B')
    #         req_body = req.get_json()
    #     except ValueError:
    #         print('C')
    #         pass
    #     else:
    #         print('D')
    #         name = req_body.get('name')

    # if name:
    #     return func.HttpResponse(f"Hello {name}!")
    # else:
    #     return func.HttpResponse(
    #          "Please pass a name on the query string or in the request body",
    #          status_code=400
    #     )
