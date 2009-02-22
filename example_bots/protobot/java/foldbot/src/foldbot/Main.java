/*

A command-line bot, this is run as a process by the dealer and given messages
on stdin, while printing messages on stdout. The messages are created using
Google Protocol Buffers.

This bot takes command-line arguments of the form "initial_credits:10000",
supplied when the process is spawned. After that, the bot waits for a
'YOUR_TURN' Event message, at which point it runs the 'turn' function, and
prints the Action message to stdout and waits for the next YOUR_TURN message.

See protocol/poker_bot.proto for the entire protocol specification. See the
wiki for more information.

The Python side of this application is 'foldbot.py'

*/

package foldbot;

public class Main {
    public static void main(String[] args) {
        System.out.println("Input 4 bytes to be parsed as a 32 bit Integer: ");
    }

}
