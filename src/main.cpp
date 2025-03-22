#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET    -1  
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

void setup() {
    Serial.begin(115200);

    if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) { 
        Serial.println(F("SSD1306 allocation failed"));
        for (;;);
    }

    display.clearDisplay();
    display.setTextSize(1);
    display.setTextColor(WHITE);
    display.setCursor(10, 10);
    display.println("Starting...");
    display.display();
    delay(2000);
}

void loop() {
    display.clearDisplay();
    
    int heartRate = random(60, 120);
    int spo2 = random(95, 100);

    display.setTextSize(2);
    display.setTextColor(WHITE);
    display.setCursor(10, 5);
    display.println("Monitor");

    display.setTextSize(2);
    display.setCursor(10, 30);
    display.print("BPM: ");
    display.print(heartRate);

    display.setCursor(10, 50);
    display.print("SpO2: ");
    display.print(spo2);
    display.print("%");

    display.display();  // Ensure display updates

    // Send data to Serial for Python
    Serial.print(heartRate);
    Serial.print(",");
    Serial.println(spo2);

    delay(1000);
}
