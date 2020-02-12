/*
  0: off
  1: red
  2: green
  3: blue
  4: yellow
  5: magenta
  6: cyan
  7: white
*/
boolean colorR[8] = {false, true, false, false, true, true, false, true};
boolean colorG[8] = {false, false, true, false, true, false, true, true};
boolean colorB[8] = {false, false, false, true, false, true, true, true};

int pins[16] = {30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45};

int reds[64] = {251, 235, 219, 203, 183, 182, 181, 180, 115, 98, 81, 64, 63, 46, 29, 12, 250, 234, 218, 202, 164, 165, 166, 167, 66, 83, 96, 113, 47, 62, 13, 28, 249, 233, 217, 201, 150, 151, 148, 149, 97, 112, 67, 82, 31, 14, 61, 44, 248, 232, 216, 200, 133, 132, 135, 134, 80, 65, 114, 99, 15, 30, 45, 60};
int greens[64] = {247, 230, 213, 196, 179, 178, 177, 176, 127, 110, 93, 76, 59, 43, 27, 11, 244, 229, 214, 199, 162, 163, 160, 161, 79, 94, 109, 124, 42, 58, 10, 26, 246, 231, 212, 197, 145, 144, 147, 146, 111, 126, 77, 92, 25, 9, 57, 41, 245, 228, 215, 198, 128, 129, 130, 131, 95, 78, 125, 108, 8, 24, 40, 56};
int blues[64] = {243, 226, 209, 192, 191, 190, 189, 188, 123, 107, 91, 75, 55, 38, 21, 4, 242, 227, 208, 193, 175, 174, 173, 172, 74, 90, 106, 122, 36, 53, 6, 23, 241, 224, 211, 194, 159, 158, 157, 156, 105, 121, 73, 89, 22, 7, 52, 37, 240, 225, 210, 195, 143, 142, 141, 140, 88, 72, 120, 104, 5, 20, 39, 54};
int n =  16;
int actualColor[64];

int last_hi = pins[0];
int last_lo = pins[0];

int width = 35;    //300 - 64 leds.  || 100 - 128 leds  || 40 - 192 leds


String inputString = "";         // a String to hold incoming data
boolean stringComplete = false;  // whether the string is complete
char copy[65];

void setup() {
  Serial.begin(57600);
  
  inputString.reserve(100); // reserve 100 bytes 

  for (int i = 0; i < n; i++)
    pinMode(pins[i], INPUT);

  for (int j = 0; j < 64; j++)
    actualColor[j] = 3;
    
  delay(200);
}

void loop() {
  for (int i = 0; i < 64; i++)
    ledON(i, actualColor[i]);
  digitalWrite(last_hi, LOW);

  if (stringComplete) {
    inputString.toCharArray(copy, 65);
    for (int i = 0; i < 64; i++)
      actualColor[i] = copy[i] - '0';

    // clear the string:
    inputString = "";
    stringComplete = false;
  }
}

void serialEvent() {
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    inputString += inChar;
    if (inChar == '\n') 
      stringComplete = true;
  }
}

void led_HL(int index) {
  digitalWrite(last_hi, LOW);
  pinMode(last_hi, INPUT);
  pinMode(last_lo, INPUT);

  last_hi = pins[index / n];
  last_lo = pins[index % n];

  pinMode(last_hi, OUTPUT);
  pinMode(last_lo, OUTPUT);
  digitalWrite(last_hi, HIGH);
  digitalWrite(last_lo, LOW);
  delayMicroseconds(width);
}

void ledON(int led, int color) {
  if ( colorR[color] )
    led_HL(reds[led]);
  if ( colorG[color] )
    led_HL(greens[led]);
  if ( colorB[color] )
    led_HL(blues[led]);
}

void ledON(int x, int y, int z, boolean r, boolean g, boolean b) {
  int index;
  index = x + (y * 4) + (z * 16);
  if ( r )
    led_HL(reds[index]);
  if ( g )
    led_HL(greens[index]);
  if ( b )
    led_HL(blues[index]);
}

