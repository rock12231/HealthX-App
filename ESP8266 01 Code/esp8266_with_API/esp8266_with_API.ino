#include ‹ESP8266wiFi.h>
#include <ESP8266HTTPClient.h>
#include ‹WiFiclient.h>
#include ‹ArduinoJson.h>

// Replace with your network credentials
const char* ssid = "Avinash";
const char* password = "Avi7071955977";
// Server URL and endpoint
const char* serverUrl = "http://192.168.1.37:8000/data/";

void setup() {
  Serial.begin (115200);
  // Connect to Wi-Fi
  WiFi. begin(ssid, password);
  while (WiFi.status() |= WL_CONNECTED) {
    delay (1000);
    serial printin("Connecting to WiFi...");
  }
  Serial-printin("Connected to wiFi");
  Serial.print ("IP address: "); serial.printin(WiFi.localIP());
}

void loop() {
// Create JSON payload
//['age', 'sex'' ср','trestbps', 'chol', 'fbs', 'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal', 'target']

DynamicJsonDocument jsonPayload(256);
jsonPayload["title"] = temperature;

// Serialize JSON to a string
String jsonString;
serializelson(jsonPayload, jsonstring);

// Send POST request
WiFiClient client;
HTTPClient http;
if (http.begin(client, serverUrl)) {
  http. addHeader ("Content-Type", "application/json");
  int httpResponseCode = http.POST(jsonString);
  
  if (httpResponsecode › 0) {
    serial.print (*HTTP Response code: *);
    Serial printin(httpResponseCode) ;
    string response = http-getstring();
    Serial-printin(response);
  } else {
    Serial print("Error code: ");
    Serial-printin(httpResponseCode);
  }

  http.end() ;
} else {
Serial-printin("Unable to connect");
}
// Wait for 5 seconds
delay (15000) ;
}