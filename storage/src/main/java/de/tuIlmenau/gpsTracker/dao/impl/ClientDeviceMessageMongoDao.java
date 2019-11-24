package de.tuIlmenau.gpsTracker.dao.impl;

import com.google.gson.Gson;
import com.mongodb.client.FindIterable;
import de.tuIlmenau.gpsTracker.connection.MongoDBFactory;
import de.tuIlmenau.gpsTracker.dao.ClientDeviceMessageDao;
import de.tuIlmenau.gpsTracker.dbModel.ClientDeviceMessage;
import de.tuIlmenau.gpsTracker.dbModel.ClientDeviceMessageFields;
import de.tuIlmenau.gpsTracker.dbModel.GpsEntity;
import org.bson.Document;
import sun.reflect.generics.reflectiveObjects.NotImplementedException;

import java.util.ArrayList;
import java.util.List;

public class ClientDeviceMessageMongoDao implements ClientDeviceMessageDao {
    private static final String TABLENAME = ClientDeviceMessageFields.TABLENAME;

    @Override
    public ClientDeviceMessage getLast() {
        Document sort = new Document(ClientDeviceMessageFields.TIME, -1);
        FindIterable<Document> iterable = MongoDBFactory.getCollection(TABLENAME).find()
                .sort(sort).limit(1);
        Document item = iterable.first();
        if (item == null) {
            return  null;
        }
        return MongoDBFactory.getParser().fromJson(item.toJson(), ClientDeviceMessage.class);
    }

    @Override
    public List<ClientDeviceMessage> getAllRecords() {
        List<ClientDeviceMessage> deviceMessages = new ArrayList<>();
        Gson parser = MongoDBFactory.getParser();
        FindIterable<Document> iterable = MongoDBFactory.getCollection(TABLENAME).find();
        for (Document doc: iterable) {
            parser.fromJson(doc.toJson(), ClientDeviceMessage.class);
        }
        return deviceMessages;
    }

    @Override
    public List<ClientDeviceMessage> getRecordByDeviceId(String id) {
        List<ClientDeviceMessage> deviceMessages = new ArrayList<>();
        Gson parser = MongoDBFactory.getParser();
        FindIterable<Document> iterable = MongoDBFactory.getCollection(TABLENAME)
                .find(new Document(ClientDeviceMessageFields.DEVICE_ID, id));
        for (Document doc: iterable) {
            parser.fromJson(doc.toJson(), ClientDeviceMessage.class);
        }
        return deviceMessages;
    }

    @Override
    public ClientDeviceMessage addRecord(ClientDeviceMessage entity) {
        throw new NotImplementedException();//TODO
    }

    @Override
    public ClientDeviceMessage remove(ClientDeviceMessage entity) {
        throw new NotImplementedException();//TODO
    }
}
