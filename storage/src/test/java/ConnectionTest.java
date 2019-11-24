
import de.tuIlmenau.gpsTracker.dao.ClientDeviceMessageDao;
import de.tuIlmenau.gpsTracker.dao.impl.ClientDeviceMessageMongoDao;
import de.tuIlmenau.gpsTracker.dbModel.ClientDeviceMessage;
import de.tuIlmenau.gpsTracker.dbModel.Coordinate;

import java.util.List;
import java.util.Map;

public class ConnectionTest { //TODO it is necessary to write tests
    public static void main(String[] args) {
        ClientDeviceMessageDao dao = new ClientDeviceMessageMongoDao();
        Map<String, List<Coordinate>> lastCoords = dao.getLastCoords();
        List<ClientDeviceMessage> lastAll = dao.getLastAll();
        lastCoords.get("f");
       /* String id = UUID.randomUUID().toString();
        ClientDeviceMessage message = new ClientDeviceMessage();
        message.setLatitude(123);
        message.setLongitude(123);
        Gson gson = MongoDBFactory.getParser();
        Document doc = Document.parse(gson.toJson(message));
        message.setMessageType(ClientDeviceMessage.MessageType.raw);
      *//*  MongoDBFactory.getInstance().getCollection("test")
                .updateOne(new Document("_id", id), new Document("$set", doc),
//                .updateOne(new Document("_id", id),
//                        new Document("$set", new Document().append("user", "1")),
                        new UpdateOptions().upsert(true));*//*
        FindIterable<Document> iterable = MongoDBFactory.getCollection("data")
                .find().sort(new Document("time", -1));
        if (iterable != null) {
            final Document item = iterable.first();
            ClientDeviceMessage message1 = gson.fromJson(item.toJson(), ClientDeviceMessage.class);
            if (item != null) {
                System.out.println(item);
                MongoDBFactory.getCollection("test").deleteOne(new Document("_id", id));
            }
        }*/
    }
}
