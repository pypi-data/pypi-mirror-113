Object.defineProperty(exports, "__esModule", { value: true });
exports.Divider = void 0;
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var overflowEllipsis_1 = tslib_1.__importDefault(require("app/styles/overflowEllipsis"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var events_1 = require("app/utils/events");
function EventTitleTreeLabel(_a) {
    var treeLabel = _a.treeLabel;
    var firstFourParts = treeLabel.slice(0, 4);
    var remainingParts = treeLabel.slice(firstFourParts.length);
    return (<Wrapper>
      <FirstFourParts>
        {firstFourParts.map(function (part, index) {
            var _a = events_1.getTreeLabelPartDetails(part), label = _a.label, highlight = _a.highlight;
            if (index !== firstFourParts.length - 1) {
                return (<react_1.Fragment key={index}>
                <PriorityPart highlight={highlight}>{label}</PriorityPart>
                <exports.Divider>{'|'}</exports.Divider>
              </react_1.Fragment>);
            }
            return (<PriorityPart key={index} highlight={highlight}>
              {label}
            </PriorityPart>);
        })}
      </FirstFourParts>
      {!!remainingParts.length && (<RemainingLabels>
          {remainingParts.map(function (part, index) {
                var _a = events_1.getTreeLabelPartDetails(part), label = _a.label, highlight = _a.highlight;
                return (<react_1.Fragment key={index}>
                <exports.Divider>{'|'}</exports.Divider>
                <Label highlight={highlight}>{label}</Label>
              </react_1.Fragment>);
            })}
        </RemainingLabels>)}
    </Wrapper>);
}
exports.default = EventTitleTreeLabel;
var Wrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: inline-grid;\n  grid-template-columns: auto 1fr;\n  align-items: center;\n"], ["\n  display: inline-grid;\n  grid-template-columns: auto 1fr;\n  align-items: center;\n"])));
var FirstFourParts = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: inline-grid;\n  grid-auto-flow: column;\n  align-items: center;\n"], ["\n  display: inline-grid;\n  grid-auto-flow: column;\n  align-items: center;\n"])));
var Label = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  ", "\n"], ["\n  ", "\n"])), function (p) {
    return p.highlight &&
        "\n      background: " + p.theme.alert.info.backgroundLight + ";\n      border-radius: " + p.theme.borderRadius + ";\n      padding: 0 " + space_1.default(0.5) + ";\n    ";
});
var PriorityPart = styled_1.default(Label)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  ", "\n  display: inline-block;\n"], ["\n  ", "\n  display: inline-block;\n"])), overflowEllipsis_1.default);
var RemainingLabels = styled_1.default('div')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  ", "\n  display: inline-block;\n  min-width: 50px;\n"], ["\n  ", "\n  display: inline-block;\n  min-width: 50px;\n"])), overflowEllipsis_1.default);
exports.Divider = styled_1.default('div')(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  display: inline-block;\n  margin: 0 ", ";\n"], ["\n  color: ", ";\n  display: inline-block;\n  margin: 0 ", ";\n"])), function (p) { return p.theme.gray200; }, space_1.default(1));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6;
//# sourceMappingURL=eventTitleTreeLabel.jsx.map