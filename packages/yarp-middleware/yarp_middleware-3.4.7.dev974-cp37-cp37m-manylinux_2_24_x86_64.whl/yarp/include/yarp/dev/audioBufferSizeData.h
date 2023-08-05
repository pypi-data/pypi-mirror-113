/*
 * SPDX-FileCopyrightText: 2006-2021 Istituto Italiano di Tecnologia (IIT)
 * SPDX-License-Identifier: BSD-3-Clause
 */

// Autogenerated by Thrift Compiler (0.14.1-yarped)
//
// This is an automatically generated file.
// It could get re-generated if the ALLOW_IDL_GENERATION flag is on.

#ifndef YARP_THRIFT_GENERATOR_STRUCT_AUDIOBUFFERSIZEDATA_H
#define YARP_THRIFT_GENERATOR_STRUCT_AUDIOBUFFERSIZEDATA_H

#include <yarp/dev/api.h>

#include <yarp/os/Wire.h>
#include <yarp/os/idl/WireTypes.h>

namespace yarp {
namespace dev {

class YARP_dev_API audioBufferSizeData :
        public yarp::os::idl::WirePortable
{
public:
    // Fields
    std::int32_t m_samples;
    std::int32_t m_channels;
    std::int32_t m_depth;
    std::int32_t size;

    // Default constructor
    audioBufferSizeData();

    // Constructor with field values
    audioBufferSizeData(const std::int32_t m_samples,
                        const std::int32_t m_channels,
                        const std::int32_t m_depth,
                        const std::int32_t size);

    // Read structure on a Wire
    bool read(yarp::os::idl::WireReader& reader) override;

    // Read structure on a Connection
    bool read(yarp::os::ConnectionReader& connection) override;

    // Write structure on a Wire
    bool write(const yarp::os::idl::WireWriter& writer) const override;

    // Write structure on a Connection
    bool write(yarp::os::ConnectionWriter& connection) const override;

    // Convert to a printable string
    std::string toString() const;

    // If you want to serialize this class without nesting, use this helper
    typedef yarp::os::idl::Unwrapped<audioBufferSizeData> unwrapped;

    class Editor :
            public yarp::os::Wire,
            public yarp::os::PortWriter
    {
    public:
        // Editor: default constructor
        Editor();

        // Editor: constructor with base class
        Editor(audioBufferSizeData& obj);

        // Editor: destructor
        ~Editor() override;

        // Editor: Deleted constructors and operator=
        Editor(const Editor& rhs) = delete;
        Editor(Editor&& rhs) = delete;
        Editor& operator=(const Editor& rhs) = delete;
        Editor& operator=(Editor&& rhs) = delete;

        // Editor: edit
        bool edit(audioBufferSizeData& obj, bool dirty = true);

        // Editor: validity check
        bool isValid() const;

        // Editor: state
        audioBufferSizeData& state();

        // Editor: start editing
        void start_editing();

#ifndef YARP_NO_DEPRECATED // Since YARP 3.2
        YARP_DEPRECATED_MSG("Use start_editing() instead")
        void begin()
        {
            start_editing();
        }
#endif // YARP_NO_DEPRECATED

        // Editor: stop editing
        void stop_editing();

#ifndef YARP_NO_DEPRECATED // Since YARP 3.2
        YARP_DEPRECATED_MSG("Use stop_editing() instead")
        void end()
        {
            stop_editing();
        }
#endif // YARP_NO_DEPRECATED

        // Editor: m_samples field
        void set_m_samples(const std::int32_t m_samples);
        std::int32_t get_m_samples() const;
        virtual bool will_set_m_samples();
        virtual bool did_set_m_samples();

        // Editor: m_channels field
        void set_m_channels(const std::int32_t m_channels);
        std::int32_t get_m_channels() const;
        virtual bool will_set_m_channels();
        virtual bool did_set_m_channels();

        // Editor: m_depth field
        void set_m_depth(const std::int32_t m_depth);
        std::int32_t get_m_depth() const;
        virtual bool will_set_m_depth();
        virtual bool did_set_m_depth();

        // Editor: size field
        void set_size(const std::int32_t size);
        std::int32_t get_size() const;
        virtual bool will_set_size();
        virtual bool did_set_size();

        // Editor: clean
        void clean();

        // Editor: read
        bool read(yarp::os::ConnectionReader& connection) override;

        // Editor: write
        bool write(yarp::os::ConnectionWriter& connection) const override;

    private:
        // Editor: state
        audioBufferSizeData* obj;
        bool obj_owned;
        int group;

        // Editor: dirty variables
        bool is_dirty;
        bool is_dirty_m_samples;
        bool is_dirty_m_channels;
        bool is_dirty_m_depth;
        bool is_dirty_size;
        int dirty_count;

        // Editor: send if possible
        void communicate();

        // Editor: mark dirty overall
        void mark_dirty();

        // Editor: mark dirty single fields
        void mark_dirty_m_samples();
        void mark_dirty_m_channels();
        void mark_dirty_m_depth();
        void mark_dirty_size();

        // Editor: dirty_flags
        void dirty_flags(bool flag);
    };

private:
    // read/write m_samples field
    bool read_m_samples(yarp::os::idl::WireReader& reader);
    bool write_m_samples(const yarp::os::idl::WireWriter& writer) const;
    bool nested_read_m_samples(yarp::os::idl::WireReader& reader);
    bool nested_write_m_samples(const yarp::os::idl::WireWriter& writer) const;

    // read/write m_channels field
    bool read_m_channels(yarp::os::idl::WireReader& reader);
    bool write_m_channels(const yarp::os::idl::WireWriter& writer) const;
    bool nested_read_m_channels(yarp::os::idl::WireReader& reader);
    bool nested_write_m_channels(const yarp::os::idl::WireWriter& writer) const;

    // read/write m_depth field
    bool read_m_depth(yarp::os::idl::WireReader& reader);
    bool write_m_depth(const yarp::os::idl::WireWriter& writer) const;
    bool nested_read_m_depth(yarp::os::idl::WireReader& reader);
    bool nested_write_m_depth(const yarp::os::idl::WireWriter& writer) const;

    // read/write size field
    bool read_size(yarp::os::idl::WireReader& reader);
    bool write_size(const yarp::os::idl::WireWriter& writer) const;
    bool nested_read_size(yarp::os::idl::WireReader& reader);
    bool nested_write_size(const yarp::os::idl::WireWriter& writer) const;
};

} // namespace yarp
} // namespace dev

#endif // YARP_THRIFT_GENERATOR_STRUCT_AUDIOBUFFERSIZEDATA_H
