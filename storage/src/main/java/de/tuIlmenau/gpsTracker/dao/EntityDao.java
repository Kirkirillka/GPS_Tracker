package de.tuIlmenau.gpsTracker.dao;

import de.tuIlmenau.gpsTracker.dbModel.GpsEntity;

import java.util.List;

public interface UserDao {
    public GpsEntity getLast();

    public List<GpsEntity> getAllRecords();

    public GpsEntity getRecordById(String id);

    public GpsEntity addRecord(GpsEntity entity);

    public GpsEntity remove(GpsEntity entity);

}
