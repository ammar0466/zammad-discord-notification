import requests
import json
import time
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
#import .env
import os
#pip install python-dotenv
from dotenv import load_dotenv
load_dotenv()

zammadUrl = os.getenv('ZAMMADURL')
discordUrl = os.getenv('DISCORDHOOK')

#headers for discord
headersD = {'Content-Type': 'application/json'}

ndata = {'username':'Helpdesk','content': 'No Ticket'}



def main():
    #replace with your zammad url
    ZammadNoti = zammadUrl + "/api/v1/online_notifications?expand=true"
    headers = {'Content-Type': 'application/json','Authorization': os.getenv('ZAMMADTOKEN')}
    noti = requests.get(ZammadNoti, headers=headers)

    
    jsonData = json.loads((noti.content).decode('utf-8').replace("'",'"'))
    print (jsonData)
    

    if not jsonData:
        #do nothing, break out of the loop
        print("No new Ticket")
        return

        
        # requests.post(discordUrl, headers=headersD, data=json.dumps(ndata))
        
    else:
        
        link_id = jsonData[0].get('o_id')
        apiTicket = zammadUrl + '/api/v1/tickets/' + str(link_id)
        ticketJson = requests.get(apiTicket, headers=headers)
        ticketJson = json.loads((ticketJson.content).decode('utf-8').replace("'",'"'))
        

        state = ticketJson.get('state_id')
            #if state is 4 , it means ticket is closed, do not send notification, and if 2 also do not send notification
        if state == 4 or state == 2:
            print("Ticket is closed or been opened")
            return

        # global last_ticket_id
        # if link_id == last_ticket_id:
        #     print("Already sent notification for this ticket")
        #     return
        
        # last_ticket_id = link_id


        link = zammadUrl+"/#ticket/zoom/" + str(link_id)


        
        ticketJson = requests.get(apiTicket, headers=headers)
        ticketJson = json.loads((ticketJson.content).decode('utf-8').replace("'",'"'))
        title = ticketJson.get('title')

        #get customer email
        customer = ticketJson.get('customer_id')
        apiUser = zammadUrl+'/api/v1/users/' + str(customer)
        userJson = requests.get(apiUser, headers=headers)
        userJson = json.loads((userJson.content).decode('utf-8').replace("'",'"'))
        customer = userJson.get('email')
        #remove @Anydomain from customer
        customer = customer.split('@')[0]
        

            #if 'seen' is flase
        if jsonData[0].get('seen') == False:
            
            #"created_at": "2022-11-22T03:27:55.548Z"
            #append created_at to data
            # data['content'] = data['content'] + jsonData[0].get('created_at')
            

            data = {'username':'Helpdesk','content': 'New Ticket - ', 'embeds': [{'title': title, 'url': link}]}
            data['content'] = data['content'] + customer
            #add embed ticketer to data
            # data['embeds'] = [{'title': 'New Ticket', 'description': ticketer}]
            print(data)
                        
            requests.post(discordUrl, headers=headersD, data=json.dumps(data))
            print("New Tickets")

        #15/03/2023 
        #dont need this anymore, since we use ticket state to check if ticket is closed or not
        #Just for testing
        # elif jsonData[0].get('seen') == True:
        #     print("Old Tickets")
        #     updata = {'username':'Helpdesk','content': 'Old Ticket -', 'embeds': [{'title': title, 'url': link}]}
        #     #insert also ticketer into content, concatinate into Old Ticket
        #     updata['content'] = updata['content'] + customer
            
        #     #add embed ticketer to data
        #     # updata['embeds'] = [{'title': 'Update Ticket', 'description': ticketer}]
        #     print(updata)
        #     # updata['content'] = updata['content'] + jsonData[0].get('created_at')
        #     requests.post(discordUrl, headers=headersD, data=json.dumps(updata))
            
        # elif jsonData[0].get('type') == 'update':
        #     print("Update Tickets")
        #     updata = {'username':'Helpdesk','content': 'Update Ticket -', 'embeds': [{'title': title, 'url': link}]}
        #     updata['content'] = updata['content'] + customer
            
        #     #add embed ticketer to data
        #     # updata['embeds'] = [{'title': 'Update Ticket', 'description': ticketer}]
        #     print(updata)
        #     # updata['content'] = updata['content'] + jsonData[0].get('created_at')
        #     requests.post(discordUrl, headers=headersD, data=json.dumps(updata))
        # else:
        #     return
  

while True:
    print("checking for new tickets")
    main()
    time.sleep(90) 


