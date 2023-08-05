Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_select_1 = require("react-select");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var selectControl_1 = tslib_1.__importDefault(require("app/components/forms/selectControl"));
var highlight_1 = tslib_1.__importDefault(require("app/components/highlight"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var locale_1 = require("app/locale");
var selectField_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/selectField"));
function MetricSelectField(_a) {
    var _b, _c;
    var metricMetas = _a.metricMetas, metricMeta = _a.metricMeta, aggregation = _a.aggregation, onChange = _a.onChange;
    var operations = (_b = metricMeta === null || metricMeta === void 0 ? void 0 : metricMeta.operations) !== null && _b !== void 0 ? _b : [];
    return (<Wrapper>
      <StyledSelectField name="metric" choices={metricMetas.map(function (metricMetaChoice) { return [
            metricMetaChoice.name,
            metricMetaChoice.name,
        ]; })} placeholder={locale_1.t('Select metric')} onChange={function (value) {
            var newMetric = metricMetas.find(function (metricMetaChoice) { return metricMetaChoice.name === value; });
            onChange('metricMeta', newMetric);
        }} value={(_c = metricMeta === null || metricMeta === void 0 ? void 0 : metricMeta.name) !== null && _c !== void 0 ? _c : ''} components={{
            Option: function (_a) {
                var label = _a.label, optionProps = tslib_1.__rest(_a, ["label"]);
                var selectProps = optionProps.selectProps;
                var inputValue = selectProps.inputValue;
                return (<react_select_1.components.Option label={label} {...optionProps}>
                <highlight_1.default text={inputValue !== null && inputValue !== void 0 ? inputValue : ''}>{label}</highlight_1.default>
              </react_select_1.components.Option>);
            },
        }} styles={{
            control: function (provided) { return (tslib_1.__assign(tslib_1.__assign({}, provided), { borderTopRightRadius: 0, borderBottomRightRadius: 0, borderRight: 'none', boxShadow: 'none' })); },
        }} inline={false} flexibleControlStateSize stacked allowClear/>
      <tooltip_1.default disabled={!!operations.length} title={locale_1.t('Please select a metric to enable this field')}>
        <selectControl_1.default name="aggregation" placeholder={locale_1.t('Aggr')} disabled={!operations.length} options={operations.map(function (operation) { return ({
            label: operation === 'count_unique' ? 'unique' : operation,
            value: operation,
        }); })} value={aggregation !== null && aggregation !== void 0 ? aggregation : ''} onChange={function (_a) {
        var value = _a.value;
        return onChange('aggregation', value);
    }} styles={{
            control: function (provided) { return (tslib_1.__assign(tslib_1.__assign({}, provided), { borderTopLeftRadius: 0, borderBottomLeftRadius: 0, boxShadow: 'none' })); },
        }}/>
      </tooltip_1.default>
    </Wrapper>);
}
exports.default = MetricSelectField;
var StyledSelectField = styled_1.default(selectField_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  padding-right: 0;\n  padding-bottom: 0;\n"], ["\n  padding-right: 0;\n  padding-bottom: 0;\n"])));
var Wrapper = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 1fr 0.5fr;\n"], ["\n  display: grid;\n  grid-template-columns: 1fr 0.5fr;\n"])));
var templateObject_1, templateObject_2;
//# sourceMappingURL=metricSelectField.jsx.map