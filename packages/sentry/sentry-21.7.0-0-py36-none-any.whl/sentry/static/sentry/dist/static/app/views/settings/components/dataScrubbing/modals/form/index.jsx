Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var sortBy_1 = tslib_1.__importDefault(require("lodash/sortBy"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var input_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/controls/input"));
var field_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/field"));
var types_1 = require("../../types");
var utils_1 = require("../../utils");
var eventIdField_1 = tslib_1.__importDefault(require("./eventIdField"));
var selectField_1 = tslib_1.__importDefault(require("./selectField"));
var sourceField_1 = tslib_1.__importDefault(require("./sourceField"));
var Form = /** @class */ (function (_super) {
    tslib_1.__extends(Form, _super);
    function Form() {
        var _a;
        var _this = _super.apply(this, tslib_1.__spreadArray([], tslib_1.__read(arguments))) || this;
        _this.state = { displayEventId: !!((_a = _this.props.eventId) === null || _a === void 0 ? void 0 : _a.value) };
        _this.handleChange = function (field) {
            return function (event) {
                _this.props.onChange(field, event.target.value);
            };
        };
        _this.handleToggleEventId = function () {
            _this.setState(function (prevState) { return ({ displayEventId: !prevState.displayEventId }); });
        };
        return _this;
    }
    Form.prototype.render = function () {
        var _a = this.props, values = _a.values, onChange = _a.onChange, errors = _a.errors, onValidate = _a.onValidate, sourceSuggestions = _a.sourceSuggestions, onUpdateEventId = _a.onUpdateEventId, eventId = _a.eventId;
        var method = values.method, type = values.type, source = values.source;
        var displayEventId = this.state.displayEventId;
        return (<React.Fragment>
        <FieldGroup hasTwoColumns={values.method === types_1.MethodType.REPLACE}>
          <field_1.default data-test-id="method-field" label={locale_1.t('Method')} help={locale_1.t('What to do')} inline={false} flexibleControlStateSize stacked showHelpInTooltip>
            <selectField_1.default placeholder={locale_1.t('Select method')} name="method" options={sortBy_1.default(Object.values(types_1.MethodType)).map(function (value) { return (tslib_1.__assign(tslib_1.__assign({}, utils_1.getMethodLabel(value)), { value: value })); })} value={method} onChange={function (value) { return onChange('method', value === null || value === void 0 ? void 0 : value.value); }}/>
          </field_1.default>
          {values.method === types_1.MethodType.REPLACE && (<field_1.default data-test-id="placeholder-field" label={locale_1.t('Custom Placeholder (Optional)')} help={locale_1.t('It will replace the default placeholder [Filtered]')} inline={false} flexibleControlStateSize stacked showHelpInTooltip>
              <input_1.default type="text" name="placeholder" placeholder={"[" + locale_1.t('Filtered') + "]"} onChange={this.handleChange('placeholder')} value={values.placeholder}/>
            </field_1.default>)}
        </FieldGroup>
        <FieldGroup hasTwoColumns={values.type === types_1.RuleType.PATTERN}>
          <field_1.default data-test-id="type-field" label={locale_1.t('Data Type')} help={locale_1.t('What to look for. Use an existing pattern or define your own using regular expressions.')} inline={false} flexibleControlStateSize stacked showHelpInTooltip>
            <selectField_1.default placeholder={locale_1.t('Select type')} name="type" options={sortBy_1.default(Object.values(types_1.RuleType)).map(function (value) { return ({
                label: utils_1.getRuleLabel(value),
                value: value,
            }); })} value={type} onChange={function (value) { return onChange('type', value === null || value === void 0 ? void 0 : value.value); }}/>
          </field_1.default>
          {values.type === types_1.RuleType.PATTERN && (<field_1.default data-test-id="regex-field" label={locale_1.t('Regex matches')} help={locale_1.t('Custom regular expression (see documentation)')} inline={false} error={errors === null || errors === void 0 ? void 0 : errors.pattern} flexibleControlStateSize stacked required showHelpInTooltip>
              <RegularExpression type="text" name="pattern" placeholder={locale_1.t('[a-zA-Z0-9]+')} onChange={this.handleChange('pattern')} value={values.pattern} onBlur={onValidate('pattern')}/>
            </field_1.default>)}
        </FieldGroup>
        <ToggleWrapper>
          {displayEventId ? (<Toggle priority="link" onClick={this.handleToggleEventId}>
              {locale_1.t('Hide event ID field')}
              <icons_1.IconChevron direction="up" size="xs"/>
            </Toggle>) : (<Toggle priority="link" onClick={this.handleToggleEventId}>
              {locale_1.t('Use event ID for auto-completion')}
              <icons_1.IconChevron direction="down" size="xs"/>
            </Toggle>)}
        </ToggleWrapper>
        <SourceGroup isExpanded={displayEventId}>
          {displayEventId && (<eventIdField_1.default onUpdateEventId={onUpdateEventId} eventId={eventId}/>)}
          <sourceField_1.default onChange={function (value) { return onChange('source', value); }} value={source} error={errors === null || errors === void 0 ? void 0 : errors.source} onBlur={onValidate('source')} isRegExMatchesSelected={type === types_1.RuleType.PATTERN} suggestions={sourceSuggestions}/>
        </SourceGroup>
      </React.Fragment>);
    };
    return Form;
}(React.Component));
exports.default = Form;
var FieldGroup = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  margin-bottom: ", ";\n  @media (min-width: ", ") {\n    grid-gap: ", ";\n    ", "\n    margin-bottom: ", ";\n  }\n"], ["\n  display: grid;\n  margin-bottom: ", ";\n  @media (min-width: ", ") {\n    grid-gap: ", ";\n    ", "\n    margin-bottom: ", ";\n  }\n"])), space_1.default(2), function (p) { return p.theme.breakpoints[0]; }, space_1.default(2), function (p) { return p.hasTwoColumns && "grid-template-columns: 1fr 1fr;"; }, function (p) { return (p.hasTwoColumns ? 0 : space_1.default(2)); });
var SourceGroup = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  height: 65px;\n  transition: all 300ms cubic-bezier(0.4, 0, 0.2, 1) 0ms;\n  transition-property: height;\n  ", "\n"], ["\n  height: 65px;\n  transition: all 300ms cubic-bezier(0.4, 0, 0.2, 1) 0ms;\n  transition-property: height;\n  ", "\n"])), function (p) {
    return p.isExpanded &&
        "\n    border-radius: " + p.theme.borderRadius + ";\n    border: 1px solid " + p.theme.border + ";\n    box-shadow: " + p.theme.dropShadowLight + ";\n    margin: " + space_1.default(2) + " 0 " + space_1.default(3) + " 0;\n    padding: " + space_1.default(2) + ";\n    height: 180px;\n  ";
});
var RegularExpression = styled_1.default(input_1.default)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  font-family: ", ";\n"], ["\n  font-family: ", ";\n"])), function (p) { return p.theme.text.familyMono; });
var ToggleWrapper = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  justify-content: flex-end;\n"], ["\n  display: flex;\n  justify-content: flex-end;\n"])));
var Toggle = styled_1.default(button_1.default)(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  font-weight: 700;\n  color: ", ";\n  &:hover,\n  &:focus {\n    color: ", ";\n  }\n  > *:first-child {\n    display: grid;\n    grid-gap: ", ";\n    grid-template-columns: repeat(2, max-content);\n    align-items: center;\n  }\n"], ["\n  font-weight: 700;\n  color: ", ";\n  &:hover,\n  &:focus {\n    color: ", ";\n  }\n  > *:first-child {\n    display: grid;\n    grid-gap: ", ";\n    grid-template-columns: repeat(2, max-content);\n    align-items: center;\n  }\n"])), function (p) { return p.theme.subText; }, function (p) { return p.theme.textColor; }, space_1.default(0.5));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=index.jsx.map