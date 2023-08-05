Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var ColorBar = function (props) {
    return (<VitalBar fractions={props.colorStops.map(function (_a) {
        var percent = _a.percent;
        return percent;
    })}>
      {props.colorStops.map(function (colorStop) {
            return <BarStatus color={colorStop.color} key={colorStop.color}/>;
        })}
    </VitalBar>);
};
var VitalBar = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  height: 16px;\n  width: 100%;\n  overflow: hidden;\n  position: relative;\n  background: ", ";\n  display: grid;\n  grid-template-columns: ", ";\n  margin-bottom: ", ";\n  border-radius: 2px;\n"], ["\n  height: 16px;\n  width: 100%;\n  overflow: hidden;\n  position: relative;\n  background: ", ";\n  display: grid;\n  grid-template-columns: ", ";\n  margin-bottom: ", ";\n  border-radius: 2px;\n"])), function (p) { return p.theme.gray100; }, function (p) { return p.fractions.map(function (f) { return f + "fr"; }).join(' '); }, space_1.default(1));
var BarStatus = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  background-color: ", ";\n"], ["\n  background-color: ", ";\n"])), function (p) { return p.theme[p.color]; });
exports.default = ColorBar;
var templateObject_1, templateObject_2;
//# sourceMappingURL=colorBar.jsx.map