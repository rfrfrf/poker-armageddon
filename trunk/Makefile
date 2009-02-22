PROTOCOLS := protocol/cpp/protocol protocol/java/protocol protocol/python/protocol

protocols:
	mkdir -p $(PROTOCOLS)
	protoc protocol/poker_bot.proto --cpp_out=protocol/cpp --java_out=protocol/java/protocol --python_out=protocol/python
	touch protocol/python/protocol/__init__.py

clean:
	rm -f -r $(PROTOCOLS) **/*.pyc **/*.class **/*.o
	#rm -f -r protocol/cpp/protocol/* protocol/java/protocol/* protocol/python/protocol/* **/*.pyc **/*.class **/*.o
