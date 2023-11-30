#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#include <uri/UriBraces.h>
#include "config.h"
#include "keys.h"

WiFiClient client;
ESP8266WebServer *server = NULL;
IRsend irsend(IR_SEND_PIN);

#ifdef FIXED_ADDRESS
IPAddress str2IP(char *ipstr, char *label) {
  Serial.printf("%s: %s", label, ipstr);
  IPAddress ret;
  if ( ret.fromString(ipstr) ) {
    Serial.println("");
  } else {
    Serial.println(" <- Invalid IP");
  }
  return ret;
}
#endif

int WIFIFailure = 0;
String url;

void lostWifiCallback (const WiFiEventStationModeDisconnected& evt) {
  Serial.println("Lost Wifi");
  ESP.reset();
  delay(1000);
}

KeyInfo FindKey(char *str) {
  for (int i = 0 ; i<std::end(KEYS) - std::begin(KEYS); i++ ) {
    if ( strcasecmp(str, KEYS[i].name) == 0 ) {
      return KEYS[i];
    }
  }
  return KeyInfo({"Invalid",0,0,0});
}

bool SendKey(char *str) {
  return SendKey(str, false);
}

bool SendKey(char *str, bool verbose) {
  bool ret = false;
  KeyInfo x = FindKey(str);
  if ( x.code1 > 0 ) {
    Serial.print("Sending Key: ");
    Serial.println(x.name);
    if (verbose ) server->sendContent("Sending Key: "+String(x.name)+"\n");
    IRDATA[REPL1] = x.code1;
    IRDATA[REPL2] = x.code2;
    IRDATA[REPL3] = x.code3;
    IRDATA[REPL4] = ( x.code1 < 1088 ) ? x.code1 + 1088 : x.code1 - 1088;
    IRDATA[REPL5] = x.code2;
    IRDATA[REPL6] = x.code3;
    irsend.enableIROut(38,50);
    for (int i=0; i<72; i++) {
        int val = IRDATA[i];
        if (i & 1) irsend.space(val);
        else       irsend.mark(val);
    }
    irsend.space(0);
    ret = true;
  } else {
    Serial.print("Invalid Key: ");
    Serial.println(str);
    if (verbose ) server->sendContent("Invalid Key: "+String(str)+"\n");
  }
  return ret;
}

void Web_Info() {
  Serial.println("Connection received endpoint '/'");
  server->setContentLength(CONTENT_LENGTH_UNKNOWN);
  server->send(200, "text/plain; charset=utf-8", "");
  server->sendContent("IR Channel Changer\n\n");
  server->sendContent("Options:\n");
  server->sendContent("   /list        - Show List of Supported Keys\n");
  server->sendContent("   /key/KEYID   - Transmit KEYID\n");
  server->sendContent("   /channel/### - Transmit Digits Followed by KEYOK\n");
  server->sendContent("   /reboot      - Reboot IR Controller\n");
  server->sendContent("");
  server->client().stop();  
}

void Web_ListKeys() {
  Serial.println("Connection received endpoint '/list'");
  server->setContentLength(CONTENT_LENGTH_UNKNOWN);
  server->send(200, "text/plain", "");

  char line[80];
  char name[20];
  char fmt[10];
  int m = 0;
  for (int i = 0 ; i<std::end(KEYS) - std::begin(KEYS); i++ ) {
    if ( m < strlen(KEYS[i].name) ) m = strlen(KEYS[i].name);
  }
  strcpy(line,"Valid Keys:");
  sprintf(fmt, "%%-%ds ", m);

  for (int i = 0 ; i<std::end(KEYS) - std::begin(KEYS); i++ ) {
    sprintf(name, fmt, KEYS[i].name);
    if ( ( i == 0 ) || ( strlen(line) + m > 45 ) ) {
      Serial.print(line);
      server->sendContent(line);
      Serial.print("\n    ");
      server->sendContent("\n    ");
      line[0] = '\0';
    }
    strcat(line, name);
  }
  Serial.println(line);
  server->sendContent(line);
  server->sendContent("\n\n");
  server->sendContent("");
  server->client().stop();  
}

void Web_SendKey() {    
  Serial.println("Connection received endpoint '/key'");
  String keyname = server->pathArg(0);
  Serial.print("  Key Received: '");
  Serial.print(keyname);
  Serial.println("'");
  char kname[22];
  strncpy(kname, keyname.c_str(), 20);
  KeyInfo x = FindKey(kname);
  if ( x.code1 > 0 ) {
    bool verbose = server->hasArg("verbose");
    if ( verbose ) {
      server->setContentLength(CONTENT_LENGTH_UNKNOWN);
      server->send(200, "text/plain", "");
    }
    SendKey(kname, verbose);
    if ( verbose ) {
      server->sendContent("");
      server->client().stop();
    } else {
      server->send(204, "text/plain", "");
    }
  } else {
    server->send(400, "text/plain", "Invalid Key: " + keyname + "\n");
  }
}

void Web_Channel() {
  Serial.println("Connection received endpoint '/channel'");
  int channel = server->pathArg(0).toInt();
  Serial.print("  Channel Received: '");
  Serial.print(channel);
  Serial.println("'");
  char num[3];
  if ( ( channel < 100 ) || ( channel > 999 ) ) {
    Serial.println("Invalid Channel");
    server->send(400, "text/plain", "Invalid Channel: " + String(channel) + "\n");
  } else {
    bool verbose = server->hasArg("verbose");
    if ( verbose ) {
      server->setContentLength(CONTENT_LENGTH_UNKNOWN);
      server->send(200, "text/plain", "");
    }
    SendKey("EXIT", verbose);
    delay(KEY_DELAY);
    SendKey("EXIT", verbose);
    delay(KEY_DELAY);
    sprintf(num, "%d", ( channel - channel % 100 ) / 100 );
    SendKey(num, verbose);
    delay(KEY_DELAY);
    channel = channel % 100;
    sprintf(num, "%d", ( channel - channel % 10 ) / 10 );
    SendKey(num, verbose);
    delay(KEY_DELAY);
    channel = channel % 10;
    sprintf(num, "%d", channel);
    SendKey(num, verbose);
    delay(KEY_DELAY);
    SendKey("OK");
    if ( verbose ) {
      server->sendContent("");
      server->client().stop();
    } else {
      server->send(204, "text/plain", "");
    }
  }
}

void Web_Reboot() {
  Serial.println("Connection received endpoint '/reboot'");
  server->send(200, "text/plain", "Rebooting Device\n");
  Serial.println("Rebooting Device");
  delay(1000);
  ESP.reset();
  delay(1000);
}

void setup() {
  Serial.begin(115200, SERIAL_8N1, SERIAL_TX_ONLY);
  Serial.println("");
  Serial.println("Starting Up");
  
#ifdef FIXED_ADDRESS
  IPAddress ip_addr = str2IP(IP_ADDRESS, "IP Address");
  IPAddress ip_gateway = str2IP(IP_GATEWAY, "Gateway");
  IPAddress ip_subnet = str2IP(IP_SUBNET, "Subnet");
  IPAddress ip_dns1 = str2IP(IP_DNS1, "Primary DNS");
  IPAddress ip_dns2 = str2IP(IP_DNS2, "Secondary DNS");
  if (!WiFi.config(ip_addr, ip_gateway, ip_subnet, ip_dns1, ip_dns2)) {
    Serial.println("Unable to Configure WIFI");
  }
#endif
  Serial.printf("Connecting to WIFI (%s)\n", WIFI_SSID);
  WiFi.begin(WIFI_SSID, WIFI_PASSWD);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  url = " http://" + WiFi.localIP().toString();
  if ( WEB_PORT != 80 ) {
    url += ":" + String(WEB_PORT);
  }
  url += "/";

  server = new ESP8266WebServer(WEB_PORT);

  WiFi.onStationModeDisconnected(&lostWifiCallback);

  irsend.begin();
  
  server->on("/", []() { Web_Info(); });
  server->on("/reboot", []() { Web_Reboot(); });
  server->on("/list", []() { Web_ListKeys(); });
  server->on(UriBraces("/key/{}"), []() { Web_SendKey(); });
  server->on(UriBraces("/channel/{}"), []() { Web_Channel(); });
  server->begin();
  Serial.println("HTTP Server started URL =" + url);
}

void loop() {
  server->handleClient();
}
