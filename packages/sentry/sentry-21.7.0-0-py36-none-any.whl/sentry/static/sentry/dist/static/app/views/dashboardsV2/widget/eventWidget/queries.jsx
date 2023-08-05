Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var searchBar_1 = tslib_1.__importDefault(require("app/components/events/searchBar"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var input_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/controls/input"));
var field_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/field"));
var utils_1 = require("../utils");
function Queries(_a) {
    var queries = _a.queries, selectedProjectIds = _a.selectedProjectIds, organization = _a.organization, displayType = _a.displayType, onRemoveQuery = _a.onRemoveQuery, onAddQuery = _a.onAddQuery, onChangeQuery = _a.onChangeQuery, errors = _a.errors;
    function handleFieldChange(queryIndex, field) {
        var widgetQuery = queries[queryIndex];
        return function handleChange(value) {
            var _a;
            var newQuery = tslib_1.__assign(tslib_1.__assign({}, widgetQuery), (_a = {}, _a[field] = value, _a));
            onChangeQuery(queryIndex, newQuery);
        };
    }
    function canAddNewQuery() {
        var rightDisplayType = [
            utils_1.DisplayType.LINE,
            utils_1.DisplayType.AREA,
            utils_1.DisplayType.STACKED_AREA,
            utils_1.DisplayType.BAR,
        ].includes(displayType);
        var underQueryLimit = queries.length < 3;
        return rightDisplayType && underQueryLimit;
    }
    var hideLegendAlias = [
        utils_1.DisplayType.TABLE,
        utils_1.DisplayType.WORLD_MAP,
        utils_1.DisplayType.BIG_NUMBER,
    ].includes(displayType);
    return (<div>
      {queries.map(function (query, queryIndex) {
            var displayDeleteButton = queries.length > 1;
            var displayLegendAlias = !hideLegendAlias;
            return (<StyledField key={queryIndex} inline={false} flexibleControlStateSize stacked error={errors === null || errors === void 0 ? void 0 : errors[queryIndex].conditions}>
            <Fields displayDeleteButton={displayDeleteButton} displayLegendAlias={displayLegendAlias}>
              <searchBar_1.default organization={organization} projectIds={selectedProjectIds} query={query.conditions} fields={[]} onSearch={handleFieldChange(queryIndex, 'conditions')} onBlur={handleFieldChange(queryIndex, 'conditions')} useFormWrapper={false}/>
              {displayLegendAlias && (<input_1.default type="text" name="name" required value={query.name} placeholder={locale_1.t('Legend Alias')} onChange={function (event) {
                        return handleFieldChange(queryIndex, 'name')(event.target.value);
                    }}/>)}
              {displayDeleteButton && (<button_1.default size="zero" borderless onClick={function (event) {
                        event.preventDefault();
                        onRemoveQuery(queryIndex);
                    }} icon={<icons_1.IconDelete />} title={locale_1.t('Remove query')} label={locale_1.t('Remove query')}/>)}
            </Fields>
          </StyledField>);
        })}
      {canAddNewQuery() && (<button_1.default size="small" icon={<icons_1.IconAdd isCircled/>} onClick={function (event) {
                event.preventDefault();
                onAddQuery();
            }}>
          {locale_1.t('Add Query')}
        </button_1.default>)}
    </div>);
}
exports.default = Queries;
var fieldsColumns = function (p) {
    if (!p.displayDeleteButton && !p.displayLegendAlias) {
        return '1fr';
    }
    if (!p.displayDeleteButton) {
        return '1fr 33%';
    }
    if (!p.displayLegendAlias) {
        return '1fr max-content';
    }
    return '1fr 33% max-content';
};
var Fields = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: ", ";\n  grid-gap: ", ";\n  align-items: center;\n"], ["\n  display: grid;\n  grid-template-columns: ", ";\n  grid-gap: ", ";\n  align-items: center;\n"])), fieldsColumns, space_1.default(1));
var StyledField = styled_1.default(field_1.default)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  padding-right: 0;\n"], ["\n  padding-right: 0;\n"])));
var templateObject_1, templateObject_2;
//# sourceMappingURL=queries.jsx.map