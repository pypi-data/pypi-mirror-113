Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var asyncComponent_1 = tslib_1.__importDefault(require("app/components/asyncComponent"));
var duration_1 = tslib_1.__importDefault(require("app/components/duration"));
var panels_1 = require("app/components/panels");
var timeSince_1 = tslib_1.__importDefault(require("app/components/timeSince"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var checkInIcon_1 = tslib_1.__importDefault(require("./checkInIcon"));
var MonitorCheckIns = /** @class */ (function (_super) {
    tslib_1.__extends(MonitorCheckIns, _super);
    function MonitorCheckIns() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    MonitorCheckIns.prototype.getEndpoints = function () {
        var monitor = this.props.monitor;
        return [
            ['checkInList', "/monitors/" + monitor.id + "/checkins/", { query: { per_page: 10 } }],
        ];
    };
    MonitorCheckIns.prototype.renderError = function () {
        return <ErrorWrapper>{_super.prototype.renderError.call(this)}</ErrorWrapper>;
    };
    MonitorCheckIns.prototype.renderBody = function () {
        return (<panels_1.PanelBody>
        {this.state.checkInList.map(function (checkIn) { return (<panels_1.PanelItem key={checkIn.id}>
            <CheckInIconWrapper>
              <checkInIcon_1.default status={checkIn.status} size={16}/>
            </CheckInIconWrapper>
            <TimeSinceWrapper>
              <timeSince_1.default date={checkIn.dateCreated}/>
            </TimeSinceWrapper>
            <div>{checkIn.duration && <duration_1.default seconds={checkIn.duration / 100}/>}</div>
          </panels_1.PanelItem>); })}
      </panels_1.PanelBody>);
    };
    return MonitorCheckIns;
}(asyncComponent_1.default));
exports.default = MonitorCheckIns;
var DivMargin = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  margin-right: ", ";\n"], ["\n  margin-right: ", ";\n"])), space_1.default(2));
var CheckInIconWrapper = styled_1.default(DivMargin)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n"], ["\n  display: flex;\n  align-items: center;\n"])));
var TimeSinceWrapper = styled_1.default(DivMargin)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject([""], [""])));
var ErrorWrapper = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  margin: ", " ", " 0;\n"], ["\n  margin: ", " ", " 0;\n"])), space_1.default(3), space_1.default(3));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=monitorCheckIns.jsx.map