package restapidatabackend.web;

import de.tuIlmenau.gpsTracker.dbModel.ClientDeviceMessage;
import de.tuIlmenau.gpsTracker.dbModel.Coordinate;
import restapidatabackend.service.ClientDeviceService;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@RestController
public class UserController {

    private static Logger logger = LogManager.getLogger(UserController.class);

    @Autowired
    private ClientDeviceService clientDeviceService;


    /**
     * Get all messages
     * @return ResponseEntity<List<ClientDeviceMessage>>
     */
    @GetMapping("/messages/all")
    public ResponseEntity<List<ClientDeviceMessage>> getAllMessages() {
        List<ClientDeviceMessage> list = clientDeviceService.findAll();
        if (list == null) {
            logger.error("No messages found");
            return new ResponseEntity<>(new ArrayList<>(), HttpStatus.NOT_FOUND);
        }

        logger.info("Returned all messages");
        return new ResponseEntity<>(list, HttpStatus.FOUND);
    }


    /**
     * Get only last message
     * @return ResponseEntity<ClientDeviceMessage>
     */
    @GetMapping("/messages/last")
    public ResponseEntity<ClientDeviceMessage> getLastMessage() {
        ClientDeviceMessage message = clientDeviceService.findLast();
        if (message == null) {
            logger.error("No message found");
            return new ResponseEntity<>(new ClientDeviceMessage.Builder().build(), HttpStatus.NOT_FOUND);
        }

        logger.info("Returned last message");
        return new ResponseEntity<>(message, HttpStatus.FOUND);
    }


    /**
     * Get message by client device id
     * @param clientId - client device id
     * @return ResponseEntity<ClientDeviceMessage>
     */
    @GetMapping("/clients/{id}")
    public ResponseEntity<ClientDeviceMessage> getClientById(@PathVariable(value = "id") String clientId) {
        ClientDeviceMessage message = clientDeviceService.findById(clientId);
        if (message == null) {
            logger.error("No message found for specified client");
            return new ResponseEntity<>(new ClientDeviceMessage.Builder().build(), HttpStatus.NOT_FOUND);
        }

        logger.info("Returned message by client device id");
        return new ResponseEntity<>(message, HttpStatus.FOUND);
    }


    /**
     * Get all clients
     * @return ResponseEntity<List<String>>
     */
    @GetMapping("/clients/all")
    public ResponseEntity<List<String>> getAllClientId() {
        List<String> list = clientDeviceService.findClientIDs();
        if (list == null) {
            logger.error("No client IDs found");
            return new ResponseEntity<>(new ArrayList<>(), HttpStatus.NOT_FOUND);
        }

        logger.info("Returned all client IDs");
        return new ResponseEntity<>(list, HttpStatus.FOUND);
    }

    /**
     * Get all coordinates
     * @return ResponseEntity<Map<String, List<Coordinate>>>
     */
    @GetMapping("/messages/all/coords")
    public ResponseEntity<Map<String, List<Coordinate>>> getLastCoords() {
        Map<String, List<Coordinate>> list = clientDeviceService.findLastCoords();
        if (list == null) {
            logger.error("No coordinates found");
            return new ResponseEntity<>(new HashMap<>(), HttpStatus.NOT_FOUND);
        }

        logger.info("Returned all coordinates");
        return new ResponseEntity<>(list, HttpStatus.FOUND);
    }

    /**
     * Get all coordinates for client
     * @param clientId - client device id
     * @return List<Coordinate>
     */
    @GetMapping("/clients/{id}/coords")
    public ResponseEntity<List<Coordinate>> getLastCoordsByClientId(@PathVariable(value = "id") String clientId) {
        List<Coordinate> coords = clientDeviceService.findLastCoordsByClientId(clientId);
        if (coords == null) {
            logger.error("No coordinates found for client " + clientId);
            return new ResponseEntity<>(new ArrayList<>(), HttpStatus.NOT_FOUND);
        }

        logger.info("Returned all coordinates for client " + clientId);
        return new ResponseEntity<>(coords, HttpStatus.FOUND);
    }
}
