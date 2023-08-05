Object.defineProperty(exports, "__esModule", { value: true });
exports.RadioLineItem = void 0;
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var is_prop_valid_1 = tslib_1.__importDefault(require("@emotion/is-prop-valid"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var radio_1 = tslib_1.__importDefault(require("app/components/radio"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var Container = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n  grid-auto-flow: ", ";\n  grid-auto-rows: max-content;\n  grid-auto-columns: max-content;\n"], ["\n  display: grid;\n  grid-gap: ", ";\n  grid-auto-flow: ", ";\n  grid-auto-rows: max-content;\n  grid-auto-columns: max-content;\n"])), function (p) { return space_1.default(p.orientInline ? 3 : 1); }, function (p) { return (p.orientInline ? 'column' : 'row'); });
var RadioGroup = function (_a) {
    var value = _a.value, disabled = _a.disabled, choices = _a.choices, label = _a.label, onChange = _a.onChange, orientInline = _a.orientInline, props = tslib_1.__rest(_a, ["value", "disabled", "choices", "label", "onChange", "orientInline"]);
    return (<Container orientInline={orientInline} {...props} role="radiogroup" aria-labelledby={label}>
    {(choices || []).map(function (_a, index) {
            var _b = tslib_1.__read(_a, 3), id = _b[0], name = _b[1], description = _b[2];
            return (<exports.RadioLineItem key={index} role="radio" index={index} aria-checked={value === id} disabled={disabled}>
        <radio_1.default aria-label={id} disabled={disabled} checked={value === id} onChange={function (e) {
                    return !disabled && onChange(id, e);
                }}/>
        <RadioLineText disabled={disabled}>{name}</RadioLineText>
        {description && (<React.Fragment>
            {/* If there is a description then we want to have a 2x2 grid so the first column width aligns with Radio Button */}
            <div />
            <Description>{description}</Description>
          </React.Fragment>)}
      </exports.RadioLineItem>);
        })}
  </Container>);
};
var shouldForwardProp = function (p) {
    return typeof p === 'string' && !['disabled', 'animate'].includes(p) && is_prop_valid_1.default(p);
};
exports.RadioLineItem = styled_1.default('label', { shouldForwardProp: shouldForwardProp })(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-gap: 0.25em 0.5em;\n  grid-template-columns: max-content auto;\n  align-items: center;\n  cursor: ", ";\n  outline: none;\n  font-weight: normal;\n  margin: 0;\n"], ["\n  display: grid;\n  grid-gap: 0.25em 0.5em;\n  grid-template-columns: max-content auto;\n  align-items: center;\n  cursor: ", ";\n  outline: none;\n  font-weight: normal;\n  margin: 0;\n"])), function (p) { return (p.disabled ? 'default' : 'pointer'); });
var RadioLineText = styled_1.default('div', { shouldForwardProp: shouldForwardProp })(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  opacity: ", ";\n"], ["\n  opacity: ", ";\n"])), function (p) { return (p.disabled ? 0.4 : null); });
var Description = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  font-size: ", ";\n  line-height: 1.4em;\n"], ["\n  color: ", ";\n  font-size: ", ";\n  line-height: 1.4em;\n"])), function (p) { return p.theme.gray300; }, function (p) { return p.theme.fontSizeRelativeSmall; });
exports.default = RadioGroup;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=radioGroup.jsx.map