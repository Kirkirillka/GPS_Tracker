package de.tuIlmenau.gpsTracker.dao;

import de.tuIlmenau.gpsTracker.dbModel.ClientDeviceMessage;

import java.util.List;

public interface ClientDeviceMessageDao {
    public ClientDeviceMessage getLast();

    public List<ClientDeviceMessage> getAllRecords();

    public List<ClientDeviceMessage> getRecordByDeviceId(String id);

    public ClientDeviceMessage addRecord(ClientDeviceMessage entity);

    public ClientDeviceMessage remove(ClientDeviceMessage entity);

}
