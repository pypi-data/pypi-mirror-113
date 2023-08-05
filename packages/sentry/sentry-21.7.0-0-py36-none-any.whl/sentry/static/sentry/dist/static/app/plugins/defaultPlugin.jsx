Object.defineProperty(exports, "__esModule", { value: true });
exports.DefaultPlugin = void 0;
var tslib_1 = require("tslib");
var basePlugin_1 = tslib_1.__importDefault(require("app/plugins/basePlugin"));
var DefaultPlugin = /** @class */ (function (_super) {
    tslib_1.__extends(DefaultPlugin, _super);
    function DefaultPlugin() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    // should never be be called since this is a non-issue plugin
    DefaultPlugin.prototype.renderGroupActions = function () {
        return null;
    };
    DefaultPlugin.displayName = 'DefaultPlugin';
    return DefaultPlugin;
}(basePlugin_1.default));
exports.DefaultPlugin = DefaultPlugin;
//# sourceMappingURL=defaultPlugin.jsx.map