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

// make sure generated code does not produce name collisions with predefined keywords
namespace delphi SysUtils

const i32 integer = 42

service deprecate_included_inner {
  void Foo( ) ( deprecated = "This method has neither 'x' nor \"y\"" )
  void Bar( ) ( deprecated = "Fails to deliver 中文 колбаса" )
  void Baz( ) ( deprecated = "Need this to work with tabs (\t) or Umlauts (äöüÄÖÜß) too" )
  void Deprecated() ( deprecated ) // no comment
}

// EOF
