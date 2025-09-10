import py4j.GatewayServer;

/*
usage:
(1) javac -cp py4j-0.10.9.7.jar:. SpeechClient.java
(2) java -cp py4j-0.10.9.7.jar:. SpeechClient.java
*/

public class SpeechClient {
    // Method exposed to Python
    public String handleMessage(String message) {
        System.out.println("Java received: " + message);
        if (message != null && !message.trim().isEmpty()) {
            return "String accepted from Java...";
        } else {
            return "String not accepted from Java...";
        }
    }

    public static void main(String[] args) {
        SpeechClient app = new SpeechClient();
        GatewayServer server = new GatewayServer(app);
        server.start();
        System.out.println("Gateway Server Started");
    }
}

