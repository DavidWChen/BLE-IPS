#include <SoftwareSerial.h>
//HM-10 TX,RX
int flag[] = {0, 0, 0, 0};
SoftwareSerial BT(9,10);
void setup() {
  BT.begin(9600);
  Serial1.begin(57600);
}
void loop() {
  String str = "", result = "", uidmm = "", rssi = "", to_send = "", rssis[4];
  str = "AT+DISI?";
  BT.print(str);
  result = getBTString();
  for (int i = 11; i < result.length() - 8; i++) {
    if (result.substring(i, i + 4) == "DISC") {
      uidmm = result.substring(i + 5, i + 70);
      rssi = result.substring(i + 71, i + 75);
      if (uidmm == "4C000215:E2C56DB5DFFB48D2B060D0F5A71096E0:271207D2BA:1918FC04200C") {
        rssis[0] = rssi;
        flag[0] = 1;
      }
      else if (uidmm == "4C000215:E2C56DB5DFFB48D2B060D0F5A71096E0:271207E2C1:1918FC042018") {
        rssis[1] = rssi;
        flag[1] = 1;
      }
      else if (uidmm == "4C000215:E2C56DB5DFFB48D2B060D0F5A71096E0:271207F1BD:1918FC0420EE") {
        rssis[2] = rssi;
        flag[2] = 1;
      }
      else if (uidmm == "4C000215:E2C56DB5DFFB48D2B060D0F5A71096E0:27120835F1:1918FC042101") {
        rssis[3] = rssi;
        flag[3] = 1;
      }
      else
        ;
    }
  }
  if ((flag[0] == 1) && (flag[1] == 1) && (flag[2] == 1) && (flag[3] == 1)){
        to_send = rssis[0] + "," + rssis[1] + "," + rssis[2] + "," + rssis[3] + "," + "\n";
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

