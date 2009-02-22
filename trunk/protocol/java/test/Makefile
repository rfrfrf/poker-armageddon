SOURCEPATH := ../../../protocol/java/protocol:../../../protocol/java/lib

all: test_sender test_receiver

test_sender: TestSender.class
	jar cfm test_sender.jar TestSenderManifest.txt TestSender.class

test_receiver: TestReceiver.class
	jar cfm test_receiver.jar TestReceiverManifest.txt TestReceiver.class

%.class: %.java
	javac -sourcepath $(SOURCEPATH) $<

clean:
	rm -f *.class *.jar
