# Mock server

This is a python server serving as mock in order to help developping the controller application

Just run the "mock_communication.py" script in order to launch the server

## Scenario

The server will replicate a global "manual control" scenario where :

 - The app send a ack command
 - The server answers it
 - The app send a START_DRONE command
 - The server answers it (positively)
 - While the drone send messages to the server, the server send it to the app too
  > Those messages are not treated (only printed), except for those which need an answer