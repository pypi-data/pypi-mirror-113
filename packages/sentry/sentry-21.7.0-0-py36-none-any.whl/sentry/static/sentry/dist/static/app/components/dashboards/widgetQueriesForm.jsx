Object.defineProperty(exports, "__esModule", { value: true });
exports.SearchConditionsWrapper = void 0;
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var cloneDeep_1 = tslib_1.__importDefault(require("lodash/cloneDeep"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var searchBar_1 = tslib_1.__importDefault(require("app/components/events/searchBar"));
var selectControl_1 = tslib_1.__importDefault(require("app/components/forms/selectControl"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var fields_1 = require("app/utils/discover/fields");
var input_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/controls/input"));
var field_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/field"));
var widgetQueryFields_1 = tslib_1.__importDefault(require("./widgetQueryFields"));
var generateOrderOptions = function (fields) {
    var options = [];
    fields.forEach(function (field) {
        var alias = fields_1.getAggregateAlias(field);
        options.push({ label: locale_1.t('%s asc', field), value: alias });
        options.push({ label: locale_1.t('%s desc', field), value: "-" + alias });
    });
    return options;
};
/**
 * Contain widget queries interactions and signal changes via the onChange
 * callback. This component's state should live in the parent.
 */
var WidgetQueriesForm = /** @class */ (function (_super) {
    tslib_1.__extends(WidgetQueriesForm, _super);
    function WidgetQueriesForm() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        // Handle scalar field values changing.
        _this.handleFieldChange = function (queryIndex, field) {
            var _a = _this.props, queries = _a.queries, onChange = _a.onChange;
            var widgetQuery = queries[queryIndex];
            return function handleChange(value) {
                var _a;
                var newQuery = tslib_1.__assign(tslib_1.__assign({}, widgetQuery), (_a = {}, _a[field] = value, _a));
                onChange(queryIndex, newQuery);
            };
        };
        return _this;
    }
    WidgetQueriesForm.prototype.getFirstQueryError = function (key) {
        var errors = this.props.errors;
        if (!errors) {
            return undefined;
        }
        return errors.find(function (queryError) { return queryError && queryError[key]; });
    };
    WidgetQueriesForm.prototype.render = function () {
        var _this = this;
        var _a;
        var _b = this.props, organization = _b.organization, selection = _b.selection, errors = _b.errors, queries = _b.queries, canAddSearchConditions = _b.canAddSearchConditions, handleAddSearchConditions = _b.handleAddSearchConditions, handleDeleteQuery = _b.handleDeleteQuery, displayType = _b.displayType, fieldOptions = _b.fieldOptions, onChange = _b.onChange;
        var hideLegendAlias = ['table', 'world_map', 'big_number'].includes(displayType);
        return (<QueryWrapper>
        {queries.map(function (widgetQuery, queryIndex) {
                return (<field_1.default key={queryIndex} label={queryIndex === 0 ? locale_1.t('Query') : null} inline={false} style={{ paddingBottom: "8px" }} flexibleControlStateSize stacked error={errors === null || errors === void 0 ? void 0 : errors[queryIndex].conditions}>
              <exports.SearchConditionsWrapper>
                <StyledSearchBar searchSource="widget_builder" organization={organization} projectIds={selection.projects} query={widgetQuery.conditions} fields={[]} onSearch={_this.handleFieldChange(queryIndex, 'conditions')} onBlur={_this.handleFieldChange(queryIndex, 'conditions')} useFormWrapper={false}/>
                {!hideLegendAlias && (<LegendAliasInput type="text" name="name" required value={widgetQuery.name} placeholder={locale_1.t('Legend Alias')} onChange={function (event) {
                            return _this.handleFieldChange(queryIndex, 'name')(event.target.value);
                        }}/>)}
                {queries.length > 1 && (<button_1.default size="zero" borderless onClick={function (event) {
                            event.preventDefault();
                            handleDeleteQuery(queryIndex);
                        }} icon={<icons_1.IconDelete />} title={locale_1.t('Remove query')} label={locale_1.t('Remove query')}/>)}
              </exports.SearchConditionsWrapper>
            </field_1.default>);
            })}
        {canAddSearchConditions && (<button_1.default size="small" icon={<icons_1.IconAdd isCircled/>} onClick={function (event) {
                    event.preventDefault();
                    handleAddSearchConditions();
                }}>
            {locale_1.t('Add Query')}
          </button_1.default>)}
        <widgetQueryFields_1.default displayType={displayType} fieldOptions={fieldOptions} errors={this.getFirstQueryError('fields')} fields={queries[0].fields} organization={organization} onChange={function (fields) {
                queries.forEach(function (widgetQuery, queryIndex) {
                    var newQuery = cloneDeep_1.default(widgetQuery);
                    newQuery.fields = fields;
                    onChange(queryIndex, newQuery);
                });
            }}/>
        {displayType === 'table' && (<field_1.default label={locale_1.t('Sort by')} inline={false} flexibleControlStateSize stacked error={(_a = this.getFirstQueryError('orderby')) === null || _a === void 0 ? void 0 : _a.orderby} style={{ marginBottom: space_1.default(1) }}>
            <selectControl_1.default value={queries[0].orderby} name="orderby" options={generateOrderOptions(queries[0].fields)} onChange={function (option) {
                    return _this.handleFieldChange(0, 'orderby')(option.value);
                }} onSelectResetsInput={false} onCloseResetsInput={false} onBlurResetsInput={false}/>
          </field_1.default>)}
      </QueryWrapper>);
    };
    return WidgetQueriesForm;
}(React.Component));
var QueryWrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  position: relative;\n"], ["\n  position: relative;\n"])));
exports.SearchConditionsWrapper = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n\n  > * + * {\n    margin-left: ", ";\n  }\n"], ["\n  display: flex;\n  align-items: center;\n\n  > * + * {\n    margin-left: ", ";\n  }\n"])), space_1.default(1));
var StyledSearchBar = styled_1.default(searchBar_1.default)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  flex-grow: 1;\n"], ["\n  flex-grow: 1;\n"])));
var LegendAliasInput = styled_1.default(input_1.default)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  width: 33%;\n"], ["\n  width: 33%;\n"])));
exports.default = WidgetQueriesForm;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=widgetQueriesForm.jsx.map