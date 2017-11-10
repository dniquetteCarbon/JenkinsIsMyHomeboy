#include <Adafruit_NeoPixel.h>

const int LED_DATA_PIN = 2;
const int BUILTIN_LED_PIN = 13;
const int NUM_LEDS = 24;

const byte MSG_HEADER[] = {0xDE, 0xAD, 0xBE, 0xEF};
const byte MSG_FOOTER[] = {0xFE, 0xEB, 0xDA, 0xED};
const int HEADER_FOOTER_LENGTH = 4;
const int MESSAGE_TYPE_LENGTH = 1;

const int MSG_SET_RAW_VALUES = 0;
const int MSG_SET_BUILTIN_LED = 1;
const int MSG_SIZES[] = {3 * NUM_LEDS,  // MSG_SET_RAW_VALUES
                         1}; // MSG_SET_LIGHT_EFFECT
const int BUFFER_SIZE = 1024;
byte READ_BUFFER[BUFFER_SIZE];
int buffered_count = 0;

Adafruit_NeoPixel strip = Adafruit_NeoPixel(NUM_LEDS, LED_DATA_PIN, NEO_GRB + NEO_KHZ800);

void resetReadBuffer() {
  for(int i = 0; i < BUFFER_SIZE; i++) {
    READ_BUFFER[i] = 0;
  }
}

boolean validateMessage(byte message[]) {
  int message_type = (int)message[4];
  int message_data_size = MSG_SIZES[message_type];
  int message_footer_offset = 5 + message_data_size;
  return verifyMessageHeader(message) && verifyMessageFooter(message, message_footer_offset);
}

void parseAndApplyMessage(byte message[]) {
  if(!validateMessage(message)) {
    return; 
  }
  
  const int message_type = (int)message[4];
  const int message_data_size = MSG_SIZES[message_type];
  const int message_data_offset = HEADER_FOOTER_LENGTH + MESSAGE_TYPE_LENGTH;
  
  byte message_data[1024];

  for(int i = 0; i < message_data_size; i++) {
    message_data[i] = message[message_data_offset + i];
  }
  
  switch(message_type) {
    case MSG_SET_RAW_VALUES:
      writeRawValuesToLights(message_data);
    break;

    case MSG_SET_BUILTIN_LED:
      setBuiltinLED((int)(message_data[0]));
    break;
  }
}

boolean verifyHeaderFooter(byte message[], const byte expected_value[], int start_index) {
  boolean message_verified = true;
  for(int i = 0; i < HEADER_FOOTER_LENGTH; i++) {
    message_verified = message_verified && (message[i + start_index] == expected_value[i]);
  }
  return message_verified;
}

boolean verifyMessageHeader(byte message[]) {
  boolean result = verifyHeaderFooter(message, MSG_HEADER, 0);
  // result ? Serial.println("Got DEADBEEF.") : Serial.println("Verify Header Failed");
  return result;
}

boolean verifyMessageFooter(byte message[], int start_index) {
  boolean result = verifyHeaderFooter(message, MSG_FOOTER, start_index);
  return result;
}

void writeRawValuesToLights(byte light_data[]) {
  for(int i = 0; i < NUM_LEDS * 3; i+=3) {
    //Serial.println("Setting pixel " + String(i/3) + " to " + String(light_data[i]) + ":" + String(light_data[i + 1]) + ":" + String(light_data[i + 2]));
    strip.setPixelColor(i / 3, (int)light_data[i], (int)light_data[i+1], (int)light_data[i+2]);
  }
  strip.show();
}

void setBuiltinLED(int pin_value) {
  digitalWrite(BUILTIN_LED_PIN, pin_value);
}

boolean endOfMessageReceived() {
  if(buffered_count < 2*HEADER_FOOTER_LENGTH + MESSAGE_TYPE_LENGTH) {
    return false;
  }
  return verifyMessageFooter(READ_BUFFER, buffered_count - 4);
}
  

void setup() {
  pinMode(BUILTIN_LED_PIN, OUTPUT);
  Serial.begin(115200);
  resetReadBuffer();
  strip.begin();
  strip.show();
}

void loop() {
  if(Serial.available()) {
      READ_BUFFER[buffered_count] = Serial.read();
      buffered_count += 1;
    }
  if(endOfMessageReceived()) {
      parseAndApplyMessage(READ_BUFFER);
      resetReadBuffer();
      buffered_count = 0;
   }
}





