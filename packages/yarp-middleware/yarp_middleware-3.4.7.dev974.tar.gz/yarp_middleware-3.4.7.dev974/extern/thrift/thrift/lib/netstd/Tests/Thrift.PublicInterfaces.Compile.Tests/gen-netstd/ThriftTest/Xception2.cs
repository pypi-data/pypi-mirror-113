/**
 * Autogenerated by Thrift Compiler (0.14.0)
 *
 * DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
 *  @generated
 */
using System;
using System.Collections;
using System.Collections.Generic;
using System.Text;
using System.IO;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.Extensions.Logging;
using Thrift;
using Thrift.Collections;
using System.ServiceModel;
using System.Runtime.Serialization;

using Thrift.Protocol;
using Thrift.Protocol.Entities;
using Thrift.Protocol.Utilities;
using Thrift.Transport;
using Thrift.Transport.Client;
using Thrift.Transport.Server;
using Thrift.Processor;


#pragma warning disable IDE0079  // remove unnecessary pragmas
#pragma warning disable IDE1006  // parts of the code use IDL spelling

namespace ThriftTest
{

public partial class Xception2 : TException, TBase
{
  private int _errorCode;
  private global::ThriftTest.Xtruct _struct_thing;

  [DataMember(Order = 0)]
  public int ErrorCode
  {
    get
    {
      return _errorCode;
    }
    set
    {
      __isset.errorCode = true;
      this._errorCode = value;
    }
  }

  [DataMember(Order = 0)]
  public global::ThriftTest.Xtruct Struct_thing
  {
    get
    {
      return _struct_thing;
    }
    set
    {
      __isset.struct_thing = true;
      this._struct_thing = value;
    }
  }


  [DataMember(Order = 1)]
  public Isset __isset;
  [DataContract]
  public struct Isset
  {
    [DataMember]
    public bool errorCode;
    [DataMember]
    public bool struct_thing;
  }

  #region XmlSerializer support

  public bool ShouldSerializeErrorCode()
  {
    return __isset.errorCode;
  }

  public bool ShouldSerializeStruct_thing()
  {
    return __isset.struct_thing;
  }

  #endregion XmlSerializer support

  public Xception2()
  {
  }

  public Xception2 DeepCopy()
  {
    var tmp65 = new Xception2();
    if(__isset.errorCode)
    {
      tmp65.ErrorCode = this.ErrorCode;
    }
    tmp65.__isset.errorCode = this.__isset.errorCode;
    if((Struct_thing != null) && __isset.struct_thing)
    {
      tmp65.Struct_thing = (global::ThriftTest.Xtruct)this.Struct_thing.DeepCopy();
    }
    tmp65.__isset.struct_thing = this.__isset.struct_thing;
    return tmp65;
  }

  public async global::System.Threading.Tasks.Task ReadAsync(TProtocol iprot, CancellationToken cancellationToken)
  {
    iprot.IncrementRecursionDepth();
    try
    {
      TField field;
      await iprot.ReadStructBeginAsync(cancellationToken);
      while (true)
      {
        field = await iprot.ReadFieldBeginAsync(cancellationToken);
        if (field.Type == TType.Stop)
        {
          break;
        }

        switch (field.ID)
        {
          case 1:
            if (field.Type == TType.I32)
            {
              ErrorCode = await iprot.ReadI32Async(cancellationToken);
            }
            else
            {
              await TProtocolUtil.SkipAsync(iprot, field.Type, cancellationToken);
            }
            break;
          case 2:
            if (field.Type == TType.Struct)
            {
              Struct_thing = new global::ThriftTest.Xtruct();
              await Struct_thing.ReadAsync(iprot, cancellationToken);
            }
            else
            {
              await TProtocolUtil.SkipAsync(iprot, field.Type, cancellationToken);
            }
            break;
          default: 
            await TProtocolUtil.SkipAsync(iprot, field.Type, cancellationToken);
            break;
        }

        await iprot.ReadFieldEndAsync(cancellationToken);
      }

      await iprot.ReadStructEndAsync(cancellationToken);
    }
    finally
    {
      iprot.DecrementRecursionDepth();
    }
  }

  public async global::System.Threading.Tasks.Task WriteAsync(TProtocol oprot, CancellationToken cancellationToken)
  {
    oprot.IncrementRecursionDepth();
    try
    {
      var struc = new TStruct("Xception2");
      await oprot.WriteStructBeginAsync(struc, cancellationToken);
      var field = new TField();
      if(__isset.errorCode)
      {
        field.Name = "errorCode";
        field.Type = TType.I32;
        field.ID = 1;
        await oprot.WriteFieldBeginAsync(field, cancellationToken);
        await oprot.WriteI32Async(ErrorCode, cancellationToken);
        await oprot.WriteFieldEndAsync(cancellationToken);
      }
      if((Struct_thing != null) && __isset.struct_thing)
      {
        field.Name = "struct_thing";
        field.Type = TType.Struct;
        field.ID = 2;
        await oprot.WriteFieldBeginAsync(field, cancellationToken);
        await Struct_thing.WriteAsync(oprot, cancellationToken);
        await oprot.WriteFieldEndAsync(cancellationToken);
      }
      await oprot.WriteFieldStopAsync(cancellationToken);
      await oprot.WriteStructEndAsync(cancellationToken);
    }
    finally
    {
      oprot.DecrementRecursionDepth();
    }
  }

  public override bool Equals(object that)
  {
    if (!(that is Xception2 other)) return false;
    if (ReferenceEquals(this, other)) return true;
    return ((__isset.errorCode == other.__isset.errorCode) && ((!__isset.errorCode) || (System.Object.Equals(ErrorCode, other.ErrorCode))))
      && ((__isset.struct_thing == other.__isset.struct_thing) && ((!__isset.struct_thing) || (System.Object.Equals(Struct_thing, other.Struct_thing))));
  }

  public override int GetHashCode() {
    int hashcode = 157;
    unchecked {
      if(__isset.errorCode)
      {
        hashcode = (hashcode * 397) + ErrorCode.GetHashCode();
      }
      if((Struct_thing != null) && __isset.struct_thing)
      {
        hashcode = (hashcode * 397) + Struct_thing.GetHashCode();
      }
    }
    return hashcode;
  }

  public override string ToString()
  {
    var sb = new StringBuilder("Xception2(");
    int tmp66 = 0;
    if(__isset.errorCode)
    {
      if(0 < tmp66++) { sb.Append(", "); }
      sb.Append("ErrorCode: ");
      ErrorCode.ToString(sb);
    }
    if((Struct_thing != null) && __isset.struct_thing)
    {
      if(0 < tmp66++) { sb.Append(", "); }
      sb.Append("Struct_thing: ");
      Struct_thing.ToString(sb);
    }
    sb.Append(')');
    return sb.ToString();
  }
}


[DataContract]
public partial class Xception2Fault
{
  private int _errorCode;
  private global::ThriftTest.Xtruct _struct_thing;

  [DataMember(Order = 0)]
  public int ErrorCode
  {
    get
    {
      return _errorCode;
    }
    set
    {
      this._errorCode = value;
    }
  }

  [DataMember(Order = 0)]
  public global::ThriftTest.Xtruct Struct_thing
  {
    get
    {
      return _struct_thing;
    }
    set
    {
      this._struct_thing = value;
    }
  }

}

}
