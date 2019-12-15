package de.tuIlmenau.gpsTracker.dbModel;

import com.fasterxml.jackson.annotation.JsonProperty;

public class Device {

    @JsonProperty("id")
    private String id;

    private Device(Builder builder) {
        setId(builder.id);
        setDeviceType(builder.deviceType);
    }

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

    public static final class Builder {
        private String id;
        private DeviceType deviceType;

        public Builder() {
        }

        public Builder id(String val) {
            id = val;
            return this;
        }

        public Builder deviceType(DeviceType val) {
            deviceType = val;
            return this;
        }

        public Device build() {
            return new Device(this);
        }
    }
}
