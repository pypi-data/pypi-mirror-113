Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_router_1 = require("react-router");
var asyncView_1 = tslib_1.__importDefault(require("app/views/asyncView"));
var monitorForm_1 = tslib_1.__importDefault(require("./monitorForm"));
var EditMonitor = /** @class */ (function (_super) {
    tslib_1.__extends(EditMonitor, _super);
    function EditMonitor() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.onUpdate = function (data) {
            return _this.setState(function (state) { return ({ monitor: tslib_1.__assign(tslib_1.__assign({}, state.monitor), data) }); });
        };
        _this.onSubmitSuccess = function (data) {
            return react_router_1.browserHistory.push("/organizations/" + _this.props.params.orgId + "/monitors/" + data.id + "/");
        };
        return _this;
    }
    EditMonitor.prototype.getEndpoints = function () {
        var params = this.props.params;
        return [['monitor', "/monitors/" + params.monitorId + "/"]];
    };
    EditMonitor.prototype.getTitle = function () {
        if (this.state.monitor) {
            return this.state.monitor.name + " - Monitors - " + this.props.params.orgId;
        }
        return "Monitors - " + this.props.params.orgId;
    };
    EditMonitor.prototype.renderBody = function () {
        var monitor = this.state.monitor;
        if (monitor === null) {
            return null;
        }
        return (<react_1.Fragment>
        <h1>Edit Monitor</h1>

        <monitorForm_1.default monitor={monitor} apiMethod="PUT" apiEndpoint={"/monitors/" + monitor.id + "/"} onSubmitSuccess={this.onSubmitSuccess}/>
      </react_1.Fragment>);
    };
    return EditMonitor;
}(asyncView_1.default));
exports.default = EditMonitor;
//# sourceMappingURL=edit.jsx.map