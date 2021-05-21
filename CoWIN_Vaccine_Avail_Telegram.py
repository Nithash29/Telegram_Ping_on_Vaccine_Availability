import pandas as pd
import datetime
import json
import openpyxl
import requests
import os
from fake_useragent import UserAgent

# State ID. Check "State_ID_Mapping.csv" to get the mapping of state id and name.
state_code = 33 #Tripura

# Age of the person to be checked
age = 28

# Number of days ahead of checking availability
numdays = 4

temp_user_agent = UserAgent()
browser_header = {'User-Agent': temp_user_agent.random}

# Getting the district name and their corresponding IDs
dist_IDs = []
dist_Name = []
print(f"Entered State code is: {state_code}")
df_state_id = pd.read_csv("State_ID_Mapping.csv")
state_name = df_state_id[df_state_id["state_id"]==state_code]["state_name"].to_list()[0]
print(f"The corresponding State name is: {state_name}")
response = requests.get("https://cdn-api.co-vin.in/api/v2/admin/location/districts/{}".format(state_code),
                        headers=browser_header)
json_data = json.loads(response.text)
for i in json_data["districts"]:
    dist_IDs.append(i["district_id"])
    dist_Name.append(i["district_name"])

#print("District IDs of the State: ", dist_IDs)
#print("District Names of the State: ", dist_Name)

base = datetime.datetime.today()
date_list = [base + datetime.timedelta(days=x) for x in range(numdays)]
date_str = [x.strftime("%d-%m-%Y") for x in date_list]

# Master dataframe for availability list across all regions
cols = ["Date", "District_ID", "District_Name", "Center_Name", "Slots_Available", "Dose1_Availability", "Dose2_Availability",
        "Min_Age_Limit", "Fee", "Vaccine_Name", "Address", "Pincode"]
df_avail = pd.DataFrame(columns = cols)

date_list = []
dist_ID_list = []
dist_nm_list = []
center_nm_list = []
avail_list = []
d1_avail = []
d2_avail = []
age_list = []
fee_list = []
vaccine_list = []
address_list = []
pincode_list = []

# Getting the available slots
for INP_DATE in date_str:
    for ind, DIST_ID in enumerate(dist_IDs):
        URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={}&date={}".format(DIST_ID, INP_DATE)
        response = requests.get(URL, headers=browser_header)
        print(DIST_ID, INP_DATE)
        temp_centre = []
        if response.ok:
            resp_json = response.json()
            if resp_json["centers"]:
                for center in resp_json["centers"]:
                    for session in center["sessions"]:
                        if session["min_age_limit"] <= age and session["available_capacity"]!=0:
                            if center["name"] not in temp_centre:
                                date_list.append(INP_DATE)
                                dist_ID_list.append(DIST_ID)
                                dist_nm_list.append(dist_Name[ind])
                                temp_centre.append(center["name"])
                                avail_list.append(session["available_capacity"])
                                d1_avail.append(session["available_capacity_dose1"])
                                d2_avail.append(session["available_capacity_dose2"])
                                age_list.append(session["min_age_limit"])
                                fee_list.append(center["fee_type"])
                                address_list.append(center["address"])
                                pincode_list.append(center["pincode"])
                                if(session["vaccine"] != ''):
                                    vaccine_list.append(session["vaccine"])
                                else:
                                    vaccine_list.append("NA")
                        else:
                            print("\t Availability is of different age group or there is no available stock")
                            print("\t Minimum Age Limit: ", session["min_age_limit"])
                            print("\t Available Capacity: ", session["available_capacity"])

            else:
                print("No available slots on {}".format(INP_DATE))

            if len(temp_centre) != 0:
                for cnt in temp_centre:
                    center_nm_list.append(cnt)

        else:
            print("Invalid response code")

df_avail["Date"] = date_list
df_avail["District_ID"] = dist_ID_list
df_avail["District_Name"] = dist_nm_list
df_avail["Center_Name"] = center_nm_list
df_avail["Slots_Available"] = avail_list
df_avail["Dose1_Availability"] = d1_avail
df_avail["Dose2_Availability"] = d2_avail
df_avail["Min_Age_Limit"] = age_list
df_avail["Fee"] = fee_list
df_avail["Vaccine_Name"] = vaccine_list
df_avail["Address"] = address_list
df_avail["Pincode"] = pincode_list


# df_Overview = pd.DataFrame(columns=["Date", "District_Name", "Available_Center_Count", 
#                                     "Dose1_Slots", "Dose2_Slots", "Age_Group"])

df_Overview = pd.DataFrame(columns=["Date", "District_Name", "Available_Center_Count", "Dose1_Center", "Dose2_Center",
                                    "Dose1_Slots", "Dose2_Slots", "Age_Group"])

# Overview sheet generation
date_app = []
place = []
center_count = []
# total_avail = []
d1_slt = []
d2_slt = []
d1_ctr = []
d2_ctr = []
df_list = []
df_list.append(df_Overview)
dst_list = []
for item in dist_Name:
    df_temp = pd.DataFrame()
    df_temp = df_avail[df_avail["District_Name"] == item]
    if df_temp.shape[0] == 0:
        for dt in date_str:
            date_app.append(dt)
            place.append(item)
            center_count.append(0)
#             total_avail.append(0)
            d1_slt.append(0)
            d2_slt.append(0)
            d1_ctr.append(0)
            d2_ctr.append(0)
    else:
        df_list.append(df_temp)
        dst_list.append(item)
        for dt in date_str:
            date_app.append(dt)
            place.append(item)
            df_temp2 = df_temp[df_temp["Date"] == dt]
            if df_temp2.shape[0] == 0:
                center_count.append(0)
#                 total_avail.append(0)
                d1_slt.append(0)
                d2_slt.append(0)
                d1_ctr.append(0)
                d2_ctr.append(0)
            else:
                cnt_lst = df_temp2["Center_Name"].to_list()
                center_count.append(len(cnt_lst))
#                 slot_cnt = df_temp2["Slots_Available"].to_list()
#                 total_avail.append(sum(slot_cnt))
                d1_slot_cnt = df_temp2["Dose1_Availability"].to_list()
                d1_slt.append(sum(d1_slot_cnt))
                d2_slot_cnt = df_temp2["Dose2_Availability"].to_list()
                d2_slt.append(sum(d2_slot_cnt))
                d1_ctr_cnt = 0
                d2_ctr_cnt = 0
                for l in range(len(cnt_lst)):
                    if d1_slot_cnt[l] != 0 and d2_slot_cnt[l] == 0:
                        d1_ctr_cnt += 1
                    elif d1_slot_cnt[l] == 0 and d2_slot_cnt[l] != 0:
                        d2_ctr_cnt += 1
                    elif d1_slot_cnt[l] != 0 and d2_slot_cnt[l] != 0:
                        d1_ctr_cnt += 1
                        d2_ctr_cnt += 1
                d1_ctr.append(d1_ctr_cnt)
                d2_ctr.append(d2_ctr_cnt)

df_Overview["Date"] = date_app
df_Overview["District_Name"] = place
df_Overview["Available_Center_Count"] = center_count
#df_Overview["Slots_Available"] = total_avail
df_Overview["Dose1_Center"] = d1_ctr
df_Overview["Dose2_Center"] = d2_ctr
df_Overview["Dose1_Slots"] = d1_slt
df_Overview["Dose2_Slots"] = d2_slt
df_Overview["Age_Group"] = ['18+']*len(date_app)

df_previous = pd.read_excel("Update_Overview.xlsx")
same_flag = df_Overview.equals(df_previous)
df_Overview.to_excel("Update_Overview.xlsx", index=False)

text = "Vaccine Availability Update For 4 days \n\n"
for dt in date_str:
    count = 0
    text += "Date---> " + dt + "\n"
    dfx_temp1 = df_Overview[df_Overview["Date"] == dt]
    #print(dfx_temp1)
    dfx_dst = []
    dfx_centre = []
    dfx_d1_centre = []
    dfx_d2_centre = []
    dfx_slots = []
    dfx_dst = dfx_temp1["District_Name"].to_list()
    dfx_centre = dfx_temp1["Available_Center_Count"].to_list()
    dfx_d1_centre = dfx_temp1["Dose1_Center"].to_list()
    dfx_d2_centre = dfx_temp1["Dose2_Center"].to_list()
    dfx_d1_slots = dfx_temp1["Dose1_Slots"].to_list()
    dfx_d2_slots = dfx_temp1["Dose2_Slots"].to_list()
    for i in range(len(dfx_dst)):
        if dfx_centre[i] == 0:
            count += 1
            #text += dfx_dst[i] + ": No Avalability \n"
        else:
            text += dfx_dst[i] + ": "
            if dfx_d1_centre[i] != 0 and dfx_d2_centre[i] == 0:
                text += "[" + str(dfx_d1_slots[i]) + "] Dose-1 slots available across " + str(dfx_d1_centre[i]) + " centers\n"
            elif dfx_d1_centre[i] == 0 and dfx_d2_centre[i] != 0:
                text += "[" + str(dfx_d2_slots[i]) + "] Dose-2 slots available across " + str(dfx_d2_centre[i]) + " centers\n"
            elif dfx_d1_centre[i] != 0 and dfx_d2_centre[i] != 0:
                text += "[" + str(dfx_d1_slots[i]) + "] Dose-1 slots available across " + str(dfx_d1_centre[i]) + " centers and [" + str(dfx_d2_slots[i]) + "] Dose-2 slots available across " + str(dfx_d2_centre[i]) + " centres \n"
    print(count)
    if count == 8:
        text += "No available slots across any districts \n"
    text += "\n"

#print(text)

if same_flag:
    base_URL = 'https://api.telegram.org/your_generated_bot_token/sendMessage?chat_id=your_chat_id&text="Nothing has changed from the previous update. Refer the previous update in the chat."'
    requests.get(base_URL)
else:
    text += "\nFor booking visit CoWIN website(https://www.cowin.gov.in/home)."
    base_URL = 'https://api.telegram.org/your_generated_bot_token/sendMessage?chat_id=your_chat_id&text="{}"'.format(text)
    requests.get(base_URL)