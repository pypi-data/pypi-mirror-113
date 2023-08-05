/* global process */
Object.defineProperty(exports, "__esModule", { value: true });
/**
 * This module is used to define the look and feels for charts rendered via the
 * backend chart rendering service Chartcuterie.
 *
 * Be careful what you import into this file, as it will end up being bundled
 * into the configuration file loaded by the service.
 */
var discover_1 = require("./discover");
/**
 * All registered style descriptors
 */
var renderConfig = new Map();
/**
 * Chartcuterie configuration object
 */
var config = {
    version: process.env.COMMIT_SHA,
    renderConfig: renderConfig,
};
/**
 * Register a style descriptor
 */
var register = function (renderDescriptor) {
    return renderConfig.set(renderDescriptor.key, renderDescriptor);
};
discover_1.discoverCharts.forEach(register);
exports.default = config;
//# sourceMappingURL=config.jsx.map