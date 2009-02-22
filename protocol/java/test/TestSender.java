import poker_bot.PokerBot.Event;
import poker_bot.PokerBot.Action;

import poker_messaging.PokerMessaging;

class TestSender {
  public static void main(String[] args) throws Exception {
    System.err.println("Start this sender");
    
    Event.Builder message_builder = Event.newBuilder();
    message_builder.setType(Event.Type.JOIN);
    message_builder.setMessage("message 1");
    PokerMessaging.send_message(System.out, message_builder.build());
    
    Event.Builder message_builder2 = Event.newBuilder();
    message_builder2.setType(Event.Type.QUIT);
    message_builder2.setMessage("message 2");
    PokerMessaging.send_message(System.out, message_builder2.build());
    
    PokerMessaging.send_terminator(System.out);
  }
}

/*
import java.io.*;

class StdinParser {

    public static void main(String[] args) {
        byte[] byteBuf = new byte[4];

        System.out.print("Input 4 bytes to be parsed as a 32 bit Integer: ");
        try {
            DataInputStream dis = new DataInputStream(System.in);
            int givenInt = dis.readInt();

            System.out.println("I read " + givenInt + " from you.");                
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
*/

/*
import com.example.tutorial.AddressBookProtos.AddressBook;
import com.example.tutorial.AddressBookProtos.Person;
import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.InputStreamReader;
import java.io.IOException;
import java.io.PrintStream;

class AddPerson {
  // This function fills in a Person message based on user input.
  static Person PromptForAddress(BufferedReader stdin,
                                 PrintStream stdout) throws IOException {
    Person.Builder person = Person.newBuilder();

    stdout.print("Enter person ID: ");
    person.setId(Integer.valueOf(stdin.readLine()));

    stdout.print("Enter name: ");
    person.setName(stdin.readLine());

    stdout.print("Enter email address (blank for none): ");
    String email = stdin.readLine();
    if (email.length() > 0) {
      person.setEmail(email);
    }

    while (true) {
      stdout.print("Enter a phone number (or leave blank to finish): ");
      String number = stdin.readLine();
      if (number.length() == 0) {
        break;
      }

      Person.PhoneNumber.Builder phoneNumber =
        Person.PhoneNumber.newBuilder().setNumber(number);

      stdout.print("Is this a mobile, home, or work phone? ");
      String type = stdin.readLine();
      if (type.equals("mobile")) {
        phoneNumber.setType(Person.PhoneType.MOBILE);
      } else if (type.equals("home")) {
        phoneNumber.setType(Person.PhoneType.HOME);
      } else if (type.equals("work")) {
        phoneNumber.setType(Person.PhoneType.WORK);
      } else {
        stdout.println("Unknown phone type.  Using default.");
      }

      person.addPhone(phoneNumber);
    }

    return person.build();
  }

  // Main function:  Reads the entire address book from a file,
  //   adds one person based on user input, then writes it back out to the same
  //   file.
  public static void main(String[] args) throws Exception {
    if (args.length != 1) {
      System.err.println("Usage:  AddPerson ADDRESS_BOOK_FILE");
      System.exit(-1);
    }

    AddressBook.Builder addressBook = AddressBook.newBuilder();

    // Read the existing address book.
    try {
      addressBook.mergeFrom(new FileInputStream(args[0]));
    } catch (FileNotFoundException e) {
      System.out.println(args[0] + ": File not found.  Creating a new file.");
    }

    // Add an address.
    addressBook.addPerson(
      PromptForAddress(new BufferedReader(new InputStreamReader(System.in)),
                       System.out));

    // Write the new address book back to disk.
    FileOutputStream output = new FileOutputStream(args[0]);
    addressBook.build().writeTo(output);
    output.close();
  }
}*/