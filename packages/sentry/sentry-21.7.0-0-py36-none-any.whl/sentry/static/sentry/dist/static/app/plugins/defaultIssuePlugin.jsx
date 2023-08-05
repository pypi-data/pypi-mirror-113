Object.defineProperty(exports, "__esModule", { value: true });
exports.DefaultIssuePlugin = void 0;
var tslib_1 = require("tslib");
var basePlugin_1 = tslib_1.__importDefault(require("app/plugins/basePlugin"));
var issueActions_1 = tslib_1.__importDefault(require("app/plugins/components/issueActions"));
var DefaultIssuePlugin = /** @class */ (function (_super) {
    tslib_1.__extends(DefaultIssuePlugin, _super);
    function DefaultIssuePlugin() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    DefaultIssuePlugin.prototype.renderGroupActions = function (props) {
        return <issueActions_1.default {...props}/>;
    };
    return DefaultIssuePlugin;
}(basePlugin_1.default));
exports.DefaultIssuePlugin = DefaultIssuePlugin;
exports.default = DefaultIssuePlugin;
//# sourceMappingURL=defaultIssuePlugin.jsx.map