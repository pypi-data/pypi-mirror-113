#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements. See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership. The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the License for the
# specific language governing permissions and limitations
# under the License.
#

use 5.10.0;
use strict;
use warnings;

use Thrift;
use Thrift::Type;

package Thrift::TException;
use version 0.77; our $VERSION = version->declare("$Thrift::VERSION");

use overload '""' => sub {
    return
        sprintf '%s error: %s (code %s)',
          ref( $_[0] ),
          ( $_[0]->{message} || 'empty message' ),
          ( defined $_[0]->{code} ? $_[0]->{code} : 'undefined' );
    };

sub new {
    my $classname = shift;
    my $self = {message => shift, code => shift || 0};

    return bless($self,$classname);
}

package Thrift::TApplicationException;
use parent -norequire, 'Thrift::TException';
use version 0.77; our $VERSION = version->declare("$Thrift::VERSION");

use constant UNKNOWN                 => 0;
use constant UNKNOWN_METHOD          => 1;
use constant INVALID_MESSAGE_TYPE    => 2;
use constant WRONG_METHOD_NAME       => 3;
use constant BAD_SEQUENCE_ID         => 4;
use constant MISSING_RESULT          => 5;
use constant INTERNAL_ERROR          => 6;
use constant PROTOCOL_ERROR          => 7;
use constant INVALID_TRANSFORM       => 8;
use constant INVALID_PROTOCOL        => 9;
use constant UNSUPPORTED_CLIENT_TYPE => 10;

sub new {
    my $classname = shift;

    my $self = $classname->SUPER::new(@_);

    return bless($self,$classname);
}

sub read {
    my $self  = shift;
    my $input = shift;

    my $xfer  = 0;
    my $fname = undef;
    my $ftype = 0;
    my $fid   = 0;

    $xfer += $input->readStructBegin(\$fname);

    while (1)
    {
        $xfer += $input->readFieldBegin(\$fname, \$ftype, \$fid);
        if ($ftype == Thrift::TType::STOP) {
            last; next;
        }

      SWITCH: for($fid)
      {
          /1/ && do{

              if ($ftype == Thrift::TType::STRING) {
                  $xfer += $input->readString(\$self->{message});
              }
              else {
                  $xfer += $input->skip($ftype);
              }

              last;
          };

          /2/ && do{
              if ($ftype == Thrift::TType::I32) {
                  $xfer += $input->readI32(\$self->{code});
              }
              else {
                  $xfer += $input->skip($ftype);
              }
              last;
          };

          $xfer += $input->skip($ftype);
      }

      $xfer += $input->readFieldEnd();
    }
    $xfer += $input->readStructEnd();

    return $xfer;
}

sub write {
    my $self   = shift;
    my $output = shift;

    my $xfer   = 0;

    $xfer += $output->writeStructBegin('TApplicationException');

    if ($self->getMessage()) {
        $xfer += $output->writeFieldBegin('message', Thrift::TType::STRING, 1);
        $xfer += $output->writeString($self->getMessage());
        $xfer += $output->writeFieldEnd();
    }

    if ($self->getCode()) {
        $xfer += $output->writeFieldBegin('type', Thrift::TType::I32, 2);
        $xfer += $output->writeI32($self->getCode());
        $xfer += $output->writeFieldEnd();
    }

    $xfer += $output->writeFieldStop();
    $xfer += $output->writeStructEnd();

    return $xfer;
}

sub getMessage
{
    my $self = shift;

    return $self->{message};
}

sub getCode
{
    my $self = shift;

    return $self->{code};
}

1;
