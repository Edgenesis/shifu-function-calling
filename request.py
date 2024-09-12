import requests
output=0
print("http://localhost:30080/deviceshifu-plc/sendsinglebit?rootaddress=Q&address=0&start=0&digit=0&value=" + str(output))
response = requests.get("http://localhost:30080/deviceshifu-plc/sendsinglebit?rootaddress=Q&address=0&start=0&digit=0&value=" + str(output))
