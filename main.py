
from fastapi import FastAPI,Response
from pydantic import BaseModel
import requests
import json
import re
from dicttoxml import dicttoxml


class RequestsData(BaseModel):
    address: str
    output_format:str

app = FastAPI()

@app.post("/getAddressDetails/")
async def coordinates(data: RequestsData):

    address_list=re.findall(r"[\w']+", data.address) 
    # Covert address into list using regex

    addres_string='+'.join(address_list) 
    # Join the list with '+' in between (eg: 3582+13+G+Main+Road)

    url="https://maps.googleapis.com/maps/api/geocode/json?address=" 

    api_key="" 
    # Your api Key

    final_url=url+addres_string+'&key='+api_key 

    respons=requests.request("GET", final_url) 
    
    json_result=respons.json() 
    # Convert result to json

    if json_result['status']=='OK':
        response_dict={} 

        response_dict['coordinates']=json_result["results"][0]["geometry"]["location"] 
        # Fetching location from json
        
        response_dict['address']=data.address 

        if data.output_format == 'json': 
            # Excute if output fomat is Json

            response_json=json.dumps(response_dict,indent=4) 
            # Convert Dictionary to json

            return Response(content=response_json) 
            # Sending Json response


        elif data.output_format == 'xml': 
            # Execute if output format is xml

            xml_reposne = dicttoxml(response_dict, custom_root='test', attr_type=False) 
            # Convert Dictionary to xml

            return Response(content=xml_reposne,media_type="application/xml") 
            # Sending xml response
    
        else:
            return {"Error: Invalid Output Format."} 
            # Send error if invaid output format
    else:
        return {"Error: Unable to locate"}