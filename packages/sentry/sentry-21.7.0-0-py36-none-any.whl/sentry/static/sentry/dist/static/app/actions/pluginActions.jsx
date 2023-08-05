Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var reflux_1 = tslib_1.__importDefault(require("reflux"));
var PluginActions = reflux_1.default.createActions([
    'update',
    'updateError',
    'updateSuccess',
    'fetchAll',
    'fetchAllSuccess',
    'fetchAllError',
]);
exports.default = PluginActions;
//# sourceMappingURL=pluginActions.jsx.map