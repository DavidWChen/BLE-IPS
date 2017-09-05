#include <SoftwareSerial.h>
//TX -> 9 , RX -> 10
//N.B. Connect Rx to Tx and vice versa
//Our HM-10 has these connections flipped
SoftwareSerial BT(9, 10);

void setup() {
  //link to HM-10 and 7688
  BT.begin(9600);
  Serial1.begin(57600);
}

void loop() {
  String result = "";
  //send discovery command to HM-10
  BT.print("AT+DISI?");
  result = getBTString();
  //as long as something was found, send to 7688
  if (!result.equals("")) {
    Serial1.print(result);
  }
}

String getBTString() {
  String str = "";
  //until the string contains "DISCE"
  while (str.indexOf("DISCE") <= 0) {
    //while there is data waiting
    while (BT.available()) {
      //read and append to string
      char temp = BT.read();
      if (temp != '\n') {
        str += temp;
      }
    }
  }
  return str;
}

