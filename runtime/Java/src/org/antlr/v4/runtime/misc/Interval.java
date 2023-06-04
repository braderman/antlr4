/*
 * Copyright (c) 2012-2017 The ANTLR Project. All rights reserved.
 * Use of this file is governed by the BSD 3-clause license that
 * can be found in the LICENSE.txt file in the project root.
 */
package org.antlr.v4.runtime.misc;

import java.io.FileOutputStream;
import org.antlr.v4.runtime.instrument.IntervalMessage;
import org.antlr.v4.runtime.instrument.Instrument;
import org.capnproto.MessageBuilder;

/** An immutable inclusive interval a..b */
public class Interval {
	public static final int INTERVAL_POOL_MAX_VALUE = 1000;

	public static final Interval INVALID = new Interval(-1,-2);

	static final Interval[] cache = new Interval[INTERVAL_POOL_MAX_VALUE+1];

	public int a;
	public int b;

	public Interval(int a, int b) { this.a=a; this.b=b; }

	/** Interval objects are used readonly so share all with the
	 *  same single value a==b up to some max size.  Use an array as a perfect hash.
	 *  Return shared object for 0..INTERVAL_POOL_MAX_VALUE or a new
	 *  Interval object with a..a in it.  On Java.g4, 218623 IntervalSets
	 *  have a..a (set with 1 element).
	 */
	public static Interval of(int a, int b) {
		// cache just a..a
		if ( a!=b || a<0 || a>INTERVAL_POOL_MAX_VALUE ) {
			return new Interval(a,b);
		}
		if ( cache[a]==null ) {
			cache[a] = new Interval(a,a);
		}

		return cache[a];
	}

	/** return number of elements between a and b inclusively. x..x is length 1.
	 *  if b &lt; a, then length is 0.  9..10 has length 2.
	 */
	public int length() {
		var message = new MessageBuilder();
		var methods = message.initRoot(IntervalMessage.IntervalMethods.factory);
		var method = methods.initLength();
		var state = method.initState();
		state.setA(this.a);
		state.setB(this.b);

		if ( b<a )
		{ 
			method.setOutput(0);
			Instrument.writeMessage(message);
			return 0;
		}

		var length = b-a+1;
		method.setOutput(length);
		Instrument.writeMessage(message);

		return length;
	}

	@Override
	public boolean equals(Object o) {
		if ( o==null || !(o instanceof Interval) ) {
			return false;
		}
		Interval other = (Interval)o;
		return this.a==other.a && this.b==other.b;
	}

	@Override
	public int hashCode() {
		var message = new MessageBuilder();
		var methods = message.initRoot(IntervalMessage.IntervalMethods.factory);
		var method = methods.initHashCode();
		var state = method.initState();
		state.setA(this.a);
		state.setB(this.b);

		int hash = 23;
		hash = hash * 31 + a;
		hash = hash * 31 + b;

		method.setOutput(hash);
		Instrument.writeMessage(message);

		return hash;
	}

	/** Does this start completely before other? Disjoint */
	public boolean startsBeforeDisjoint(Interval other) {
		var retVal = this.a<other.a && this.b<other.a;
		return retVal;
	}

	/** Does this start at or before other? Nondisjoint */
	public boolean startsBeforeNonDisjoint(Interval other) {
		var message = new MessageBuilder();
		var methods = message.initRoot(IntervalMessage.IntervalMethods.factory);
		var method = methods.initStartsBeforeNonDisjoint();
		var state = method.initState();
		state.setA(this.a);
		state.setB(this.b);
		var input = method.initInput();
		input.setA(other.a);
		input.setB(other.b);

		var retVal = this.a<=other.a && this.b>=other.a;

		method.setOutput(retVal);
		Instrument.writeMessage(message);

		return retVal;
	}

	/** Does this.a start after other.b? May or may not be disjoint */
	public boolean startsAfter(Interval other) 
	{ 
		var message = new MessageBuilder();
		var methods = message.initRoot(IntervalMessage.IntervalMethods.factory);
		var method = methods.initStartsAfter();
		var state = method.initState();
		state.setA(this.a);
		state.setB(this.b);
		var input = method.initInput();
		input.setA(other.a);
		input.setB(other.b);

		var retVal = this.a>other.a;

		method.setOutput(retVal);
		Instrument.writeMessage(message);

		return retVal; 
	}

	/** Does this start completely after other? Disjoint */
	public boolean startsAfterDisjoint(Interval other) {
		var retVal = this.a>other.b;
		return retVal;
	}

	/** Does this start after other? NonDisjoint */
	public boolean startsAfterNonDisjoint(Interval other) {
		var message = new MessageBuilder();
		var methods = message.initRoot(IntervalMessage.IntervalMethods.factory);
		var method = methods.initStartsAfterNonDisjoint();
		var state = method.initState();
		state.setA(this.a);
		state.setB(this.b);
		var input = method.initInput();
		input.setA(other.a);
		input.setB(other.b);

		var retVal = this.a>other.a && this.a<=other.b; // this.b>=other.b implied

		method.setOutput(retVal);
		Instrument.writeMessage(message);

		return retVal;
	}

	/** Are both ranges disjoint? I.e., no overlap? */
	public boolean disjoint(Interval other) {
		var retVal = startsBeforeDisjoint(other) || startsAfterDisjoint(other);
		return retVal;
	}

	/** Are two intervals adjacent such as 0..41 and 42..42? */
	public boolean adjacent(Interval other) {
		var retVal = this.a == other.b+1 || this.b == other.a-1;
		return retVal;
	}

	public boolean properlyContains(Interval other) {
		var message = new MessageBuilder();
		var methods = message.initRoot(IntervalMessage.IntervalMethods.factory);
		var method = methods.initProperlyContains();
		var state = method.initState();
		state.setA(this.a);
		state.setB(this.b);
		var input = method.initInput();
		input.setA(other.a);
		input.setB(other.b);

		var retVal = other.a >= this.a && other.b <= this.b;

		method.setOutput(retVal);
		Instrument.writeMessage(message);

		return retVal;
	}

	/** Return the interval computed from combining this and other */
	public Interval union(Interval other) {
		var retVal = Interval.of(Math.min(a, other.a), Math.max(b, other.b));
		return retVal;
	}

	/** Return the interval in common between this and o */
	public Interval intersection(Interval other) {
		var message = new MessageBuilder();
		var methods = message.initRoot(IntervalMessage.IntervalMethods.factory);
		var method = methods.initIntersection();
		var state = method.initState();
		state.setA(this.a);
		state.setB(this.b);
		var input = method.initInput();
		input.setA(other.a);
		input.setB(other.b);
		var output = method.initOutput();

		var retVal = Interval.of(Math.max(a, other.a), Math.min(b, other.b));

		output.setA(retVal.a);
		output.setB(retVal.b);
		Instrument.writeMessage(message);

		return retVal;
	}

	/** Return the interval with elements from this not in other;
	 *  other must not be totally enclosed (properly contained)
	 *  within this, which would result in two disjoint intervals
	 *  instead of the single one returned by this method.
	 */
	public Interval differenceNotProperlyContained(Interval other) {
		Interval diff = null;
		// other.a to left of this.a (or same)
		if ( other.startsBeforeNonDisjoint(this) ) {
			diff = Interval.of(Math.max(this.a, other.b + 1),
							   this.b);
		}

		// other.a to right of this.a
		else if ( other.startsAfterNonDisjoint(this) ) {
			diff = Interval.of(this.a, other.a - 1);
		}

		var message = new MessageBuilder();
		var methods = message.initRoot(IntervalMessage.IntervalMethods.factory);
		var method = methods.initDifferenceNotProperlyContained();
		var state = method.initState();
		state.setA(this.a);
		state.setB(this.b);
		var input = method.initInput();
		input.setA(other.a);
		input.setB(other.b);
		var output = method.initOutput();

		output.setA(diff.a);
		output.setB(diff.b);
		Instrument.writeMessage(message);

		return diff;
	}

	@Override
	public String toString() {
		var message = new MessageBuilder();
		var methods = message.initRoot(IntervalMessage.IntervalMethods.factory);
		var method = methods.initToString();
		var state = method.initState();
		state.setA(this.a);
		state.setB(this.b);

		var retVal = a+".."+b;

		method.setOutput(retVal);
		Instrument.writeMessage(message);

		return retVal;
	}
}
