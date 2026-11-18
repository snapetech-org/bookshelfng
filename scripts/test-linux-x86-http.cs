using System.Net;
using System.Net.Sockets;
using System.Runtime.InteropServices;

if (RuntimeInformation.ProcessArchitecture != Architecture.X86)
{
    throw new InvalidOperationException("This acceptance probe must execute in the native x86 runtime.");
}

using var unusedPort = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
unusedPort.Bind(new IPEndPoint(IPAddress.Loopback, 0));
using var client = new HttpClient(new SocketsHttpHandler { UseProxy = false, ConnectCallback = ConnectWithRetry });
var endpoint = (IPEndPoint)unusedPort.LocalEndPoint!;
try
{
    using var response = await client.GetAsync($"http://{endpoint}/");
    throw new InvalidOperationException("A socket that was never listening accepted the connection.");
}
catch (HttpRequestException error) when (error.InnerException is SocketException { SocketErrorCode: SocketError.ConnectionRefused })
{
    Console.WriteLine("PASS async HTTP connection failure propagated to the caller");
}

static async ValueTask<Stream> ConnectWithRetry(SocketsHttpConnectionContext context, CancellationToken cancellationToken)
{
    try
    {
        return await ConnectSocket(context, cancellationToken).ConfigureAwait(false);
    }
    catch (SocketException)
    {
        return await ConnectSocket(context, cancellationToken).ConfigureAwait(false);
    }
}

static async ValueTask<Stream> ConnectSocket(SocketsHttpConnectionContext context, CancellationToken cancellationToken)
{
    var socket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
    try
    {
        await socket.ConnectAsync(context.DnsEndPoint, cancellationToken).ConfigureAwait(false);
        return new NetworkStream(socket, ownsSocket: true);
    }
    catch
    {
        socket.Dispose();
        throw;
    }
}
