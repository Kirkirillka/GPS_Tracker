import com.mongodb.client.FindIterable;
import com.mongodb.client.model.UpdateOptions;
import de.tuIlmenau.gpsTracker.connection.MongoDBFactory;
import org.bson.Document;

import java.util.UUID;

public class ConnectionTest {
    public static void main(String[] args) {
        String id = UUID.randomUUID().toString();
        MongoDBFactory.getCollection("test")
                .updateOne(new Document("_id", id),
                        new Document("$set", new Document().append("user", "1")),
                        new UpdateOptions().upsert(true));
        FindIterable<Document> iterable = MongoDBFactory.getCollection("test").find(new Document("_id", id));
        if (iterable != null) {
            final Document item = iterable.first();
            if (item != null) {
                System.out.println(item);
                MongoDBFactory.getCollection("test").deleteOne(new Document("_id", id));
            }
        }
    }
}
