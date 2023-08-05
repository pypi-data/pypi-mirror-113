Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var settings_1 = tslib_1.__importDefault(require("app/plugins/components/settings"));
var BasePlugin = /** @class */ (function () {
    function BasePlugin(data) {
        this.plugin = data;
    }
    BasePlugin.prototype.renderSettings = function (props) {
        return <settings_1.default plugin={this.plugin} {...props}/>;
    };
    return BasePlugin;
}());
exports.default = BasePlugin;
//# sourceMappingURL=basePlugin.jsx.map