Object.defineProperty(exports, "__esModule", { value: true });
exports.QueryFieldWrapper = void 0;
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var fields_1 = require("app/utils/discover/fields");
var columnEditCollection_1 = tslib_1.__importDefault(require("app/views/eventsV2/table/columnEditCollection"));
var queryField_1 = require("app/views/eventsV2/table/queryField");
var types_1 = require("app/views/eventsV2/table/types");
var field_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/field"));
function WidgetQueryFields(_a) {
    var displayType = _a.displayType, errors = _a.errors, fields = _a.fields, fieldOptions = _a.fieldOptions, organization = _a.organization, onChange = _a.onChange, style = _a.style;
    // Handle new fields being added.
    function handleAdd(event) {
        event.preventDefault();
        var newFields = tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(fields)), ['']);
        onChange(newFields);
    }
    function handleRemove(event, fieldIndex) {
        event.preventDefault();
        var newFields = tslib_1.__spreadArray([], tslib_1.__read(fields));
        newFields.splice(fieldIndex, 1);
        onChange(newFields);
    }
    function handleChangeField(value, fieldIndex) {
        var newFields = tslib_1.__spreadArray([], tslib_1.__read(fields));
        newFields[fieldIndex] = fields_1.generateFieldAsString(value);
        onChange(newFields);
    }
    function handleColumnChange(columns) {
        var newFields = columns.map(fields_1.generateFieldAsString);
        onChange(newFields);
    }
    if (displayType === 'table') {
        return (<field_1.default data-test-id="columns" label={locale_1.t('Columns')} inline={false} style={tslib_1.__assign({ padding: space_1.default(1) + " 0" }, (style !== null && style !== void 0 ? style : {}))} error={errors === null || errors === void 0 ? void 0 : errors.fields} flexibleControlStateSize stacked required>
        <StyledColumnEditCollection columns={fields.map(function (field) { return fields_1.explodeField({ field: field }); })} onChange={handleColumnChange} fieldOptions={fieldOptions} organization={organization}/>
      </field_1.default>);
    }
    var hideAddYAxisButton = (['world_map', 'big_number'].includes(displayType) && fields.length === 1) ||
        (['line', 'area', 'stacked_area', 'bar'].includes(displayType) &&
            fields.length === 3);
    // Any function/field choice for Big Number widgets is legal since the
    // data source is from an endpoint that is not timeseries-based.
    // The function/field choice for World Map widget will need to be numeric-like.
    // Column builder for Table widget is already handled above.
    var doNotValidateYAxis = displayType === 'big_number';
    return (<field_1.default data-test-id="y-axis" label={locale_1.t('Y-Axis')} inline={false} style={tslib_1.__assign({ padding: space_1.default(2) + " 0 24px 0" }, (style !== null && style !== void 0 ? style : {}))} flexibleControlStateSize error={errors === null || errors === void 0 ? void 0 : errors.fields} required stacked>
      {fields.map(function (field, i) {
            var fieldValue = fields_1.explodeField({ field: field });
            return (<exports.QueryFieldWrapper key={field + ":" + i}>
            <queryField_1.QueryField fieldValue={fieldValue} fieldOptions={fieldOptions} onChange={function (value) { return handleChangeField(value, i); }} filterPrimaryOptions={function (option) {
                    // Only validate function names for timeseries widgets and
                    // world map widgets.
                    if (!doNotValidateYAxis &&
                        option.value.kind === types_1.FieldValueKind.FUNCTION) {
                        var primaryOutput = fields_1.aggregateFunctionOutputType(option.value.meta.name, undefined);
                        if (primaryOutput) {
                            // If a function returns a specific type, then validate it.
                            return fields_1.isLegalYAxisType(primaryOutput);
                        }
                    }
                    return option.value.kind === types_1.FieldValueKind.FUNCTION;
                }} filterAggregateParameters={function (option) {
                    // Only validate function parameters for timeseries widgets and
                    // world map widgets.
                    if (doNotValidateYAxis) {
                        return true;
                    }
                    if (fieldValue.kind !== 'function') {
                        return true;
                    }
                    var functionName = fieldValue.function[0];
                    var primaryOutput = fields_1.aggregateFunctionOutputType(functionName, option.value.meta.name);
                    if (primaryOutput) {
                        return fields_1.isLegalYAxisType(primaryOutput);
                    }
                    if (option.value.kind === types_1.FieldValueKind.FUNCTION) {
                        // Functions are not legal options as an aggregate/function parameter.
                        return false;
                    }
                    return fields_1.isLegalYAxisType(option.value.meta.dataType);
                }}/>
            {fields.length > 1 && (<button_1.default size="zero" borderless onClick={function (event) { return handleRemove(event, i); }} icon={<icons_1.IconDelete />} title={locale_1.t('Remove this Y-Axis')} label={locale_1.t('Remove this Y-Axis')}/>)}
          </exports.QueryFieldWrapper>);
        })}
      {!hideAddYAxisButton && (<div>
          <button_1.default size="small" icon={<icons_1.IconAdd isCircled/>} onClick={handleAdd}>
            {locale_1.t('Add Overlay')}
          </button_1.default>
        </div>)}
    </field_1.default>);
}
var StyledColumnEditCollection = styled_1.default(columnEditCollection_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  margin-top: ", ";\n"], ["\n  margin-top: ", ";\n"])), space_1.default(1));
exports.QueryFieldWrapper = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  margin-bottom: ", ";\n\n  > * + * {\n    margin-left: ", ";\n  }\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  margin-bottom: ", ";\n\n  > * + * {\n    margin-left: ", ";\n  }\n"])), space_1.default(1), space_1.default(1));
exports.default = WidgetQueryFields;
var templateObject_1, templateObject_2;
//# sourceMappingURL=widgetQueryFields.jsx.map