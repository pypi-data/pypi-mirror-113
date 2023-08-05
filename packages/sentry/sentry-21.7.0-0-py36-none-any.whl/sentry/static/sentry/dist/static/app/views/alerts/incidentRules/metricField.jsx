Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_2 = require("@emotion/react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var locale_1 = require("app/locale");
var fields_1 = require("app/utils/discover/fields");
var options_1 = require("app/views/alerts/wizard/options");
var queryField_1 = require("app/views/eventsV2/table/queryField");
var types_1 = require("app/views/eventsV2/table/types");
var utils_1 = require("app/views/eventsV2/utils");
var formField_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/formField"));
var constants_1 = require("./constants");
var presets_1 = require("./presets");
var types_2 = require("./types");
var getFieldOptionConfig = function (_a) {
    var dataset = _a.dataset, alertType = _a.alertType;
    var config;
    var hidePrimarySelector = false;
    var hideParameterSelector = false;
    if (alertType) {
        config = constants_1.getWizardAlertFieldConfig(alertType, dataset);
        hidePrimarySelector = options_1.hidePrimarySelectorSet.has(alertType);
        hideParameterSelector = options_1.hideParameterSelectorSet.has(alertType);
    }
    else {
        config = dataset === types_2.Dataset.ERRORS ? constants_1.errorFieldConfig : constants_1.transactionFieldConfig;
    }
    var aggregations = Object.fromEntries(config.aggregations.map(function (key) {
        // TODO(scttcper): Temporary hack for default value while we handle the translation of user
        if (key === 'count_unique') {
            var agg = fields_1.AGGREGATIONS[key];
            agg.getFieldOverrides = function () {
                return { defaultValue: 'tags[sentry:user]' };
            };
            return [key, agg];
        }
        return [key, fields_1.AGGREGATIONS[key]];
    }));
    var fields = Object.fromEntries(config.fields.map(function (key) {
        // XXX(epurkhiser): Temporary hack while we handle the translation of user ->
        // tags[sentry:user].
        if (key === 'user') {
            return ['tags[sentry:user]', 'string'];
        }
        return [key, fields_1.FIELDS[key]];
    }));
    var measurementKeys = config.measurementKeys;
    return {
        fieldOptionsConfig: { aggregations: aggregations, fields: fields, measurementKeys: measurementKeys },
        hidePrimarySelector: hidePrimarySelector,
        hideParameterSelector: hideParameterSelector,
    };
};
var help = function (_a) {
    var name = _a.name, model = _a.model;
    var aggregate = model.getValue(name);
    var presets = presets_1.PRESET_AGGREGATES.filter(function (preset) {
        return preset.validDataset.includes(model.getValue('dataset'));
    })
        .map(function (preset) { return (tslib_1.__assign(tslib_1.__assign({}, preset), { selected: preset.match.test(aggregate) })); })
        .map(function (preset, i, list) { return (<react_1.Fragment key={preset.name}>
        <tooltip_1.default title={locale_1.t('This preset is selected')} disabled={!preset.selected}>
          <PresetButton type="button" onClick={function () { return model.setValue(name, preset.default); }} disabled={preset.selected}>
            {preset.name}
          </PresetButton>
        </tooltip_1.default>
        {i + 1 < list.length && ', '}
      </react_1.Fragment>); });
    return locale_1.tct('Choose an aggregate function. Not sure what to select, try a preset: [presets]', { presets: presets });
};
var MetricField = function (_a) {
    var organization = _a.organization, columnWidth = _a.columnWidth, inFieldLabels = _a.inFieldLabels, alertType = _a.alertType, props = tslib_1.__rest(_a, ["organization", "columnWidth", "inFieldLabels", "alertType"]);
    return (<formField_1.default help={help} {...props}>
    {function (_a) {
            var _b;
            var onChange = _a.onChange, value = _a.value, model = _a.model, disabled = _a.disabled;
            var dataset = model.getValue('dataset');
            var _c = getFieldOptionConfig({
                dataset: dataset,
                alertType: alertType,
            }), fieldOptionsConfig = _c.fieldOptionsConfig, hidePrimarySelector = _c.hidePrimarySelector, hideParameterSelector = _c.hideParameterSelector;
            var fieldOptions = utils_1.generateFieldOptions(tslib_1.__assign({ organization: organization }, fieldOptionsConfig));
            var fieldValue = fields_1.explodeFieldString(value !== null && value !== void 0 ? value : '');
            var fieldKey = (fieldValue === null || fieldValue === void 0 ? void 0 : fieldValue.kind) === types_1.FieldValueKind.FUNCTION
                ? "function:" + fieldValue.function[0]
                : '';
            var selectedField = (_b = fieldOptions[fieldKey]) === null || _b === void 0 ? void 0 : _b.value;
            var numParameters = (selectedField === null || selectedField === void 0 ? void 0 : selectedField.kind) === types_1.FieldValueKind.FUNCTION
                ? selectedField.meta.parameters.length
                : 0;
            var parameterColumns = numParameters - (hideParameterSelector ? 1 : 0) - (hidePrimarySelector ? 1 : 0);
            return (<react_1.Fragment>
          <StyledQueryField filterPrimaryOptions={function (option) { return option.value.kind === types_1.FieldValueKind.FUNCTION; }} fieldOptions={fieldOptions} fieldValue={fieldValue} onChange={function (v) { return onChange(fields_1.generateFieldAsString(v), {}); }} columnWidth={columnWidth} gridColumns={parameterColumns + 1} inFieldLabels={inFieldLabels} shouldRenderTag={false} disabled={disabled} hideParameterSelector={hideParameterSelector} hidePrimarySelector={hidePrimarySelector}/>
        </react_1.Fragment>);
        }}
  </formField_1.default>);
};
var StyledQueryField = styled_1.default(queryField_1.QueryField)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  ", "\n"], ["\n  ", "\n"])), function (p) {
    return p.columnWidth && react_2.css(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n      width: ", "px;\n    "], ["\n      width: ", "px;\n    "])), p.gridColumns * p.columnWidth);
});
var PresetButton = styled_1.default(button_1.default)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  ", "\n"], ["\n  ", "\n"])), function (p) {
    return p.disabled && react_2.css(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n      color: ", ";\n      &:hover,\n      &:focus {\n        color: ", ";\n      }\n    "], ["\n      color: ", ";\n      &:hover,\n      &:focus {\n        color: ", ";\n      }\n    "])), p.theme.textColor, p.theme.textColor);
});
PresetButton.defaultProps = {
    priority: 'link',
    borderless: true,
};
exports.default = MetricField;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=metricField.jsx.map