// Licensed to the Apache Software Foundation(ASF) under one
// or more contributor license agreements.See the NOTICE file
// distributed with this work for additional information
// regarding copyright ownership.The ASF licenses this file
// to you under the Apache License, Version 2.0 (the
// "License"); you may not use this file except in compliance
// with the License. You may obtain a copy of the License at
// 
//     http://www.apache.org/licenses/LICENSE-2.0
// 
// Unless required by applicable law or agreed to in writing,
// software distributed under the License is distributed on an
// "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
// KIND, either express or implied. See the License for the
// specific language governing permissions and limitations
// under the License.

using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net.Security;
using System.Security.Cryptography.X509Certificates;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Logging;
using Thrift;
using Thrift.Protocol;
using Thrift.Server;
using Thrift.Transport;
using Thrift.Transport.Server;
using tutorial;
using shared;
using Thrift.Processor;
using System.Diagnostics;

namespace Server
{
    public class Program
    {
        private static ServiceCollection ServiceCollection = new ServiceCollection();
        private static ILogger Logger;
        private static readonly TConfiguration Configuration = null;  // new TConfiguration() if  needed

        public static void Main(string[] args)
        {
            args = args ?? new string[0];

            ServiceCollection.AddLogging(logging => ConfigureLogging(logging));
            using (var serviceProvider = ServiceCollection.BuildServiceProvider())
            {
                Logger = serviceProvider.GetService<ILoggerFactory>().CreateLogger(nameof(Server));

                if (args.Any(x => x.StartsWith("-help", StringComparison.OrdinalIgnoreCase)))
                {
                    DisplayHelp();
                    return;
                }

                using (var source = new CancellationTokenSource())
                {
                    RunAsync(args, source.Token).GetAwaiter().GetResult();

                    Logger.LogInformation("Press any key to stop...");

                    Console.ReadLine();
                    source.Cancel();
                }

                Logger.LogInformation("Server stopped");
            }
        }

        private static void ConfigureLogging(ILoggingBuilder logging)
        {
            logging.SetMinimumLevel(LogLevel.Trace);
            logging.AddConsole();
            logging.AddDebug();
        }

        private static void DisplayHelp()
        {
            Logger.LogInformation(@"
Usage: 
    Server -help
        will diplay help information 

    Server -tr:<transport> -bf:<buffering> -pr:<protocol>
        will run server with specified arguments (tcp transport, no buffering, and binary protocol by default)

Options:
    -tr (transport): 
        tcp - (default) tcp transport will be used (host - ""localhost"", port - 9090)
        namedpipe - namedpipe transport will be used (pipe address - "".test"")
        http - http transport will be used (http address - ""localhost:9090"")
        tcptls - tcp transport with tls will be used (host - ""localhost"", port - 9090)

    -bf (buffering): 
        none - (default) no buffering will be used
        buffered - buffered transport will be used
        framed - framed transport will be used

    -pr (protocol): 
        binary - (default) binary protocol will be used
        compact - compact protocol will be used
        json - json protocol will be used
        multiplexed - multiplexed protocol will be used

Sample:
    Server -tr:tcp
");
        }

        private static async Task RunAsync(string[] args, CancellationToken cancellationToken)
        {
            var selectedTransport = GetTransport(args);
            var selectedBuffering = GetBuffering(args);
            var selectedProtocol = GetProtocol(args);

            if (selectedTransport == Transport.Http)
            {
                new HttpServerSample().Run(cancellationToken);
            }
            else
            {
                await RunSelectedConfigurationAsync(selectedTransport, selectedBuffering, selectedProtocol, cancellationToken);
            }
        }

        private static Protocol GetProtocol(string[] args)
        {
            var transport = args.FirstOrDefault(x => x.StartsWith("-pr"))?.Split(':')?[1];

            Enum.TryParse(transport, true, out Protocol selectedProtocol);

            return selectedProtocol;
        }

        private static Buffering GetBuffering(string[] args)
        {
            var buffering = args.FirstOrDefault(x => x.StartsWith("-bf"))?.Split(":")?[1];

            Enum.TryParse<Buffering>(buffering, out var selectedBuffering);

            return selectedBuffering;
        }

        private static Transport GetTransport(string[] args)
        {
            var transport = args.FirstOrDefault(x => x.StartsWith("-tr"))?.Split(':')?[1];

            Enum.TryParse(transport, true, out Transport selectedTransport);

            return selectedTransport;
        }

        private static async Task RunSelectedConfigurationAsync(Transport transport, Buffering buffering, Protocol protocol, CancellationToken cancellationToken)
        {
            var handler = new CalculatorAsyncHandler();

            TServerTransport serverTransport = null;
            switch (transport)
            {
                case Transport.Tcp:
                    serverTransport = new TServerSocketTransport(9090, Configuration);
                    break;
                case Transport.NamedPipe:
                    serverTransport = new TNamedPipeServerTransport(".test", Configuration);
                    break;
                case Transport.TcpTls:
                    serverTransport = new TTlsServerSocketTransport(9090, Configuration,
                        GetCertificate(), ClientCertValidator, LocalCertificateSelectionCallback);
                    break;
            }

            TTransportFactory inputTransportFactory = null;
            TTransportFactory outputTransportFactory = null;
            switch (buffering)
            {
                case Buffering.Buffered:
                    inputTransportFactory = new TBufferedTransport.Factory();
                    outputTransportFactory = new TBufferedTransport.Factory();
                    break;

                case Buffering.Framed:
                    inputTransportFactory = new TFramedTransport.Factory();
                    outputTransportFactory = new TFramedTransport.Factory();
                    break;

                default: // layered transport(s) are optional
                    Debug.Assert(buffering == Buffering.None, "unhandled case");
                    break;
            }

            TProtocolFactory inputProtocolFactory = null;
            TProtocolFactory outputProtocolFactory = null;
            ITAsyncProcessor processor = null;
            switch (protocol)
            {
                case Protocol.Binary:
                    inputProtocolFactory = new TBinaryProtocol.Factory();
                    outputProtocolFactory = new TBinaryProtocol.Factory();
                    processor = new Calculator.AsyncProcessor(handler);
                    break;

                case Protocol.Compact:
                    inputProtocolFactory = new TCompactProtocol.Factory();
                    outputProtocolFactory = new TCompactProtocol.Factory();
                    processor = new Calculator.AsyncProcessor(handler);
                    break;

                case Protocol.Json:
                    inputProtocolFactory = new TJsonProtocol.Factory();
                    outputProtocolFactory = new TJsonProtocol.Factory();
                    processor = new Calculator.AsyncProcessor(handler);
                    break;

                case Protocol.Multiplexed:
                    inputProtocolFactory = new TBinaryProtocol.Factory();
                    outputProtocolFactory = new TBinaryProtocol.Factory();

                    var calcHandler = new CalculatorAsyncHandler();
                    var calcProcessor = new Calculator.AsyncProcessor(calcHandler);

                    var sharedServiceHandler = new SharedServiceAsyncHandler();
                    var sharedServiceProcessor = new SharedService.AsyncProcessor(sharedServiceHandler);

                    var multiplexedProcessor = new TMultiplexedProcessor();
                    multiplexedProcessor.RegisterProcessor(nameof(Calculator), calcProcessor);
                    multiplexedProcessor.RegisterProcessor(nameof(SharedService), sharedServiceProcessor);

                    processor = multiplexedProcessor;
                    break;

                default:
                    throw new ArgumentOutOfRangeException(nameof(protocol), protocol, null);
            }


            try
            {
                Logger.LogInformation(
                    $"Selected TAsyncServer with {serverTransport} transport, {processor} processor and {inputProtocolFactory} protocol factories");

                var loggerFactory = ServiceCollection.BuildServiceProvider().GetService<ILoggerFactory>();

                var server = new TSimpleAsyncServer(
                    itProcessorFactory: new TSingletonProcessorFactory(processor),
                    serverTransport: serverTransport,
                    inputTransportFactory: inputTransportFactory,
                    outputTransportFactory: outputTransportFactory,
                    inputProtocolFactory: inputProtocolFactory,
                    outputProtocolFactory: outputProtocolFactory,
                    logger: loggerFactory.CreateLogger<TSimpleAsyncServer>());

                Logger.LogInformation("Starting the server...");

                await server.ServeAsync(cancellationToken);
            }
            catch (Exception x)
            {
                Logger.LogInformation(x.ToString());
            }
        }

        private static X509Certificate2 GetCertificate()
        {
            // due to files location in net core better to take certs from top folder
            var certFile = GetCertPath(Directory.GetParent(Directory.GetCurrentDirectory()));
            return new X509Certificate2(certFile, "ThriftTest");
        }

        private static string GetCertPath(DirectoryInfo di, int maxCount = 6)
        {
            var topDir = di;
            var certFile =
                topDir.EnumerateFiles("ThriftTest.pfx", SearchOption.AllDirectories)
                    .FirstOrDefault();
            if (certFile == null)
            {
                if (maxCount == 0)
                    throw new FileNotFoundException("Cannot find file in directories");
                return GetCertPath(di.Parent, maxCount - 1);
            }

            return certFile.FullName;
        }

        private static X509Certificate LocalCertificateSelectionCallback(object sender,
            string targetHost, X509CertificateCollection localCertificates,
            X509Certificate remoteCertificate, string[] acceptableIssuers)
        {
            return GetCertificate();
        }

        private static bool ClientCertValidator(object sender, X509Certificate certificate,
            X509Chain chain, SslPolicyErrors sslPolicyErrors)
        {
            return true;
        }

        private enum Transport
        {
            Tcp,
            NamedPipe,
            Http,
            TcpTls,
        }

        private enum Buffering
        {
            None,
            Buffered,
            Framed,
        }

        private enum Protocol
        {
            Binary,
            Compact,
            Json,
            Multiplexed
        }

        public class HttpServerSample
        {
            public void Run(CancellationToken cancellationToken)
            {
                var config = new ConfigurationBuilder()
                    .AddEnvironmentVariables(prefix: "ASPNETCORE_")
                    .Build();

                var host = new WebHostBuilder()
                    .UseConfiguration(config)
                    .UseKestrel()
                    .UseUrls("http://localhost:9090")
                    .UseContentRoot(Directory.GetCurrentDirectory())
                    .UseStartup<Startup>()
                    .ConfigureLogging((ctx,logging) => ConfigureLogging(logging))
                    .Build();

                Logger.LogTrace("test");
                Logger.LogCritical("test");
                host.RunAsync(cancellationToken).GetAwaiter().GetResult();
            }

            public class Startup
            {
                public Startup(IWebHostEnvironment env)
                {
                    var builder = new ConfigurationBuilder()
                        .SetBasePath(env.ContentRootPath)
                        .AddEnvironmentVariables();

                    Configuration = builder.Build();
                }

                public IConfigurationRoot Configuration { get; }

                // This method gets called by the runtime. Use this method to add services to the container.
                public void ConfigureServices(IServiceCollection services)
                {
                    services.AddTransient<Calculator.IAsync, CalculatorAsyncHandler>();
                    services.AddTransient<ITAsyncProcessor, Calculator.AsyncProcessor>();
                    services.AddTransient<THttpServerTransport, THttpServerTransport>();
                }

                // This method gets called by the runtime. Use this method to configure the HTTP request pipeline.
                public void Configure(IApplicationBuilder app, IWebHostEnvironment env, ILoggerFactory loggerFactory)
                {
                    app.UseMiddleware<THttpServerTransport>();
                }
            }
        }

        public class CalculatorAsyncHandler : Calculator.IAsync
        {
            private readonly Dictionary<int, SharedStruct> _log = new Dictionary<int, SharedStruct>();

            public CalculatorAsyncHandler()
            {
            }

            public async Task<SharedStruct> getStructAsync(int key,
                CancellationToken cancellationToken)
            {
                Logger.LogInformation("GetStructAsync({0})", key);
                return await Task.FromResult(_log[key]);
            }

            public async Task pingAsync(CancellationToken cancellationToken)
            {
                Logger.LogInformation("PingAsync()");
                await Task.CompletedTask;
            }

            public async Task<int> addAsync(int num1, int num2, CancellationToken cancellationToken)
            {
                Logger.LogInformation($"AddAsync({num1},{num2})");
                return await Task.FromResult(num1 + num2);
            }

            public async Task<int> calculateAsync(int logid, Work w, CancellationToken cancellationToken)
            {
                Logger.LogInformation($"CalculateAsync({logid}, [{w.Op},{w.Num1},{w.Num2}])");

                var val = 0;
                switch (w.Op)
                {
                    case Operation.ADD:
                        val = w.Num1 + w.Num2;
                        break;

                    case Operation.SUBTRACT:
                        val = w.Num1 - w.Num2;
                        break;

                    case Operation.MULTIPLY:
                        val = w.Num1 * w.Num2;
                        break;

                    case Operation.DIVIDE:
                        if (w.Num2 == 0)
                        {
                            var io = new InvalidOperation
                            {
                                WhatOp = (int) w.Op,
                                Why = "Cannot divide by 0"
                            };

                            throw io;
                        }
                        val = w.Num1 / w.Num2;
                        break;

                    default:
                    {
                        var io = new InvalidOperation
                        {
                            WhatOp = (int) w.Op,
                            Why = "Unknown operation"
                        };

                        throw io;
                    }
                }

                var entry = new SharedStruct
                {
                    Key = logid,
                    Value = val.ToString()
                };

                _log[logid] = entry;

                return await Task.FromResult(val);
            }

            public async Task zipAsync(CancellationToken cancellationToken)
            {
                Logger.LogInformation("ZipAsync() with delay 100mc");
                await Task.Delay(100, CancellationToken.None);
            }
        }

        public class SharedServiceAsyncHandler : SharedService.IAsync
        {
            public async Task<SharedStruct> getStructAsync(int key, CancellationToken cancellationToken)
            {
                Logger.LogInformation("GetStructAsync({0})", key);
                return await Task.FromResult(new SharedStruct()
                {
                    Key = key,
                    Value = "GetStructAsync"
                });
            }
        }
    }
}
