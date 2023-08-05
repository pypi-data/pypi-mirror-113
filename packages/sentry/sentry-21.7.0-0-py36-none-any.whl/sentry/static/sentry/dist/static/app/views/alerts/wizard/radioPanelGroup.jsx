Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var radio_1 = tslib_1.__importDefault(require("app/components/radio"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var RadioPanelGroup = function (_a) {
    var value = _a.value, choices = _a.choices, label = _a.label, onChange = _a.onChange, props = tslib_1.__rest(_a, ["value", "choices", "label", "onChange"]);
    return (<Container {...props} role="radiogroup" aria-labelledby={label}>
    {(choices || []).map(function (_a, index) {
            var _b = tslib_1.__read(_a, 3), id = _b[0], name = _b[1], extraContent = _b[2];
            return (<RadioPanel key={index}>
        <RadioLineItem role="radio" index={index} aria-checked={value === id}>
          <radio_1.default radioSize="small" aria-label={id} checked={value === id} onChange={function (e) { return onChange(id, e); }}/>
          <div>{name}</div>
          {extraContent}
        </RadioLineItem>
      </RadioPanel>);
        })}
  </Container>);
};
exports.default = RadioPanelGroup;
var Container = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n  grid-auto-flow: row;\n  grid-auto-rows: max-content;\n  grid-auto-columns: auto;\n"], ["\n  display: grid;\n  grid-gap: ", ";\n  grid-auto-flow: row;\n  grid-auto-rows: max-content;\n  grid-auto-columns: auto;\n"])), space_1.default(1));
var RadioLineItem = styled_1.default('label')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-gap: ", " ", ";\n  grid-template-columns: max-content auto max-content;\n  align-items: center;\n  cursor: pointer;\n  outline: none;\n  font-weight: normal;\n  margin: 0;\n  color: ", ";\n  transition: color 0.3s ease-in;\n  padding: 0;\n  position: relative;\n\n  &:hover,\n  &:focus {\n    color: ", ";\n  }\n\n  svg {\n    display: none;\n    opacity: 0;\n  }\n\n  &[aria-checked='true'] {\n    color: ", ";\n  }\n"], ["\n  display: grid;\n  grid-gap: ", " ", ";\n  grid-template-columns: max-content auto max-content;\n  align-items: center;\n  cursor: pointer;\n  outline: none;\n  font-weight: normal;\n  margin: 0;\n  color: ", ";\n  transition: color 0.3s ease-in;\n  padding: 0;\n  position: relative;\n\n  &:hover,\n  &:focus {\n    color: ", ";\n  }\n\n  svg {\n    display: none;\n    opacity: 0;\n  }\n\n  &[aria-checked='true'] {\n    color: ", ";\n  }\n"])), space_1.default(0.25), space_1.default(1), function (p) { return p.theme.subText; }, function (p) { return p.theme.textColor; }, function (p) { return p.theme.textColor; });
var RadioPanel = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  margin: 0;\n"], ["\n  margin: 0;\n"])));
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=radioPanelGroup.jsx.map