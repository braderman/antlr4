package org.antlr.v4.runtime.instrument;

import java.io.FileOutputStream;
import org.capnproto.MessageBuilder;

public class Instrument
{
    public static void writeMessage(MessageBuilder message)
	{
		try
		{
			java.io.FileOutputStream output = new java.io.FileOutputStream("/home/brian/test.dat", true);
			org.capnproto.SerializePacked.writeToUnbuffered(output.getChannel(), message);
			output.close();
		}
		catch (java.io.IOException e)
		{
		}
	}
}