## Base Structure Logic

The `base` directory contains foundational code that supports the main functionality of your IoT system. Specifically, it includes the `mqtt_base.py` file, which defines the `MQTTController` class. This class is responsible for managing MQTT connections and operations, such as connecting to the broker, subscribing to topics, publishing messages, and handling disconnections.

### Key Components of `base/mqtt_base.py`:

- **`MQTTController` Class**: Manages MQTT client operations.
  - **Initialization**: Sets up the MQTT client with a specified client name and broker URL.
  - **Connect Method**: Connects the client to the MQTT broker and starts the loop.
  - **Subscribe Method**: Subscribes to a specified topic and sets a callback for incoming messages.
  - **Unsubscribe Method**: Unsubscribes from a specified topic.
  - **Publish Method**: Publishes messages to a specified topic.
  - **Stop Method**: Stops the MQTT client and disconnects from the broker.

### Device ABC

The `device_abc.py` file contains the `DeviceABC` class, which serves as an abstract base class for all devices in the IoT system. This class defines the common interface and behavior that all device classes must implement.

- **`DeviceABC` Class**: Abstract base class for devices.
  - **Initialization**: Sets up common attributes for devices.
  - **Abstract Methods**: Defines methods that must be implemented by subclasses, such as `read_data` and `execute_command`.

### Usage Logic

The `MQTTController` class provides a reusable interface for managing MQTT operations. By using this class, you can easily integrate MQTT communication into different parts of your IoT system without duplicating code. The class follows a modular design pattern, allowing you to:

1. **Initialize** the MQTT client with a unique client name and broker URL.
2. **Connect** to the MQTT broker and start the network loop.
3. **Subscribe** to topics and handle incoming messages with a callback function.
4. **Publish** messages to specific topics.
5. **Unsubscribe** from topics when they are no longer needed.
6. **Stop** the client and disconnect from the broker when shutting down.

This modular approach ensures that MQTT-related functionality is centralized and easily maintainable, promoting code reuse and reducing complexity.

### Design Patterns

- **Abstract Base Class (ABC)**: The `DeviceABC` class uses the ABC pattern to define a common interface for all devices. This ensures that all device classes implement the required methods, promoting consistency and code reuse.
- **Modular Design**: The `MQTTController` class follows a modular design pattern, encapsulating MQTT operations in a single class. This makes the code more maintainable and reusable across different parts of the IoT system.