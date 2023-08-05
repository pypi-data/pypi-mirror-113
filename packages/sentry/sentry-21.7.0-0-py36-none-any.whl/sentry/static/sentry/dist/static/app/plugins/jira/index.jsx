Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var defaultIssuePlugin_1 = tslib_1.__importDefault(require("app/plugins/defaultIssuePlugin"));
var issueActions_1 = tslib_1.__importDefault(require("./components/issueActions"));
var settings_1 = tslib_1.__importDefault(require("./components/settings"));
var Jira = /** @class */ (function (_super) {
    tslib_1.__extends(Jira, _super);
    function Jira() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.displayName = 'Jira';
        return _this;
    }
    Jira.prototype.renderSettings = function (props) {
        return <settings_1.default plugin={this.plugin} {...props}/>;
    };
    Jira.prototype.renderGroupActions = function (props) {
        return <issueActions_1.default {...props}/>;
    };
    return Jira;
}(defaultIssuePlugin_1.default));
exports.default = Jira;
//# sourceMappingURL=index.jsx.map