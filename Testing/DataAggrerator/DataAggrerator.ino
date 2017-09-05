#include <SoftwareSerial.h>
//HM-10 TX,RX
int flag[] = {1, 1, 1, 1};
const byte dtpts = 100;
byte r200C[dtpts],r2018[dtpts],r20EE[dtpts],r2101[dtpts];
byte i200C = 0, i2018 = 0, i20EE = 0, i2101 = 0;
SoftwareSerial BT(10, 11);
void setup() {
  Serial.begin(9600);
  BT.begin(9600);
}
void loop() {
  Serial.print("L");
  String str = "", result = "", uidmm = "", rssi = "", to_send = "", rssis[4];
  str = "AT+DISI?";
  //Serial.println(str);
  BT.print(str);
  result = getBTString();
  for (int i = 11; i < result.length() - 8; i++) {
    if (result.substring(i, i + 4) == "DISC") {
      uidmm = result.substring(i + 5, i + 70);
      rssi = result.substring(i + 72, i + 75);
      if (uidmm == "4C000215:E2C56DB5DFFB48D2B060D0F5A71096E0:271207D2BA:1918FC04200C") {
        if (flag[0] == 1) {
          r200C[i200C] = rssi.toInt();
          i200C++;
          if (i200C == dtpts) {
            Serial.println();
            Serial.println("200C: ");
            for (int i = 0; i < dtpts; i ++ ) {
              Serial.println(r200C[i]);
            }
            flag[0] = 0;
          }
        }
      }
      else if (uidmm == "4C000215:E2C56DB5DFFB48D2B060D0F5A71096E0:271207E2C1:1918FC042018") {
        if (flag[1] == 1) {
          r2018[i2018] = rssi.toInt();
          i2018++;
          if (i2018 == dtpts) {
            Serial.println();
            Serial.println("2018: ");
            for (int i = 0; i < dtpts; i ++ ) {
              Serial.println(r2018[i]);
            }
            flag[1] = 0;
          }
        }
      }
      else if (uidmm == "4C000215:E2C56DB5DFFB48D2B060D0F5A71096E0:271207F1BD:1918FC0420EE") {
        if (flag[2] == 1) {
          r20EE[i20EE] = rssi.toInt();
          i20EE++;
          if (i20EE == dtpts) {
            Serial.println();
            Serial.println("20EE: ");
            for (int i = 0; i < dtpts; i ++ ) {
              Serial.println(r20EE[i]);
            }
            flag[2] = 0;
          }
        }
      }
      else if (uidmm == "4C000215:FDA50693A4E24FB1AFCFC6EB07647825:27120835F1:1918FC042101") {
        if (flag[3] == 1) {
          r2101[i2101] = rssi.toInt();
          i2101++;
          if (i2101 == dtpts) {
            Serial.println();
            Serial.println("2101: ");
            for (int i = 0; i < dtpts; i ++ ) {
              Serial.println(r2101[i]);
            }
            flag[3] = 0;
          }
        }
      }
      else
        ;
    }
  }
}

String getBTString() {
  String str = "";
  while (str.indexOf("DISCE") <= 0) {
    while (BT.available()) {
      char temp = BT.read();
      if (temp != '\n') {
        str += temp;
      }
    }
  }
  return str;
}


