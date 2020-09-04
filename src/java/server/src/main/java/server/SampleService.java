package server;

import io.grpc.stub.StreamObserver;
import sample.Sample.SampleRequest;
import sample.Sample.SampleResponse;

public class SampleService extends sample.SampleServiceGrpc.SampleServiceImplBase {
    @Override
    public void call(SampleRequest request,
        StreamObserver<SampleResponse> responseObserver) {
        SampleResponse.Builder builder = SampleResponse.newBuilder();
        System.out.println("request : " + request.getMessage());
        builder.setReply("reply for \"" + request.getMessage() + "\" (java)");
        SampleResponse response = builder.build();
        responseObserver.onNext(response);
        responseObserver.onCompleted();
    }
}
