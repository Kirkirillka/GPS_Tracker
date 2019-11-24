package de.tuIlmenau.gpsTracker.connection;

import com.mongodb.MongoClient;
import com.mongodb.MongoClientOptions;
import com.mongodb.MongoClientURI;
import com.mongodb.MongoCredential;
import com.mongodb.ServerAddress;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoDatabase;
import org.apache.log4j.Logger;
import org.bson.Document;
import org.bson.codecs.configuration.CodecRegistry;
import org.bson.codecs.pojo.PojoCodecProvider;

import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.Collections;
import java.util.Properties;

import static org.bson.codecs.configuration.CodecRegistries.fromProviders;
import static org.bson.codecs.configuration.CodecRegistries.fromRegistries;

public class MongoDBFactory {
    private final static Logger logger = Logger.getLogger(MongoDBFactory.class); //TODO create some util for logger class
    private static MongoClient mongoClient;
    private static volatile MongoDatabase db;
    private static boolean reconnect;


    private static final String FILE = "mongo.properties";
    private static final String USERNAME = "username";
    private static final String DBNAME = "dbName";
    private static final String PASSWORD = "password";
    private static final String HOST = "host";
    private static final String PORT = "port";


    private static final Object lock = new Object();
    private static final int CONNECTION_PER_HOST = 30;

    private static String user = "user";
    private static String database = "test";
    private static String host = "localhost";
    private static int port = 27017;
    private static char[] password = "password".toCharArray();

    private MongoDBFactory() {
    }

    public static MongoDatabase getInstance() {
        if (db == null) {
            synchronized (lock) {
                if (db == null) {
                    connect();
                }
            }
        }
        return db;
    }

    public static void reconnect() {
        reconnect = true;
        synchronized (lock) {
            if (reconnect) {
                connect();
                reconnect = false;
            }
        }
    }

    private static void connect() {
        db = null;
        if (mongoClient != null) {
            try {
                mongoClient.close();
            } catch (Exception e) {
                logger.error("Mongo client throws exception while closing connection", e);
            }
        }
        mongoClient = getMongoClient();
        db = mongoClient.getDatabase(getDatabaseName());
    }

    private static MongoClient getMongoClient() {
        if (System.getProperty("mongo") != null) {
            loadDbConfig();
        }
        /*return new MongoClientURI(new ServerAddress(host, port),
                Collections.singletonList(MongoCredential.createScramSha1Credential(user, database, password)),*/
        MongoClientURI uri = new MongoClientURI("mongodb://user:password@localhost:27017",
                new MongoClientOptions.Builder()
                        .connectTimeout(0).connectionsPerHost(CONNECTION_PER_HOST)
                        .cursorFinalizerEnabled(false));
        return new MongoClient(uri);
    }

    private static void loadDbConfig() {
        final Properties credProp = loadConfigFromLocalFile();
        host = credProp.getProperty(HOST);
        port = Integer.parseInt(credProp.getProperty(PORT));
        database = credProp.getProperty(DBNAME);
        user = credProp.getProperty(USERNAME);
        password = credProp.getProperty(PASSWORD).toCharArray();
    }

    private static Properties loadConfigFromLocalFile() {
        Properties properties = new Properties();
        try (InputStream in = new FileInputStream(FILE)) {
            properties.load(in);
        } catch (final IOException e) {
            logger.debug("cannot load configurations from local file");
        }
        return properties;
    }

    public static String getDatabaseName() {
        return database;
    }

    public static MongoCollection<Document> getCollection(String tableName) {
        return MongoDBFactory.getInstance().getCollection(tableName);
    }
}
