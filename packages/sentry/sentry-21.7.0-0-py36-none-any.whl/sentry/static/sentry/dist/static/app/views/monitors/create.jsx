Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_router_1 = require("react-router");
var asyncView_1 = tslib_1.__importDefault(require("app/views/asyncView"));
var monitorForm_1 = tslib_1.__importDefault(require("./monitorForm"));
var CreateMonitor = /** @class */ (function (_super) {
    tslib_1.__extends(CreateMonitor, _super);
    function CreateMonitor() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.onSubmitSuccess = function (data) {
            react_router_1.browserHistory.push("/organizations/" + _this.props.params.orgId + "/monitors/" + data.id + "/");
        };
        return _this;
    }
    CreateMonitor.prototype.getTitle = function () {
        return "Monitors - " + this.props.params.orgId;
    };
    CreateMonitor.prototype.renderBody = function () {
        return (<react_1.Fragment>
        <h1>New Monitor</h1>
        <monitorForm_1.default apiMethod="POST" apiEndpoint={"/organizations/" + this.props.params.orgId + "/monitors/"} onSubmitSuccess={this.onSubmitSuccess}/>
      </react_1.Fragment>);
    };
    return CreateMonitor;
}(asyncView_1.default));
exports.default = CreateMonitor;
//# sourceMappingURL=create.jsx.map