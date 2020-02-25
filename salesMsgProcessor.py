# Pull sales messages from container
from time import sleep
import json
import sys

## recordMsg - TO STORE ALL MESSAGES
## products - TO STORE ALL THE PRODUCT TYPES
## logAdjustments- TO STORE ONLY THE ADJUSTMENT MESSAGES
recordMsg = []
products  = []
logAdjustments = []

def recordingMsg(msg):
    ## RECORDING OF MESSAGES::
    msg = msg.replace("'", "\"")
    ## CONVERT THE JSON STRING MESSAGE INTO DICTIONARY FORMAT
    msgDict = json.loads(msg)
    recordMsg.append(msgDict)
    products.append(msgDict['prod_type'])
    ## CHECK IF THE MESSAGE TYPE IS ADUSTMENT
    ## IF YES APLLY THE OPERATION TO ALL SALE OF THAT PRODUCT TYPE
    if msgDict.get('adjustment'):
        adjusttment = msgDict['adjustment'].lower()
        if adjusttment == 'add':
            for updateSale in recordMsg:
                if updateSale['prod_type'] == msgDict['prod_type'] and updateSale.get('adjustment','None') == 'None':
                    updateSale['value_in_pence'] = updateSale['value_in_pence'] + msgDict['value_in_pence']

        if adjusttment == 'sub':
            for updateSale in recordMsg:
                if updateSale['prod_type'] == msgDict['prod_type'] and updateSale.get('adjustment','None') == 'None':
                    updateSale['value_in_pence'] = updateSale['value_in_pence'] - msgDict['value_in_pence']

        if adjusttment == 'mul':
            for updateSale in recordMsg:
                if updateSale['prod_type'] == msgDict['prod_type'] and updateSale.get('adjustment','None') == 'None':
                    updateSale['value_in_pence'] = updateSale['value_in_pence'] * msgDict['value_in_pence']

        ## RECORD ADJUSTMENTS MESSAGES
        logAdjustments.append(msgDict)

with open(r"..\salesMessages.txt","r") as f:
    i = 1
    msg_no = 1
    msg_idx_10 = 0
    msg_idx_50 = 0
    while i == 1:
        msg = f.readline()
        if (msg):
            recordingMsg(msg)
            msg_idx_10_diff = msg_no - msg_idx_10
            msg_idx_50_diff = msg_no - msg_idx_50
            if msg_idx_10_diff == 10:
                ## WE HAVE RECEIVED 10 MESSAGES BY PULLING,
                ## INCREASING THE msg_idx_10 by 10 POSITIONS AND GENERATE REPORT
                msg_idx_10 += 10
                ## IDENTIFYING THE UNIQUE PRODUCTS
                products = list(dict.fromkeys(products))
                ## GENERATE REPORT IN PROGRESS
                ## INITIALIZING gen10Report WITH UNIQUE PRODUCTS SALE AND VALUE IN PENCE
                gen10Report = {}
                for p in products:
                    gen10Report[p] = {'sale' : 0,'value_in_pence' : 0}
                for valueSale in recordMsg:
                    if valueSale.get('adjustment', 'None') == 'None':
                        if valueSale.get('no_of_count', 'None') == 'None':
                            valueSale['no_of_count'] = 1
                        gen10Report[valueSale['prod_type']]['value_in_pence'] =  gen10Report[valueSale[
                                'prod_type']]['value_in_pence'] + (valueSale['value_in_pence']) * (valueSale['no_of_count'])

                        gen10Report[valueSale['prod_type']]['sale'] = gen10Report[valueSale['prod_type']][
                                'sale'] + (valueSale['no_of_count'])

                print('=========Report detailing[every 10msgs] the number of sales of each product and their total '
                      'value==========')
                for logGen10Report in gen10Report:
                    print("Product Type : %s, Sale : %s, Total Value(Pence): %s" % (logGen10Report, gen10Report[
                        logGen10Report]['sale'], gen10Report[logGen10Report]['value_in_pence']))

            if msg_idx_50_diff == 50:
                ## WE HAVE RECEIVED 50 MESSAGES BY PULLING
                ## INCREASING THE msg_idx_50 by 50 POSITIONS AND GENERATE REPORT
                msg_idx_50 += 50
                ## GENERATE ADJUSTMENT REPORTS
                print('==========================================')
                print('REPORT DETAILING THE ADJUSTMENTS MESSAGES')
                print('==========================================')
                print("HANG ON--GENERATING ADJUSTMENTS REPORT")
                for adjustmentValues in logAdjustments:
                    print(adjustmentValues)

                ## CHOICE OF USER TO PROCEED OR NOT TO
                while i == 1:
                    print("Do you want to precess more messages ? ::[Y / N]")
                    choice1 = input("Enter your choice :: ")
                    if choice1.upper() == "N":
                        print("Do you want to exit the application ? ::[Y / N]")
                        choice2 = input("Enter your choice :: ")
                        if choice2.upper() == "N":
                            print("SLEEPING FOR 10 SECONDS")
                            sleep(10)
                        else:
                            print("EXITING THE APPLICATION")
                            sys.exit()
                    else:
                        break
            msg_no += 1
        else:
            print("EOF - NO MORE MESSAGES")
            f.close()
            break
