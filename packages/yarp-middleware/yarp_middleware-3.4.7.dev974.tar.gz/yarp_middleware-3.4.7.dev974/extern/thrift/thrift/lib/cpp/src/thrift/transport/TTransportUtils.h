/*
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements. See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership. The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License. You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied. See the License for the
 * specific language governing permissions and limitations
 * under the License.
 */

#ifndef _THRIFT_TRANSPORT_TTRANSPORTUTILS_H_
#define _THRIFT_TRANSPORT_TTRANSPORTUTILS_H_ 1

#include <cstdlib>
#include <cstring>
#include <string>
#include <algorithm>
#include <thrift/transport/TTransport.h>
// Include the buffered transports that used to be defined here.
#include <thrift/transport/TBufferTransports.h>
#include <thrift/transport/TFileTransport.h>

namespace apache {
namespace thrift {
namespace transport {

/**
 * The null transport is a dummy transport that doesn't actually do anything.
 * It's sort of an analogy to /dev/null, you can never read anything from it
 * and it will let you write anything you want to it, though it won't actually
 * go anywhere.
 *
 */
class TNullTransport : public TVirtualTransport<TNullTransport> {
public:
  TNullTransport() = default;

  ~TNullTransport() override = default;

  bool isOpen() const override { return true; }

  void open() override {}

  void write(const uint8_t* /* buf */, uint32_t /* len */) { return; }
};

/**
 * TPipedTransport. This transport allows piping of a request from one
 * transport to another either when readEnd() or writeEnd(). The typical
 * use case for this is to log a request or a reply to disk.
 * The underlying buffer expands to a keep a copy of the entire
 * request/response.
 *
 */
class TPipedTransport : virtual public TTransport {
public:
  TPipedTransport(std::shared_ptr<TTransport> srcTrans, std::shared_ptr<TTransport> dstTrans,
                 std::shared_ptr<TConfiguration> config = nullptr)
    : TTransport(config),
      srcTrans_(srcTrans),
      dstTrans_(dstTrans),
      rBufSize_(512),
      rPos_(0),
      rLen_(0),
      wBufSize_(512),
      wLen_(0) {

    // default is to to pipe the request when readEnd() is called
    pipeOnRead_ = true;
    pipeOnWrite_ = false;

    rBuf_ = (uint8_t*)std::malloc(sizeof(uint8_t) * rBufSize_);
    if (rBuf_ == nullptr) {
      throw std::bad_alloc();
    }
    wBuf_ = (uint8_t*)std::malloc(sizeof(uint8_t) * wBufSize_);
    if (wBuf_ == nullptr) {
      throw std::bad_alloc();
    }
  }

  TPipedTransport(std::shared_ptr<TTransport> srcTrans,
                  std::shared_ptr<TTransport> dstTrans,
                  uint32_t sz,
                  std::shared_ptr<TConfiguration> config = nullptr)
    : TTransport(config),
      srcTrans_(srcTrans),
      dstTrans_(dstTrans),
      rBufSize_(512),
      rPos_(0),
      rLen_(0),
      wBufSize_(sz),
      wLen_(0) {

    rBuf_ = (uint8_t*)std::malloc(sizeof(uint8_t) * rBufSize_);
    if (rBuf_ == nullptr) {
      throw std::bad_alloc();
    }
    wBuf_ = (uint8_t*)std::malloc(sizeof(uint8_t) * wBufSize_);
    if (wBuf_ == nullptr) {
      throw std::bad_alloc();
    }
  }

  ~TPipedTransport() override {
    std::free(rBuf_);
    std::free(wBuf_);
  }

  bool isOpen() const override { return srcTrans_->isOpen(); }

  bool peek() override {
    if (rPos_ >= rLen_) {
      // Double the size of the underlying buffer if it is full
      if (rLen_ == rBufSize_) {
        rBufSize_ *= 2;
        auto * tmpBuf = (uint8_t*)std::realloc(rBuf_, sizeof(uint8_t) * rBufSize_);
	if (tmpBuf == nullptr) {
	  throw std::bad_alloc();
	}
	rBuf_ = tmpBuf;
      }

      // try to fill up the buffer
      rLen_ += srcTrans_->read(rBuf_ + rPos_, rBufSize_ - rPos_);
    }
    return (rLen_ > rPos_);
  }

  void open() override { srcTrans_->open(); }

  void close() override { srcTrans_->close(); }

  void setPipeOnRead(bool pipeVal) { pipeOnRead_ = pipeVal; }

  void setPipeOnWrite(bool pipeVal) { pipeOnWrite_ = pipeVal; }

  uint32_t read(uint8_t* buf, uint32_t len);

  uint32_t readEnd() override {

    if (pipeOnRead_) {
      dstTrans_->write(rBuf_, rPos_);
      dstTrans_->flush();
    }

    srcTrans_->readEnd();

    // If requests are being pipelined, copy down our read-ahead data,
    // then reset our state.
    int read_ahead = rLen_ - rPos_;
    uint32_t bytes = rPos_;
    memcpy(rBuf_, rBuf_ + rPos_, read_ahead);
    rPos_ = 0;
    rLen_ = read_ahead;

    return bytes;
  }

  void write(const uint8_t* buf, uint32_t len);

  uint32_t writeEnd() override {
    if (pipeOnWrite_) {
      dstTrans_->write(wBuf_, wLen_);
      dstTrans_->flush();
    }
    return wLen_;
  }

  void flush() override;

  std::shared_ptr<TTransport> getTargetTransport() { return dstTrans_; }

  /*
   * Override TTransport *_virt() functions to invoke our implementations.
   * We cannot use TVirtualTransport to provide these, since we need to inherit
   * virtually from TTransport.
   */
  uint32_t read_virt(uint8_t* buf, uint32_t len) override { return this->read(buf, len); }
  void write_virt(const uint8_t* buf, uint32_t len) override { this->write(buf, len); }

protected:
  std::shared_ptr<TTransport> srcTrans_;
  std::shared_ptr<TTransport> dstTrans_;

  uint8_t* rBuf_;
  uint32_t rBufSize_;
  uint32_t rPos_;
  uint32_t rLen_;

  uint8_t* wBuf_;
  uint32_t wBufSize_;
  uint32_t wLen_;

  bool pipeOnRead_;
  bool pipeOnWrite_;
};

/**
 * Wraps a transport into a pipedTransport instance.
 *
 */
class TPipedTransportFactory : public TTransportFactory {
public:
  TPipedTransportFactory() = default;
  TPipedTransportFactory(std::shared_ptr<TTransport> dstTrans) {
    initializeTargetTransport(dstTrans);
  }
  ~TPipedTransportFactory() override = default;

  /**
   * Wraps the base transport into a piped transport.
   */
  std::shared_ptr<TTransport> getTransport(std::shared_ptr<TTransport> srcTrans) override {
    return std::shared_ptr<TTransport>(new TPipedTransport(srcTrans, dstTrans_));
  }

  virtual void initializeTargetTransport(std::shared_ptr<TTransport> dstTrans) {
    if (dstTrans_.get() == nullptr) {
      dstTrans_ = dstTrans;
    } else {
      throw TException("Target transport already initialized");
    }
  }

protected:
  std::shared_ptr<TTransport> dstTrans_;
};

/**
 * TPipedFileTransport. This is just like a TTransport, except that
 * it is a templatized class, so that clients who rely on a specific
 * TTransport can still access the original transport.
 *
 */
class TPipedFileReaderTransport : public TPipedTransport, public TFileReaderTransport {
public:
  TPipedFileReaderTransport(std::shared_ptr<TFileReaderTransport> srcTrans,
                            std::shared_ptr<TTransport> dstTrans,
                            std::shared_ptr<TConfiguration> config = nullptr);

  ~TPipedFileReaderTransport() override;

  // TTransport functions
  bool isOpen() const override;
  bool peek() override;
  void open() override;
  void close() override;
  uint32_t read(uint8_t* buf, uint32_t len);
  uint32_t readAll(uint8_t* buf, uint32_t len);
  uint32_t readEnd() override;
  void write(const uint8_t* buf, uint32_t len);
  uint32_t writeEnd() override;
  void flush() override;

  // TFileReaderTransport functions
  int32_t getReadTimeout() override;
  void setReadTimeout(int32_t readTimeout) override;
  uint32_t getNumChunks() override;
  uint32_t getCurChunk() override;
  void seekToChunk(int32_t chunk) override;
  void seekToEnd() override;

  /*
   * Override TTransport *_virt() functions to invoke our implementations.
   * We cannot use TVirtualTransport to provide these, since we need to inherit
   * virtually from TTransport.
   */
  uint32_t read_virt(uint8_t* buf, uint32_t len) override { return this->read(buf, len); }
  uint32_t readAll_virt(uint8_t* buf, uint32_t len) override { return this->readAll(buf, len); }
  void write_virt(const uint8_t* buf, uint32_t len) override { this->write(buf, len); }

protected:
  // shouldn't be used
  TPipedFileReaderTransport();
  std::shared_ptr<TFileReaderTransport> srcTrans_;
};

/**
 * Creates a TPipedFileReaderTransport from a filepath and a destination transport
 *
 */
class TPipedFileReaderTransportFactory : public TPipedTransportFactory {
public:
  TPipedFileReaderTransportFactory() = default;
  TPipedFileReaderTransportFactory(std::shared_ptr<TTransport> dstTrans)
    : TPipedTransportFactory(dstTrans) {}
  ~TPipedFileReaderTransportFactory() override = default;

  std::shared_ptr<TTransport> getTransport(std::shared_ptr<TTransport> srcTrans) override {
    std::shared_ptr<TFileReaderTransport> pFileReaderTransport
        = std::dynamic_pointer_cast<TFileReaderTransport>(srcTrans);
    if (pFileReaderTransport.get() != nullptr) {
      return getFileReaderTransport(pFileReaderTransport);
    } else {
      return std::shared_ptr<TTransport>();
    }
  }

  std::shared_ptr<TFileReaderTransport> getFileReaderTransport(
      std::shared_ptr<TFileReaderTransport> srcTrans) {
    return std::shared_ptr<TFileReaderTransport>(
        new TPipedFileReaderTransport(srcTrans, dstTrans_));
  }
};
}
}
} // apache::thrift::transport

#endif // #ifndef _THRIFT_TRANSPORT_TTRANSPORTUTILS_H_
