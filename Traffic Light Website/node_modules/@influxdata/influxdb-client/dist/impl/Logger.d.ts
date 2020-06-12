/**
 * Logging interface.
 */
export interface Logger {
    error(message: string, err?: any): void;
    warn(message: string, err?: any): void;
}
/**
 * Logger that logs to console.out
 */
export declare const consoleLogger: Logger;
declare const Logger: Logger;
/**
 * Sets custom logger.
 * @param logger new logger
 * @return previous logger
 */
export declare function setLogger(logger: Logger): Logger;
export default Logger;
//# sourceMappingURL=Logger.d.ts.map