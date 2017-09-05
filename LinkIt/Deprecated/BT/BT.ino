#include <SoftwareSerial.h>
//HM-10 TX -> 6 , RX -> 7
SoftwareSerial BT(9, 10);

void setup() {
  Serial.begin(9600);
  BT.begin(9600);
  Serial1.begin(57600);
}

void loop() {

  String str = "", result = "";

//  str = getSerialString();
//
//  //=========================== MODE 1 : 接受AT Commands
//  if (!str.equals("")) {
//    Serial.println(str);
//    BT.print(str);
//    result = getBTString();
//  }
  //===========================

  //=========================== MODE 2 : 發送AT Commands
    str = "AT+DISI?";
    Serial.println(str);
    BT.print(str);
    result = getBTString();
  //===========================

  if (!result.equals("")) {
    Serial1.print(result);
  }
}

String getSerialString() {
  String str = "";
  while (Serial.available()) {
    char temp = Serial.read();
    if (temp != '\n') {
      str += temp;
    }
    delay(5);
  }
  return str;
}

String getBTString() {
  String str = "";
  while (str.indexOf("DISCE") <= 0) {
    while (BT.available()) {
      char temp = BT.read();
      if (temp != '\n') {
        str += temp;
      }
      //delay(5);
    }
  }
  return str;
}

