import json
import copy
import datetime
import os

dashboards = []
for dashboardFileName in os.listdir(os.getcwd() + '\input'):
  file = open("input/" + dashboardFileName)
  dashboard = json.load(file)
  file.close()
  dashboards.append(dashboard)

file = open("dashboardTemplate.json")
dashboardTemplate = json.load(file)
file.close()

file = open("pageTemplate.json")
pageTemplate = json.load(file)
file.close()

for dashboard in dashboards:
  dashboardTemplateTemp = copy.deepcopy(dashboardTemplate)
  dashboardTemplateTemp["name"] = dashboard["dashboardName"]
  
  
  for page in dashboard["pages"]:
    pageTemplateTemp = copy.deepcopy(pageTemplate)
    
    five_minute = datetime.timedelta(minutes = 5)

    # Convert to datetime
    startTime_Rampup300 = datetime.datetime.strptime(page["senarios"]["rampup300"]["startTime"], "%Y-%m-%d %H:%M")
    startTime_Rampup0 = datetime.datetime.strptime(page["senarios"]["rampup0"]["startTime"], "%Y-%m-%d %H:%M")
    duration_Rampup300 = datetime.timedelta(minutes = page["senarios"]["rampup300"]["duration"])
    duration_Rampup0 = datetime.timedelta(minutes = page["senarios"]["rampup0"]["duration"])
    
    # Calculate times base on start time and duration in senario rampup 300
    endTime_Rampup300 = startTime_Rampup300 + duration_Rampup300
    startTimeChart_Rampup300 = startTime_Rampup300 - five_minute
    endTimeChart_Rampup300 = endTime_Rampup300 + five_minute
    
    # Calculate times base on start time and duration in senario rampup 0
    endTime_Rampup0 = startTime_Rampup0 + duration_Rampup0
    startTimeChart_Rampup0 = startTime_Rampup0 - five_minute
    endTimeChart_Rampup0 = endTime_Rampup0 + five_minute

    pageTemplateTemp = json.dumps(pageTemplateTemp)
    
    pageTemplateTemp = pageTemplateTemp.replace("AppName", dashboard["appName"])
    pageTemplateTemp = pageTemplateTemp.replace("PageName", page["pageName"])
    pageTemplateTemp = pageTemplateTemp.replace("TransactionName", page["transactionName"])
    
    pageTemplateTemp = pageTemplateTemp.replace("StartTime_Rampup300", startTime_Rampup300.strftime("%Y-%m-%d %H:%M"))
    pageTemplateTemp = pageTemplateTemp.replace("EndTime_Rampup300", endTime_Rampup300.strftime("%Y-%m-%d %H:%M"))
    pageTemplateTemp = pageTemplateTemp.replace("StartTimeChart_Rampup300", startTimeChart_Rampup300.strftime("%Y-%m-%d %H:%M"))
    pageTemplateTemp = pageTemplateTemp.replace("EndTimeChart_Rampup300", endTimeChart_Rampup300.strftime("%Y-%m-%d %H:%M"))

    pageTemplateTemp = pageTemplateTemp.replace("StartTime_Rampup0", startTime_Rampup0.strftime("%Y-%m-%d %H:%M"))
    pageTemplateTemp = pageTemplateTemp.replace("EndTime_Rampup0", endTime_Rampup0.strftime("%Y-%m-%d %H:%M"))
    pageTemplateTemp = pageTemplateTemp.replace("StartTimeChart_Rampup0",startTimeChart_Rampup0.strftime("%Y-%m-%d %H:%M"))
    pageTemplateTemp = pageTemplateTemp.replace("EndTimeChart_Rampup0",endTimeChart_Rampup0.strftime("%Y-%m-%d %H:%M"))
    
    pageTemplateTemp=json.loads(pageTemplateTemp)
    dashboardTemplateTemp["pages"].append(pageTemplateTemp)
    
  dashboard = json.dumps(dashboardTemplateTemp)
  outputFile = open("output/" + dashboardTemplateTemp["name"] + ".json", "w")
  outputFile.write(dashboard)
  outputFile.close()

print("Script execute completed...")