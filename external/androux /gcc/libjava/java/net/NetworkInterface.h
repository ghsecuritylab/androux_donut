
// DO NOT EDIT THIS FILE - it is machine generated -*- c++ -*-

#ifndef __java_net_NetworkInterface__
#define __java_net_NetworkInterface__

#pragma interface

#include <java/lang/Object.h>
#include <gcj/array.h>

extern "Java"
{
  namespace java
  {
    namespace net
    {
        class InetAddress;
        class NetworkInterface;
    }
  }
}

class java::net::NetworkInterface : public ::java::lang::Object
{

public: // actually package-private
  NetworkInterface(::java::lang::String *, ::java::net::InetAddress *);
  NetworkInterface(::java::lang::String *, JArray< ::java::net::InetAddress * > *);
public:
  ::java::lang::String * getName();
  ::java::util::Enumeration * getInetAddresses();
  ::java::lang::String * getDisplayName();
  static ::java::net::NetworkInterface * getByName(::java::lang::String *);
  static ::java::net::NetworkInterface * getByInetAddress(::java::net::InetAddress *);
private:
  static ::java::util::Collection * condense(::java::util::Collection *);
public:
  static ::java::util::Enumeration * getNetworkInterfaces();
  jboolean equals(::java::lang::Object *);
  jint hashCode();
  ::java::lang::String * toString();
private:
  ::java::lang::String * __attribute__((aligned(__alignof__( ::java::lang::Object)))) name;
  ::java::util::Vector * inetAddresses;
public:
  static ::java::lang::Class class$;
};

#endif // __java_net_NetworkInterface__
