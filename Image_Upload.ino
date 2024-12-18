#include <WiFi.h>
#include "VideoStream.h"

#define CHANNEL 0
#define SERVER_IP "192.168.10.20"
#define SERVER_PORT 8888

// Use a pre-defined resolution, or choose to configure your own resolution
VideoSetting config(VIDEO_FHD, CAM_FPS, VIDEO_JPEG, 1);

char ssid[] = "NET-MESH-FOREST";    // your network SSID (name)
char pass[] = "B4r3f2c1!+";         // your network password
int status = WL_IDLE_STATUS;

uint32_t img_addr = 0;
uint32_t img_len = 0;

void uploadImage(uint8_t* buf, uint32_t len) {
    WiFiClient client;
    
    Serial.println("Attempting to connect to server...");
    if (client.connect(SERVER_IP, SERVER_PORT)) {
        Serial.println("Connected to server");
        
        // Send image length first
        client.println(len);
        
        // Send image data
        size_t bytesSent = client.write(buf, len);
        
        client.stop();
        
        Serial.print("Image upload ");
        Serial.println(bytesSent == len ? "successful" : "failed");
    } else {
        Serial.println("Connection to server failed");
    }
}

void setup() {
    Serial.begin(115200);
    
    // Connect to WiFi
    while (status != WL_CONNECTED) {
        Serial.print("Attempting to connect to SSID: ");
        Serial.println(ssid);
        status = WiFi.begin(ssid, pass);
        delay(5000);
    }
    
    Serial.println("WiFi connected");
    Serial.print("IP Address: ");
    Serial.println(WiFi.localIP());

    // Initialize camera
    Camera.configVideoChannel(CHANNEL, config);
    Camera.videoInit();
    Camera.channelBegin(CHANNEL);
}

void loop() {
    // Capture image
    Camera.getImage(CHANNEL, &img_addr, &img_len);
  delay(30000);
    if (img_addr != 0 && img_len > 0) {
        // Upload image to server
        uploadImage((uint8_t*)img_addr, img_len);
    } else {
        Serial.println("Image capture failed");
    }
    
    // Wait before next capture
    delay(30000);  // 5 seconds between uploads
}