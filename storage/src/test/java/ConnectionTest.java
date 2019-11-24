import com.google.gson.Gson;
import com.mongodb.client.FindIterable;
import com.mongodb.client.model.UpdateOptions;
import de.tuIlmenau.gpsTracker.connection.MongoDBFactory;
import de.tuIlmenau.gpsTracker.dbModel.ClientDeviceMessage;
import org.bson.Document;

import java.util.UUID;

public class ConnectionTest {
    public static void main(String[] args) {
        String id = UUID.randomUUID().toString();
        ClientDeviceMessage message = new ClientDeviceMessage();
        message.setId(id);
        message.setLatitude(123);
        message.setLongitude(123);
        Gson gson = new Gson();
        Document doc = Document.parse(gson.toJson(message));
        message.setMessageType(ClientDeviceMessage.MessageType.raw);
        MongoDBFactory.getInstance().getCollection("test")
                .updateOne(new Document("_id", id), new Document("$set", doc),
//                .updateOne(new Document("_id", id),
//                        new Document("$set", new Document().append("user", "1")),
                        new UpdateOptions().upsert(true));
        FindIterable<Document> iterable = MongoDBFactory.getCollection("test").find(new Document("_id", id));
        if (iterable != null) {
            final Document item = iterable.first();
            ClientDeviceMessage message1 = gson.fromJson(item.toJson(), ClientDeviceMessage.class);
            if (item != null) {
                System.out.println(item);
                MongoDBFactory.getCollection("test").deleteOne(new Document("_id", id));
            }
        }
    }
}
