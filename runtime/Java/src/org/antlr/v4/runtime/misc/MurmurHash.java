/*
 * Copyright (c) 2012-2017 The ANTLR Project. All rights reserved.
 * Use of this file is governed by the BSD 3-clause license that
 * can be found in the LICENSE.txt file in the project root.
 */

package org.antlr.v4.runtime.misc;

//import java.io.FileOutputStream;
//import org.antlr.v4.runtime.instrument.MurmurHashMessage;
//import org.capnproto.MessageBuilder;

/**
 *
 * @author Sam Harwell
 */
public final class MurmurHash {

	private static final int DEFAULT_SEED = 0;

	/**
	 * Initialize the hash using the default seed value.
	 *
	 * @return the intermediate hash value
	 */
	public static int initialize() {
		return initialize(DEFAULT_SEED);
	}

	/**
	 * Initialize the hash using the specified {@code seed}.
	 *
	 * @param seed the seed
	 * @return the intermediate hash value
	 */
	public static int initialize(int seed) {
		return seed;
	}

	/**
	 * Update the intermediate hash value for the next input {@code value}.
	 *
	 * @param hash the intermediate hash value
	 * @param value the value to add to the current hash
	 * @return the updated intermediate hash value
	 */
	public static int update(int hash, int value) {
		final int c1 = 0xCC9E2D51;
		final int c2 = 0x1B873593;
		final int r1 = 15;
		final int r2 = 13;
		final int m = 5;
		final int n = 0xE6546B64;

		// MessageBuilder message = new MessageBuilder();
		// MurmurHashMessage.MurmurHashMethods.Builder methods = message.initRoot(MurmurHashMessage.MurmurHashMethods.factory);
		// MurmurHashMessage.MethodUpdateInt.Builder updateInt = methods.initUpdateInt();
		// MurmurHashMessage.MethodUpdateInt.Input.Builder input = updateInt.initInput();
		// input.setHash(hash);
		// input.setValue(value);

		int k = value;
		k = k * c1;
		k = (k << r1) | (k >>> (32 - r1));
		k = k * c2;

		hash = hash ^ k;
		hash = (hash << r2) | (hash >>> (32 - r2));
		hash = hash * m + n;

		// updateInt.setOutput(hash);

		// try
		// {
		// 	java.io.FileOutputStream output = new java.io.FileOutputStream("/home/brian/test.dat", true);
		// 	org.capnproto.SerializePacked.writeToUnbuffered(output.getChannel(), message);
		// 	output.close();
		// }
		// catch (java.io.IOException e)
		// {
		// }
		
		return hash;
	}

	/**
	 * Update the intermediate hash value for the next input {@code value}.
	 *
	 * @param hash the intermediate hash value
	 * @param value the value to add to the current hash
	 * @return the updated intermediate hash value
	 */
	public static int update(int hash, Object value) {
		return update(hash, value != null ? value.hashCode() : 0);
	}

	/**
	 * Apply the final computation steps to the intermediate value {@code hash}
	 * to form the final result of the MurmurHash 3 hash function.
	 *
	 * @param hash the intermediate hash value
	 * @param numberOfWords the number of integer values added to the hash
	 * @return the final hash result
	 */
	public static int finish(int hash, int numberOfWords) {
		// MessageBuilder message = new MessageBuilder();
		// MurmurHashMessage.MurmurHashMethods.Builder methods = message.initRoot(MurmurHashMessage.MurmurHashMethods.factory);
		// MurmurHashMessage.MethodFinish.Builder finish = methods.initFinish();
		// MurmurHashMessage.MethodFinish.Input.Builder input = finish.initInput();
		// input.setHash(hash);
		// input.setNumberOfWords(numberOfWords);

		hash = hash ^ (numberOfWords * 4);
		hash = hash ^ (hash >>> 16);
		hash = hash * 0x85EBCA6B;
		hash = hash ^ (hash >>> 13);
		hash = hash * 0xC2B2AE35;
		hash = hash ^ (hash >>> 16);

		//finish.setOutput(hash);

		// try
		// {
		// 	java.io.FileOutputStream output = new java.io.FileOutputStream("/home/brian/test.dat", true);
		// 	org.capnproto.SerializePacked.writeToUnbuffered(output.getChannel(), message);
		// 	output.close();
		// }
		// catch (java.io.IOException e)
		// {
		// }

		return hash;
	}

	/**
	 * Utility function to compute the hash code of an array using the
	 * MurmurHash algorithm.
	 *
	 * @param <T> the array element type
	 * @param data the array data
	 * @param seed the seed for the MurmurHash algorithm
	 * @return the hash code of the data
	 */
	public static <T> int hashCode(T[] data, int seed) {
		int hash = initialize(seed);
		for (T value : data) {
			hash = update(hash, value);
		}

		hash = finish(hash, data.length);
		return hash;
	}

	private MurmurHash() {
	}
}
