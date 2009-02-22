PROTOCOL_PATH := ../../../../protocol/java/protocol
LIB_PATH := ../../../../protocol/java/lib
MESSAGING_PATH := ../../../../protocol/java/messaging
JAR := dist/foldbot.jar

all:
	jar uf $(JAR) -C $(PROTOCOL_PATH) .
	jar uf $(JAR) -C $(LIB_PATH) .
	jar uf $(JAR) -C $(MESSAGING_PATH) .
