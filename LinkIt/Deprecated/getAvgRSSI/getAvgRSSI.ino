#include <SoftwareSerial.h>
//HM-10 TX,RX
int flag[] = {0, 0, 0, 0};
int rssis[4];
SoftwareSerial BT(9, 10);
void setup() {
  BT.begin(9600);
  Serial1.begin(57600);
}
void loop() {
  String  result = "", uidmm = "", rssi = "", to_send = "";
  int rssint = 0;
  BT.print("AT+DISI?");
  result = getBTString();
  for (int i = 11; i < result.length() - 8; i++) {
    if (result.substring(i, i + 4) == "DISC") {
      uidmm = result.substring(i + 5, i + 70);
      rssi = result.substring(i + 71, i + 75);//always negative
      rssint = rssi.toInt();
      if (uidmm == "4C000215:E2C56DB5DFFB48D2B060D0F5A71096E0:271207D2BA:1918FC04200C") {
        if (rssis[0] != 0) {
          for (int j = 0; j < 4; j++) {
            rssint = (rssis[0] + rssint) / 2;
          }
        }
        rssis[0] = rssint;
        flag[0] = 1;
      }
      else if (uidmm == "4C000215:E2C56DB5DFFB48D2B060D0F5A71096E0:271207E2C1:1918FC042018") {
        if (rssis[1] != 0) {
          for (int j = 0; j < 4; j++) {
            rssint = (rssis[1] + rssint) / 2;
          }
        }
        rssis[1] = rssint;
        flag[1] = 1;
      }
      else if (uidmm == "4C000215:E2C56DB5DFFB48D2B060D0F5A71096E0:271207F1BD:1918FC0420EE") {
        if (rssis[2] != 0) {
          for (int j = 0; j < 4; j++) {
            rssint = (rssis[2] + rssint) / 2;
          }
        }
        rssis[2] = rssint;
        flag[2] = 1;
      }
      else if (uidmm == "4C000215:E2C56DB5DFFB48D2B060D0F5A71096E0:27120835F1:1918FC042101") {
        if (rssis[3] != 0) {
          for (int j = 0; j < 4; j++) {
            rssint = (rssis[3] + rssint) / 2;
          }
        }
        rssis[3] = rssint;
        flag[3] = 1;
      }
      else
        ;
    }
  }
  if ((flag[0] == 1) && (flag[1] == 1) && (flag[2] == 1) && (flag[3] == 1)) {
    to_send = String(rssis[0]) + "," + String(rssis[1]) + "," + String(rssis[2]) + "," + String(rssis[3]) + "," + "\n";
    Serial1.print(to_send);
    flag[0] = flag[1] = flag[2] = flag[3] = 0;
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

