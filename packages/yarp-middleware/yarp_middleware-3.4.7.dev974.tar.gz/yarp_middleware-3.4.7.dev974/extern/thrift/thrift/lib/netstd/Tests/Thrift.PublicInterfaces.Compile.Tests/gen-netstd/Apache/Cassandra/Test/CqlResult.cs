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

namespace Apache.Cassandra.Test
{

  [DataContract(Namespace="")]
  public partial class CqlResult : TBase
  {
    private List<global::Apache.Cassandra.Test.CqlRow> _rows;
    private int _num;
    private global::Apache.Cassandra.Test.CqlMetadata _schema;

    /// <summary>
    /// 
    /// <seealso cref="global::Apache.Cassandra.Test.CqlResultType"/>
    /// </summary>
    [DataMember(Order = 0)]
    public global::Apache.Cassandra.Test.CqlResultType Type { get; set; }

    [DataMember(Order = 0)]
    public List<global::Apache.Cassandra.Test.CqlRow> Rows
    {
      get
      {
        return _rows;
      }
      set
      {
        __isset.rows = true;
        this._rows = value;
      }
    }

    [DataMember(Order = 0)]
    public int Num
    {
      get
      {
        return _num;
      }
      set
      {
        __isset.num = true;
        this._num = value;
      }
    }

    [DataMember(Order = 0)]
    public global::Apache.Cassandra.Test.CqlMetadata Schema
    {
      get
      {
        return _schema;
      }
      set
      {
        __isset.schema = true;
        this._schema = value;
      }
    }


    [DataMember(Order = 1)]
    public Isset __isset;
    [DataContract]
    public struct Isset
    {
      [DataMember]
      public bool rows;
      [DataMember]
      public bool num;
      [DataMember]
      public bool schema;
    }

    #region XmlSerializer support

    public bool ShouldSerializeRows()
    {
      return __isset.rows;
    }

    public bool ShouldSerializeNum()
    {
      return __isset.num;
    }

    public bool ShouldSerializeSchema()
    {
      return __isset.schema;
    }

    #endregion XmlSerializer support

    public CqlResult()
    {
    }

    public CqlResult(global::Apache.Cassandra.Test.CqlResultType type) : this()
    {
      this.Type = type;
    }

    public CqlResult DeepCopy()
    {
      var tmp141 = new CqlResult();
      tmp141.Type = this.Type;
      if((Rows != null) && __isset.rows)
      {
        tmp141.Rows = this.Rows.DeepCopy();
      }
      tmp141.__isset.rows = this.__isset.rows;
      if(__isset.num)
      {
        tmp141.Num = this.Num;
      }
      tmp141.__isset.num = this.__isset.num;
      if((Schema != null) && __isset.schema)
      {
        tmp141.Schema = (global::Apache.Cassandra.Test.CqlMetadata)this.Schema.DeepCopy();
      }
      tmp141.__isset.schema = this.__isset.schema;
      return tmp141;
    }

    public async global::System.Threading.Tasks.Task ReadAsync(TProtocol iprot, CancellationToken cancellationToken)
    {
      iprot.IncrementRecursionDepth();
      try
      {
        bool isset_type = false;
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
                Type = (global::Apache.Cassandra.Test.CqlResultType)await iprot.ReadI32Async(cancellationToken);
                isset_type = true;
              }
              else
              {
                await TProtocolUtil.SkipAsync(iprot, field.Type, cancellationToken);
              }
              break;
            case 2:
              if (field.Type == TType.List)
              {
                {
                  TList _list142 = await iprot.ReadListBeginAsync(cancellationToken);
                  Rows = new List<global::Apache.Cassandra.Test.CqlRow>(_list142.Count);
                  for(int _i143 = 0; _i143 < _list142.Count; ++_i143)
                  {
                    global::Apache.Cassandra.Test.CqlRow _elem144;
                    _elem144 = new global::Apache.Cassandra.Test.CqlRow();
                    await _elem144.ReadAsync(iprot, cancellationToken);
                    Rows.Add(_elem144);
                  }
                  await iprot.ReadListEndAsync(cancellationToken);
                }
              }
              else
              {
                await TProtocolUtil.SkipAsync(iprot, field.Type, cancellationToken);
              }
              break;
            case 3:
              if (field.Type == TType.I32)
              {
                Num = await iprot.ReadI32Async(cancellationToken);
              }
              else
              {
                await TProtocolUtil.SkipAsync(iprot, field.Type, cancellationToken);
              }
              break;
            case 4:
              if (field.Type == TType.Struct)
              {
                Schema = new global::Apache.Cassandra.Test.CqlMetadata();
                await Schema.ReadAsync(iprot, cancellationToken);
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
        if (!isset_type)
        {
          throw new TProtocolException(TProtocolException.INVALID_DATA);
        }
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
        var struc = new TStruct("CqlResult");
        await oprot.WriteStructBeginAsync(struc, cancellationToken);
        var field = new TField();
        field.Name = "type";
        field.Type = TType.I32;
        field.ID = 1;
        await oprot.WriteFieldBeginAsync(field, cancellationToken);
        await oprot.WriteI32Async((int)Type, cancellationToken);
        await oprot.WriteFieldEndAsync(cancellationToken);
        if((Rows != null) && __isset.rows)
        {
          field.Name = "rows";
          field.Type = TType.List;
          field.ID = 2;
          await oprot.WriteFieldBeginAsync(field, cancellationToken);
          {
            await oprot.WriteListBeginAsync(new TList(TType.Struct, Rows.Count), cancellationToken);
            foreach (global::Apache.Cassandra.Test.CqlRow _iter145 in Rows)
            {
              await _iter145.WriteAsync(oprot, cancellationToken);
            }
            await oprot.WriteListEndAsync(cancellationToken);
          }
          await oprot.WriteFieldEndAsync(cancellationToken);
        }
        if(__isset.num)
        {
          field.Name = "num";
          field.Type = TType.I32;
          field.ID = 3;
          await oprot.WriteFieldBeginAsync(field, cancellationToken);
          await oprot.WriteI32Async(Num, cancellationToken);
          await oprot.WriteFieldEndAsync(cancellationToken);
        }
        if((Schema != null) && __isset.schema)
        {
          field.Name = "schema";
          field.Type = TType.Struct;
          field.ID = 4;
          await oprot.WriteFieldBeginAsync(field, cancellationToken);
          await Schema.WriteAsync(oprot, cancellationToken);
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
      if (!(that is CqlResult other)) return false;
      if (ReferenceEquals(this, other)) return true;
      return System.Object.Equals(Type, other.Type)
        && ((__isset.rows == other.__isset.rows) && ((!__isset.rows) || (TCollections.Equals(Rows, other.Rows))))
        && ((__isset.num == other.__isset.num) && ((!__isset.num) || (System.Object.Equals(Num, other.Num))))
        && ((__isset.schema == other.__isset.schema) && ((!__isset.schema) || (System.Object.Equals(Schema, other.Schema))));
    }

    public override int GetHashCode() {
      int hashcode = 157;
      unchecked {
        hashcode = (hashcode * 397) + Type.GetHashCode();
        if((Rows != null) && __isset.rows)
        {
          hashcode = (hashcode * 397) + TCollections.GetHashCode(Rows);
        }
        if(__isset.num)
        {
          hashcode = (hashcode * 397) + Num.GetHashCode();
        }
        if((Schema != null) && __isset.schema)
        {
          hashcode = (hashcode * 397) + Schema.GetHashCode();
        }
      }
      return hashcode;
    }

    public override string ToString()
    {
      var sb = new StringBuilder("CqlResult(");
      sb.Append(", Type: ");
      Type.ToString(sb);
      if((Rows != null) && __isset.rows)
      {
        sb.Append(", Rows: ");
        Rows.ToString(sb);
      }
      if(__isset.num)
      {
        sb.Append(", Num: ");
        Num.ToString(sb);
      }
      if((Schema != null) && __isset.schema)
      {
        sb.Append(", Schema: ");
        Schema.ToString(sb);
      }
      sb.Append(')');
      return sb.ToString();
    }
  }

}
