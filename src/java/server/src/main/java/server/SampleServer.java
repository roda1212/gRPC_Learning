/*
 * This Java source file was generated by the Gradle 'init' task.
 */
package server;

import java.io.IOException;

import io.grpc.Server;
import io.grpc.ServerBuilder;

public class SampleServer {
    public static void main(String[] args) throws IOException, InterruptedException {
        final int portNumber = 9999;
        Server server = ServerBuilder.forPort(portNumber)
                                .addService(new SampleService())
                                .build();
        server.start();
        System.out.println("server started");
        server.awaitTermination();
    }
}
