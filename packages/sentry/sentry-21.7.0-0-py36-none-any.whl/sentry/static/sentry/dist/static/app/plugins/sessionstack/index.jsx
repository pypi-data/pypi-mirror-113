Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var basePlugin_1 = tslib_1.__importDefault(require("app/plugins/basePlugin"));
var settings_1 = tslib_1.__importDefault(require("./components/settings"));
var SessionStackPlugin = /** @class */ (function (_super) {
    tslib_1.__extends(SessionStackPlugin, _super);
    function SessionStackPlugin() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.displayName = 'SessionStack';
        return _this;
    }
    // should never be be called since this is a non-issue plugin
    SessionStackPlugin.prototype.renderGroupActions = function () {
        return null;
    };
    SessionStackPlugin.prototype.renderSettings = function (props) {
        return <settings_1.default plugin={this.plugin} {...props}/>;
    };
    return SessionStackPlugin;
}(basePlugin_1.default));
exports.default = SessionStackPlugin;
//# sourceMappingURL=index.jsx.map