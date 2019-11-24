package de.tuIlmenau.gpsTracker.dao.impl;

import com.mongodb.client.FindIterable;
import de.tuIlmenau.gpsTracker.connection.MongoDBFactory;
import de.tuIlmenau.gpsTracker.dao.EntityDao;
import de.tuIlmenau.gpsTracker.dbModel.GpsEntity;
import org.bson.Document;
import sun.reflect.generics.reflectiveObjects.NotImplementedException;

import java.util.List;

public class EntityMongoDao implements EntityDao {
    private static final String TABLENAME = "test";

    @Override
    public GpsEntity getLast() {
        Document sort = new Document("CreateDate", -1);
        FindIterable<Document> iterable = MongoDBFactory.getCollection(TABLENAME).find().sort(sort).limit(1);
        return null;//TODO implement
    }

    @Override
    public List<GpsEntity> getAllRecords() {
        throw new NotImplementedException();//TODO
    }

    @Override
    public GpsEntity getRecordById(String id) {
        throw new NotImplementedException();//TODO
    }

    @Override
    public GpsEntity addRecord(GpsEntity entity) {
        throw new NotImplementedException();//TODO
    }

    @Override
    public GpsEntity remove(GpsEntity entity) {
        throw new NotImplementedException();//TODO
    }
}
