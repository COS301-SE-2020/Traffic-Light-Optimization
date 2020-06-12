import { ConnectionOptions } from '../../options';
import { CommunicationObserver, Transport, SendOptions, ChunkCombiner } from '../../transport';
/**
 * Transport layer on top of node http or https library.
 */
export declare class NodeHttpTransport implements Transport {
    private connectionOptions;
    readonly chunkCombiner: ChunkCombiner;
    private defaultOptions;
    private requestApi;
    /**
     * Creates a node transport using for the client options supplied.
     * @param connectionOptions client options
     */
    constructor(connectionOptions: ConnectionOptions);
    /**
     * Sends data to server and receives communication events via communication callbacks.
     *
     * @param path HTTP path
     * @param body  message body
     * @param headers HTTP headers
     * @param method HTTP method
     * @param callbacks communication callbacks
     * @return a handle that can cancel the communication
     */
    send(path: string, body: string, options: SendOptions, callbacks?: Partial<CommunicationObserver<any>>): void;
    /**
     * Sends data to the server and receives decoded result. The type of the result depends on
     * response's content-type (deserialized json, text).
    
     * @param path HTTP path
     * @param requestBody  request body
     * @param options  send options
     */
    request(path: string, body: any, options: SendOptions): Promise<any>;
    /**
     * Creates configuration for a specific request.
     *
     * @param path API path starting with '/' and containing also query parameters
     * @param headers HTTP headers to use
     * @param method HTTP method
     * @param body request body, will be utf-8 encoded
     * @return configuration suitable for making the request
     */
    private createRequestMessage;
    private _request;
}
export default NodeHttpTransport;
//# sourceMappingURL=NodeHttpTransport.d.ts.map