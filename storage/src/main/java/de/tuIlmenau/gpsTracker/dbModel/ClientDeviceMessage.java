package de.tuIlmenau.gpsTracker.dbModel;


import com.fasterxml.jackson.annotation.JsonProperty;

import javax.xml.datatype.XMLGregorianCalendar;



public class ClientDeviceMessage {

    @JsonProperty(ClientDeviceMessageFields.TIME)
    private XMLGregorianCalendar time;

    public enum MessageType {
        raw,
        wifi
    }

    @JsonProperty("message_type")
    private MessageType messageType;

    @JsonProperty("device")
    private Device device;


    public static class Device {

        @JsonProperty("id")
        private String id;

        private enum DeviceType {
            handy,
            UAV
        }

        @JsonProperty("device_type")
        private DeviceType deviceType;


        public String getId() {
            return id;
        }

        public void setId(String id) {
            this.id = id;
        }

        public DeviceType getDeviceType() {
            return deviceType;
        }

        public void setDeviceType(DeviceType deviceType) {
            this.deviceType = deviceType;
        }
    }

    @JsonProperty("longitude")
    private double longitude;

    @JsonProperty("latitude")
    private double latitude;

    @JsonProperty("payload")
    private Block payload;


    public static class Block {

        @JsonProperty("info_type")
        private String infoType;

        @JsonProperty("ssid")
        private String ssid;

        @JsonProperty("bssid")
        private String bssid;

        @JsonProperty("signal")
        private Signal signal;


        public static class Signal {

            @JsonProperty("rssi")
            private int rssi;

            public int getRssi() {
                return rssi;
            }

            public void setRssi(int rssi) {
                this.rssi = rssi;
            }
        }

        public String getInfoType() {
            return infoType;
        }

        public void setInfoType(String infoType) {
            this.infoType = infoType;
        }

        public String getSsid() {
            return ssid;
        }

        public void setSsid(String ssid) {
            this.ssid = ssid;
        }

        public String getBssid() {
            return bssid;
        }

        public void setBssid(String bssid) {
            if (bssid.matches("^([0-9A-Fa-f]{2}[\\.:-]){5}([0-9A-Fa-f]{2})$")) this.bssid = bssid;
        }

        public Signal getSignal() {
            return signal;
        }

        public void setSignal(Signal signal) {
            this.signal = signal;
        }
    }


    public XMLGregorianCalendar getTime() {
        return time;
    }

    public void setTime(XMLGregorianCalendar time) {
        this.time = time;
    }

    public MessageType getMessageType() {
        return messageType;
    }

    public void setMessageType(MessageType messageType) {
        this.messageType = messageType;
    }

    public Device getDevice() {
        return device;
    }

    public void setDevice(Device device) {
        this.device = device;
    }

    public double getLongitude() {
        return longitude;
    }

    public void setLongitude(double longitude) {
        this.longitude = longitude;
    }

    public double getLatitude() {
        return latitude;
    }

    public void setLatitude(double latitude) {
        this.latitude = latitude;
    }

    public Block getPayload() {
        return payload;
    }

    public void setPayload(Block payload) {
        this.payload = payload;
    }
}