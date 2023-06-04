@0xb1a369fb149e7b07;

using Java = import "/capnp/java.capnp";
$Java.package("org.antlr.v4.runtime.instrument");
$Java.outerClassname("MurmurHashMessage");

struct MethodUpdateInt
{
    struct Input
    {
        hash @0 : Int32;
        value @1 : Int32;
    }

    input @0 : Input;
    output @1 : Int32;
}

struct MethodFinish
{
    struct Input
    {
        hash @0 : Int32;
        numberOfWords @1 : Int32;
    }

    input @0 : Input;
    output @1 : Int32;
}

struct MurmurHashMethods
{
    union 
    {
        updateInt @0 : MethodUpdateInt;
        finish @1 : MethodFinish;
    }
}