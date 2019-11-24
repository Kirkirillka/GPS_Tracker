package de.tuIlmenau.gpsTracker.dao.impl;

import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;
import com.mongodb.client.AggregateIterable;
import com.mongodb.client.FindIterable;
import de.tuIlmenau.gpsTracker.connection.MongoDBFactory;
import de.tuIlmenau.gpsTracker.dao.ClientDeviceMessageDao;
import de.tuIlmenau.gpsTracker.dbModel.ClientDeviceMessage;
import de.tuIlmenau.gpsTracker.dbModel.ClientDeviceMessageFields;
import de.tuIlmenau.gpsTracker.dbModel.Coordinate;
import org.bson.Document;
import sun.reflect.generics.reflectiveObjects.NotImplementedException;

import java.lang.reflect.Type;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class ClientDeviceMessageMongoDao implements ClientDeviceMessageDao {
    private static final String TABLENAME = ClientDeviceMessageFields.TABLENAME;
    private final Type COORDS_LIST_TYPE = new TypeToken<ArrayList<Coordinate>>() {
    }.getType();

    @Override
    public ClientDeviceMessage getLast() {
        Document sort = new Document(ClientDeviceMessageFields.TIME, -1);
        FindIterable<Document> iterable = MongoDBFactory.getCollection(TABLENAME).find()
                .sort(sort).limit(1);
        Document item = iterable.first();
        if (item == null) {
            return null;
        }
        return MongoDBFactory.getParser().fromJson(item.toJson(), ClientDeviceMessage.class);
    }

    @Override
    public List<ClientDeviceMessage> getAllRecords() {
        List<ClientDeviceMessage> deviceMessages = new ArrayList<>();
        Gson parser = MongoDBFactory.getParser();
        FindIterable<Document> iterable = MongoDBFactory.getCollection(TABLENAME).find();
        for (Document doc : iterable) {
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
        for (Document doc : iterable) {
            parser.fromJson(doc.toJson(), ClientDeviceMessage.class);
        }
        return deviceMessages;
    }

    @Override
    public ClientDeviceMessage save(ClientDeviceMessage entity) {
        throw new NotImplementedException();//TODO
    }

    @Override
    public ClientDeviceMessage remove(ClientDeviceMessage entity) {
        throw new NotImplementedException();//TODO
    }

    @Override
    public Map<String, List<Coordinate>> getLastCoords() {
        Map<String, List<Coordinate>> devicesMessages = new HashMap<>();
        Gson parser = MongoDBFactory.getParser();
        AggregateIterable<Document> iterable = MongoDBFactory.getCollection(TABLENAME)
                .aggregate(buildAggregate(false));
        for (Document doc : iterable) {
            String key = doc.getString(MongoConstants.ID);
            List<Coordinate> coordinates = devicesMessages.computeIfAbsent(key, k -> new ArrayList<>());
            List<Document> list = doc.get(ClientDeviceMessageFields.CORDS, List.class);
            for (Document coord : list) {
                coordinates.add(parser.fromJson(coord.toJson(), Coordinate.class));
            }
        }
        return devicesMessages;
    }

    @Override
    public List<Coordinate> getLastCoordsByDeviceId(String deviceId) {
        List<Coordinate> deviceMessages = new ArrayList<>();
        Document projection = new Document(ClientDeviceMessageFields.LATITUDE, 1)
                .append(ClientDeviceMessageFields.LONGITUDE, 1);
        Gson parser = MongoDBFactory.getParser();
        FindIterable<Document> iterable = MongoDBFactory.getCollection(TABLENAME)
                .find(new Document(ClientDeviceMessageFields.DEVICE_ID, deviceId))
                .projection(projection);
        for (Document doc : iterable) {
            parser.fromJson(doc.toJson(), Coordinate.class);
        }
        return deviceMessages;
    }

    @Override
    public List<ClientDeviceMessage> getLastAll() {
        List<ClientDeviceMessage> devicesMessages = new ArrayList<>();
        Gson parser = MongoDBFactory.getParser();
        AggregateIterable<Document> iterable = MongoDBFactory.getCollection(TABLENAME)
                .aggregate(buildAggregate(true));
        for (Document doc : iterable) {
            Document document = doc.get(ClientDeviceMessageFields.DEVICE, Document.class);
            devicesMessages.add(parser.fromJson(document.toJson(), ClientDeviceMessage.class));
        }
        return devicesMessages;
    }

    private List<Document> buildAggregate(boolean onlyFirst) {
        Document projection = new Document(ClientDeviceMessageFields.LATITUDE, MongoConstants.VAL + ClientDeviceMessageFields.LATITUDE)
                .append(ClientDeviceMessageFields.LONGITUDE, MongoConstants.VAL + ClientDeviceMessageFields.LONGITUDE);
        Document groupExp = new Document(MongoConstants.ID, MongoConstants.VAL + ClientDeviceMessageFields.DEVICE_ID);
        if (!onlyFirst) {
            groupExp.append(ClientDeviceMessageFields.CORDS, new Document(MongoConstants.PUSH, projection));
        } else {
            groupExp.append(ClientDeviceMessageFields.DEVICE, new Document(MongoConstants.FIRST, MongoConstants.ROOT));
        }
        Document group = new Document(MongoConstants.GROUP, groupExp);
        Document sort = new Document(MongoConstants.SORT, new Document(ClientDeviceMessageFields.TIME, -1));
        return Arrays.asList(sort, group);
    }
}
