import json

voltage_values = [1, 2, 3, 4, 5, 6]

dataDict = dict()
dataDict["voltage"] = dict()
dataDict["current"] = dict()

dataDict["voltage"]["labels"] = ["" for x in range(len(voltage_values))]
dataDict["voltage"]["datasets"] = [{"data": []}]
dataDict["voltage"]["datasets"][0]["data"].extend(voltage_values)

json_string = json.dumps(dataDict)

a = 5