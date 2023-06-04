@0x946ab19b2dba58e2;

using Java = import "/capnp/java.capnp";
$Java.package("org.antlr.v4.runtime.instrument");
$Java.outerClassname("IntervalMessage");

struct Interval
{
    a @0 : Int32;
    b @1 : Int32;
}

struct MethodOf
{
    input @0 : Interval;
    output @1 : Interval;
}

struct MethodStateIntOut
{
    state @0 : Interval;
    output @1 : Int32; 
}
struct MethodStateStringOut
{
    state @0 : Interval;
    output @1 : Text;
}

struct MethodStateIntervalInBoolOut
{
    state @0 : Interval;
    input @1 : Interval;
    output @2 : Bool;
}

struct MethodStateIntervalInIntervalOut
{
    state @0 : Interval;
    input @1 : Interval;
    output @2 : Interval;   
}

struct IntervalMethods
{
    union 
    {
        intervalOf @0 : MethodOf;
        length @1 : MethodStateIntOut;
        hashCode @2 : MethodStateIntOut;
        startsBeforeDisjoint @3 : MethodStateIntervalInBoolOut;
        startsBeforeNonDisjoint @4 : MethodStateIntervalInBoolOut;
        startsAfter @5 : MethodStateIntervalInBoolOut;
        startsAfterDisjoint @6 : MethodStateIntervalInBoolOut;
        startsAfterNonDisjoint @7 : MethodStateIntervalInBoolOut;
        disjoint @8 : MethodStateIntervalInBoolOut;
        adjacent @9 : MethodStateIntervalInBoolOut;
        properlyContains @10 : MethodStateIntervalInBoolOut;
        methUnion @11 : MethodStateIntervalInIntervalOut;
        intersection @12 : MethodStateIntervalInIntervalOut;
        differenceNotProperlyContained @13 : MethodStateIntervalInIntervalOut;
        toString @14 : MethodStateStringOut;
    }
}