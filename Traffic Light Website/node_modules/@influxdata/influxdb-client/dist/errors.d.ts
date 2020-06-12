/**
 * Strategy for calculating retry delays.
 */
export interface RetryDelayStrategy {
    /**
     * Returns delay for a next retry
     * @param error reason for retrying
     * @return milliseconds
     */
    nextDelay(error?: Error): number;
    /** Implementation should reset its state, this is mandatory to call upon success.  */
    success(): void;
}
/**
 * Interface for errors to inform that an associated operation can be retried.
 */
export interface RetriableDecision {
    /**
     * Informs whether this can be retried.
     */
    canRetry(): boolean;
    /**
     * Get the delay in milliseconds to retry the action.
     * @return  0 to let the implementation decide, miliseconds delay otherwise
     */
    retryAfter(): number;
}
export declare function isStatusCodeRetriable(statusCode: number): boolean;
export declare class IllegalArgumentError extends Error {
    constructor(message: string);
}
/**
 * A general HTTP error.
 */
export declare class HttpError extends Error implements RetriableDecision {
    readonly statusCode: number;
    readonly statusMessage: string | undefined;
    readonly body?: string | undefined;
    private _retryAfter;
    constructor(statusCode: number, statusMessage: string | undefined, body?: string | undefined, retryAfter?: string | undefined | null);
    private setRetryAfter;
    canRetry(): boolean;
    retryAfter(): number;
}
/**
 * Tests the error to know whether a possible HTTP call can be retried.
 * @param error Test whether the givver e
 */
export declare function canRetryHttpCall(error: any): boolean;
/**
 * Gets retry delay from the supplied error, possibly using random number up to retryJitter.
 */
export declare function getRetryDelay(error?: Error, retryJitter?: number): number;
export declare class RequestTimedOutError extends Error implements RetriableDecision {
    constructor();
    canRetry(): boolean;
    retryAfter(): number;
}
export declare class AbortError extends Error implements RetriableDecision {
    constructor();
    canRetry(): boolean;
    retryAfter(): number;
}
//# sourceMappingURL=errors.d.ts.map