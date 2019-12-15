package restapidatabackend.service;

import de.tuIlmenau.gpsTracker.dao.ClientDeviceMessageDao;
import de.tuIlmenau.gpsTracker.dao.impl.ClientDeviceMessageMongoDao;
import de.tuIlmenau.gpsTracker.dbModel.ClientDeviceMessage;
import de.tuIlmenau.gpsTracker.dbModel.Coordinate;
import org.springframework.stereotype.Service;

import java.util.*;

@Service
public class ClientDeviceService {

    private ClientDeviceMessageDao clientDeviceMessageDao;


    public ClientDeviceService() {
        this.clientDeviceMessageDao = new ClientDeviceMessageMongoDao();
    }

    public List<ClientDeviceMessage> findAll() {
        return clientDeviceMessageDao.getAllRecords();
    }

    public ClientDeviceMessage findLast() {
        return clientDeviceMessageDao.getLast();
    }

    public ClientDeviceMessage findById(String id) {
        List<ClientDeviceMessage> records = clientDeviceMessageDao.getRecordByDeviceId(id);
        return records.isEmpty() ? null : records.get(0);
    }

    public List<String> findClientIDs() {
        List<ClientDeviceMessage> list = clientDeviceMessageDao.getAllRecords();

        Set<String> result = new HashSet<>();
        for (ClientDeviceMessage message : list) {
            result.add(message.getDevice().getId());
        }
        return new ArrayList<>(result);
    }

    public Map<String, List<Coordinate>> findLastCoords() {
        return clientDeviceMessageDao.getLastCoords();
    }

    public List<Coordinate> findLastCoordsByClientId(String id) {
        return clientDeviceMessageDao.getLastCoordsByDeviceId(id);
    }
}
