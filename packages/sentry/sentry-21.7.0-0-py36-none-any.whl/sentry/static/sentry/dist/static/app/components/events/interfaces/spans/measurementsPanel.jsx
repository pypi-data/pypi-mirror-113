Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var utils_1 = require("app/components/performance/waterfall/utils");
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var utils_2 = require("app/utils");
var constants_1 = require("app/utils/performance/vitals/constants");
var utils_3 = require("./utils");
var MeasurementsPanel = /** @class */ (function (_super) {
    tslib_1.__extends(MeasurementsPanel, _super);
    function MeasurementsPanel() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    MeasurementsPanel.prototype.render = function () {
        var _a = this.props, event = _a.event, generateBounds = _a.generateBounds, dividerPosition = _a.dividerPosition;
        var measurements = utils_3.getMeasurements(event);
        return (<Container style={{
                // the width of this component is shrunk to compensate for half of the width of the divider line
                width: "calc(" + utils_1.toPercent(1 - dividerPosition) + " - 0.5px)",
            }}>
        {Array.from(measurements).map(function (_a) {
                var _b = tslib_1.__read(_a, 2), timestamp = _b[0], verticalMark = _b[1];
                var bounds = utils_3.getMeasurementBounds(timestamp, generateBounds);
                var shouldDisplay = utils_2.defined(bounds.left) && utils_2.defined(bounds.width);
                if (!shouldDisplay || !bounds.isSpanVisibleInView) {
                    return null;
                }
                // Measurements are referred to by their full name `measurements.<name>`
                // here but are stored using their abbreviated name `<name>`. Make sure
                // to convert it appropriately.
                var vitals = Object.keys(verticalMark.marks).map(function (name) { return constants_1.WEB_VITAL_DETAILS["measurements." + name]; });
                // generate vertical marker label
                var acronyms = vitals.map(function (vital) { return vital.acronym; });
                var lastAcronym = acronyms.pop();
                var label = acronyms.length
                    ? acronyms.join(', ') + " & " + lastAcronym
                    : lastAcronym;
                // generate tooltip labe;l
                var longNames = vitals.map(function (vital) { return vital.name; });
                var lastName = longNames.pop();
                var tooltipLabel = longNames.length
                    ? longNames.join(', ') + " & " + lastName
                    : lastName;
                return (<LabelContainer key={String(timestamp)} failedThreshold={verticalMark.failedThreshold} label={label} tooltipLabel={tooltipLabel} left={utils_1.toPercent(bounds.left || 0)}/>);
            })}
      </Container>);
    };
    return MeasurementsPanel;
}(react_1.PureComponent));
var Container = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  position: relative;\n  overflow: hidden;\n\n  height: 20px;\n"], ["\n  position: relative;\n  overflow: hidden;\n\n  height: 20px;\n"])));
var StyledLabelContainer = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  position: absolute;\n  top: 0;\n  height: 100%;\n  user-select: none;\n  white-space: nowrap;\n"], ["\n  position: absolute;\n  top: 0;\n  height: 100%;\n  user-select: none;\n  white-space: nowrap;\n"])));
var Label = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  transform: translateX(-50%);\n  font-size: ", ";\n  font-weight: 600;\n  ", "\n"], ["\n  transform: translateX(-50%);\n  font-size: ", ";\n  font-weight: 600;\n  ", "\n"])), function (p) { return p.theme.fontSizeExtraSmall; }, function (p) { return (p.failedThreshold ? "color: " + p.theme.red300 + ";" : null); });
exports.default = MeasurementsPanel;
var LabelContainer = /** @class */ (function (_super) {
    tslib_1.__extends(LabelContainer, _super);
    function LabelContainer() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            width: 1,
        };
        _this.elementDOMRef = react_1.createRef();
        return _this;
    }
    LabelContainer.prototype.componentDidMount = function () {
        var current = this.elementDOMRef.current;
        if (current) {
            // eslint-disable-next-line react/no-did-mount-set-state
            this.setState({
                width: current.clientWidth,
            });
        }
    };
    LabelContainer.prototype.render = function () {
        var _a = this.props, left = _a.left, label = _a.label, tooltipLabel = _a.tooltipLabel, failedThreshold = _a.failedThreshold;
        return (<StyledLabelContainer ref={this.elementDOMRef} style={{
                left: "clamp(calc(0.5 * " + this.state.width + "px), " + left + ", calc(100% - 0.5 * " + this.state.width + "px))",
            }}>
        <Label failedThreshold={failedThreshold}>
          <tooltip_1.default title={tooltipLabel} position="top" containerDisplayMode="inline-block">
            {label}
          </tooltip_1.default>
        </Label>
      </StyledLabelContainer>);
    };
    return LabelContainer;
}(react_1.Component));
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=measurementsPanel.jsx.map