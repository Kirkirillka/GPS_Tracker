package de.tuIlmenau.gpsTracker.dao.impl;

import com.mongodb.client.FindIterable;
import de.tuIlmenau.gpsTracker.connection.MongoDBFactory;
import de.tuIlmenau.gpsTracker.dao.UserDao;
import de.tuIlmenau.gpsTracker.dbModel.GpsEntity;
import org.bson.Document;
import sun.reflect.generics.reflectiveObjects.NotImplementedException;

import java.util.List;

public class UserMongoDao extends UserDao {
    private static final String TABLENAME = "test";

    @Override
    public GpsEntity getLast() {
        Document sort = new Document("CreateDate", -1);
        FindIterable<Document> iterable = MongoDBFactory.getCollection(TABLENAME).find().sort(sort).limit(1);
        return null;//TODO implement
    }

    @Override
    public List<GpsEntity> getAllRecords() {
throw new NotImplementedException("not inpl");
    }

    @Override
    public GpsEntity getRecordById(String id) {
        return null;
    }

    @Override
    public GpsEntity addRecord(GpsEntity entity) {
        return null;
    }

    @Override
    public GpsEntity remove(GpsEntity entity) {
        return null;
    }
}
