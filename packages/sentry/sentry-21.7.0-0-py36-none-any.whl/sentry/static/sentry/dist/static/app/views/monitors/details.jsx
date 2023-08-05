Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var panels_1 = require("app/components/panels");
var locale_1 = require("app/locale");
var asyncView_1 = tslib_1.__importDefault(require("app/views/asyncView"));
var monitorCheckIns_1 = tslib_1.__importDefault(require("./monitorCheckIns"));
var monitorHeader_1 = tslib_1.__importDefault(require("./monitorHeader"));
var monitorIssues_1 = tslib_1.__importDefault(require("./monitorIssues"));
var monitorStats_1 = tslib_1.__importDefault(require("./monitorStats"));
var MonitorDetails = /** @class */ (function (_super) {
    tslib_1.__extends(MonitorDetails, _super);
    function MonitorDetails() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.onUpdate = function (data) {
            return _this.setState(function (state) { return ({ monitor: tslib_1.__assign(tslib_1.__assign({}, state.monitor), data) }); });
        };
        return _this;
    }
    MonitorDetails.prototype.getEndpoints = function () {
        var _a = this.props, params = _a.params, location = _a.location;
        return [['monitor', "/monitors/" + params.monitorId + "/", { query: location.query }]];
    };
    MonitorDetails.prototype.getTitle = function () {
        if (this.state.monitor) {
            return this.state.monitor.name + " - Monitors - " + this.props.params.orgId;
        }
        return "Monitors - " + this.props.params.orgId;
    };
    MonitorDetails.prototype.renderBody = function () {
        var monitor = this.state.monitor;
        if (monitor === null) {
            return null;
        }
        return (<react_1.Fragment>
        <monitorHeader_1.default monitor={monitor} orgId={this.props.params.orgId} onUpdate={this.onUpdate}/>

        <monitorStats_1.default monitor={monitor}/>

        <panels_1.Panel style={{ paddingBottom: 0 }}>
          <panels_1.PanelHeader>{locale_1.t('Related Issues')}</panels_1.PanelHeader>

          <monitorIssues_1.default monitor={monitor} orgId={this.props.params.orgId}/>
        </panels_1.Panel>

        <panels_1.Panel>
          <panels_1.PanelHeader>{locale_1.t('Recent Check-ins')}</panels_1.PanelHeader>

          <monitorCheckIns_1.default monitor={monitor}/>
        </panels_1.Panel>
      </react_1.Fragment>);
    };
    return MonitorDetails;
}(asyncView_1.default));
exports.default = MonitorDetails;
//# sourceMappingURL=details.jsx.map