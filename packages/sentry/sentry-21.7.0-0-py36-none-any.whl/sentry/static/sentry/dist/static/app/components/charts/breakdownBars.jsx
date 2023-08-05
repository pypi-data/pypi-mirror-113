Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var formatters_1 = require("app/utils/formatters");
function BreakdownBars(_a) {
    var data = _a.data;
    var total = data.reduce(function (sum, point) { return point.value + sum; }, 0);
    return (<BreakdownGrid>
      {data.map(function (point, i) { return (<react_1.Fragment key={i + ":" + point.label}>
          <Percentage>{formatters_1.formatPercentage(point.value / total, 0)}</Percentage>
          <BarContainer data-test-id={"status-" + point.label} cursor={point.onClick ? 'pointer' : 'default'} onClick={point.onClick}>
            <Bar style={{ width: ((point.value / total) * 100).toFixed(2) + "%" }}/>
            <Label>{point.label}</Label>
          </BarContainer>
        </react_1.Fragment>); })}
    </BreakdownGrid>);
}
exports.default = BreakdownBars;
var BreakdownGrid = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: min-content auto;\n  column-gap: ", ";\n  row-gap: ", ";\n"], ["\n  display: grid;\n  grid-template-columns: min-content auto;\n  column-gap: ", ";\n  row-gap: ", ";\n"])), space_1.default(1), space_1.default(1));
var Percentage = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n  text-align: right;\n"], ["\n  font-size: ", ";\n  text-align: right;\n"])), function (p) { return p.theme.fontSizeExtraLarge; });
var BarContainer = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  padding-left: ", ";\n  padding-right: ", ";\n  position: relative;\n  cursor: ", ";\n"], ["\n  padding-left: ", ";\n  padding-right: ", ";\n  position: relative;\n  cursor: ", ";\n"])), space_1.default(1), space_1.default(1), function (p) { return p.cursor; });
var Label = styled_1.default('span')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  position: relative;\n  color: ", ";\n  z-index: 2;\n  font-size: ", ";\n"], ["\n  position: relative;\n  color: ", ";\n  z-index: 2;\n  font-size: ", ";\n"])), function (p) { return p.theme.textColor; }, function (p) { return p.theme.fontSizeSmall; });
var Bar = styled_1.default('div')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  border-radius: 2px;\n  background-color: ", ";\n  position: absolute;\n  top: 0;\n  left: 0;\n  z-index: 1;\n  height: 100%;\n  width: 0%;\n"], ["\n  border-radius: 2px;\n  background-color: ", ";\n  position: absolute;\n  top: 0;\n  left: 0;\n  z-index: 1;\n  height: 100%;\n  width: 0%;\n"])), function (p) { return p.theme.border; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=breakdownBars.jsx.map