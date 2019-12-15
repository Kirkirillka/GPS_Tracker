package de.tuIlmenau.gpsTracker.dao;

import de.tuIlmenau.gpsTracker.dbModel.ClientDeviceMessage;
import de.tuIlmenau.gpsTracker.dbModel.Coordinate;

import java.util.List;
import java.util.Map;

public interface ClientDeviceMessageDao {
    public ClientDeviceMessage getLast();

    public List<ClientDeviceMessage> getAllRecords();

    public List<ClientDeviceMessage> getRecordByDeviceId(String id);

    public ClientDeviceMessage save(ClientDeviceMessage entity);

    public ClientDeviceMessage remove(ClientDeviceMessage entity);

    public Map<String, List<Coordinate>> getLastCoords();

    public List<Coordinate> getLastCoordsByDeviceId(String deviceId);

    public List<ClientDeviceMessage> getLastAll();


}
