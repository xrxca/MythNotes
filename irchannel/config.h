// Replace with your WiFi details
#define WIFI_SSID   "YOUR-WIFI-SID"
#define WIFI_PASSWD "YOUR-WIFI-PASSWD"

#define IR_SEND_PIN 4

#define WEB_PORT 80

#define KEY_DELAY 510

// Fixed Address
#define FIXED_ADDRESS true
#ifdef FIXED_ADDRESS
  #define IP_ADDRESS "192.168.1.129"
  #define IP_GATEWAY "192.168.1.254"
  #define IP_SUBNET "255.255.255.0"
  #define IP_DNS1 "192.168.1.254"
#endif
