
// DO NOT EDIT THIS FILE - it is machine generated -*- c++ -*-

#ifndef __java_util_Hashtable$ValueEnumerator__
#define __java_util_Hashtable$ValueEnumerator__

#pragma interface

#include <java/lang/Object.h>

class java::util::Hashtable$ValueEnumerator : public ::java::lang::Object
{

public: // actually package-private
  Hashtable$ValueEnumerator(::java::util::Hashtable *);
public:
  jboolean hasMoreElements();
  ::java::lang::Object * nextElement();
private:
  ::java::util::Hashtable$EntryEnumerator * __attribute__((aligned(__alignof__( ::java::lang::Object)))) enumerator;
public: // actually package-private
  ::java::util::Hashtable * this$0;
public:
  static ::java::lang::Class class$;
};

#endif // __java_util_Hashtable$ValueEnumerator__