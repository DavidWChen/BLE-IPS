package com.leedian.demo;

import com.google.gson.annotations.SerializedName;

import java.io.Serializable;

/**
 * Created by yangxuewu on 2017/7/19.
 */

public class MyData {


    /**
     * chip1 : {"raw_time":1.501226869755596E9,"x-coordinate":5.002878095006796,"y-coordinate":6.02235962842314,"z-coordinate":0.9813516295551126}
     * chip2 : {"raw_time":"t1","x-coordinate":"x1","y-coordinate":"y1","z-coordinate":"z1"}
     * chip3 : {"raw_time":"t2","x-coordinate":"x2","y-coordinate":"y2","z-coordinate":"z2"}
     */

    private Chip1Bean chip1;
    private Chip2Bean chip2;
    private Chip3Bean chip3;

    public Chip1Bean getChip1() {
        return chip1;
    }

    public void setChip1(Chip1Bean chip1) {
        this.chip1 = chip1;
    }

    public Chip2Bean getChip2() {
        return chip2;
    }

    public void setChip2(Chip2Bean chip2) {
        this.chip2 = chip2;
    }

    public Chip3Bean getChip3() {
        return chip3;
    }

    public void setChip3(Chip3Bean chip3) {
        this.chip3 = chip3;
    }

    public static class Chip1Bean {
        /**
         * raw_time : 1.501226869755596E9
         * x-coordinate : 5.002878095006796
         * y-coordinate : 6.02235962842314
         * z-coordinate : 0.9813516295551126
         */

        private double raw_time;
        @SerializedName("x-coordinate")
        private double xcoordinate;
        @SerializedName("y-coordinate")
        private double ycoordinate;
        @SerializedName("z-coordinate")
        private double zcoordinate;

        public double getRaw_time() {
            return raw_time;
        }

        public void setRaw_time(double raw_time) {
            this.raw_time = raw_time;
        }

        public double getXcoordinate() {
            return xcoordinate;
        }

        public void setXcoordinate(double xcoordinate) {
            this.xcoordinate = xcoordinate;
        }

        public double getYcoordinate() {
            return ycoordinate;
        }

        public void setYcoordinate(double ycoordinate) {
            this.ycoordinate = ycoordinate;
        }

        public double getZcoordinate() {
            return zcoordinate;
        }

        public void setZcoordinate(double zcoordinate) {
            this.zcoordinate = zcoordinate;
        }

        @Override
        public String toString() {
            return "=" + "\n" +
                    "     x_coordinate=" + xcoordinate + "\n" +
                    "     y_coordinate=" + ycoordinate + "\n" +
                    "     z_coordinate=" + zcoordinate;
        }

        //public Long rawtime() {
       //     return (long) raw_time;
        //}
    }



    public static class Chip2Bean {
        /**
         * raw_time : t1
         * x-coordinate : x1
         * y-coordinate : y1
         * z-coordinate : z1
         */

        private String raw_time;
        @SerializedName("x-coordinate")
        private String xcoordinate;
        @SerializedName("y-coordinate")
        private String ycoordinate;
        @SerializedName("z-coordinate")
        private String zcoordinate;

        public String getRaw_time() {
            return raw_time;
        }

        public void setRaw_time(String raw_time) {
            this.raw_time = raw_time;
        }

        public String getXcoordinate() {
            return xcoordinate;
        }

        public void setXcoordinate(String xcoordinate) {
            this.xcoordinate = xcoordinate;
        }

        public String getYcoordinate() {
            return ycoordinate;
        }

        public void setYcoordinate(String ycoordinate) {
            this.ycoordinate = ycoordinate;
        }

        public String getZcoordinate() {
            return zcoordinate;
        }

        public void setZcoordinate(String zcoordinate) {
            this.zcoordinate = zcoordinate;
        }

        @Override
        public String toString() {
            return "=" + "\n" +
                    "     x_coordinate=" + xcoordinate + "\n" +
                    "     y_coordinate=" + ycoordinate + "\n" +
                    "     z_coordinate=" + zcoordinate;
        }

    }

    public static class Chip3Bean {
        /**
         * raw_time : t2
         * x-coordinate : x2
         * y-coordinate : y2
         * z-coordinate : z2
         */

        private String raw_time;
        @SerializedName("x-coordinate")
        private String xcoordinate;
        @SerializedName("y-coordinate")
        private String ycoordinate;
        @SerializedName("z-coordinate")
        private String zcoordinate;

        public String getRaw_time() {
            return raw_time;
        }

        public void setRaw_time(String raw_time) {
            this.raw_time = raw_time;
        }

        public String getXcoordinate() {
            return xcoordinate;
        }

        public void setXcoordinate(String xcoordinate) {
            this.xcoordinate = xcoordinate;
        }

        public String getYcoordinate() {
            return ycoordinate;
        }

        public void setYcoordinate(String ycoordinate) {
            this.ycoordinate = ycoordinate;
        }

        public String getZcoordinate() {
            return zcoordinate;
        }

        public void setZcoordinate(String zcoordinate) {
            this.zcoordinate = zcoordinate;
        }

        @Override
        public String toString() {
            return  "=" + "\n" +
                    "     x_coordinate=" + xcoordinate + "\n" +
                    "     y_coordinate=" + ycoordinate + "\n" +
                    "     z_coordinate=" + zcoordinate;
        }


    }

    @Override
    public String toString() {
        return "chip1=" + chip1 + "\n" +
                "chip2=" + chip2 + "\n" +
                "chip3=" + chip3 + "\n";

    }

}

// global variable to store state of add/remove function
//