Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var input_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/controls/input"));
var groupByField_1 = tslib_1.__importDefault(require("./groupByField"));
var metricSelectField_1 = tslib_1.__importDefault(require("./metricSelectField"));
function Queries(_a) {
    var metricMetas = _a.metricMetas, metricTags = _a.metricTags, queries = _a.queries, onRemoveQuery = _a.onRemoveQuery, onAddQuery = _a.onAddQuery, onChangeQuery = _a.onChangeQuery;
    function handleFieldChange(queryIndex, field) {
        var widgetQuery = queries[queryIndex];
        return function handleChange(value) {
            var _a;
            var newQuery = tslib_1.__assign(tslib_1.__assign({}, widgetQuery), (_a = {}, _a[field] = value, _a));
            onChangeQuery(queryIndex, newQuery);
        };
    }
    return (<Wrapper>
      {queries.map(function (query, queryIndex) {
            return (<Fields displayDeleteButton={queries.length > 1} key={queryIndex}>
            <metricSelectField_1.default metricMetas={metricMetas} metricMeta={query.metricMeta} aggregation={query.aggregation} onChange={function (field, value) { return handleFieldChange(queryIndex, field)(value); }}/>
            <groupByField_1.default metricTags={metricTags} groupBy={query.groupBy} onChange={function (v) { return handleFieldChange(queryIndex, 'groupBy')(v); }}/>
            <input_1.default type="text" name="legend" value={query.legend} placeholder={locale_1.t('Legend Alias')} onChange={function (event) {
                    return handleFieldChange(queryIndex, 'legend')(event.target.value);
                }} required/>
            {queries.length > 1 && (<react_1.Fragment>
                <ButtonDeleteWrapper>
                  <button_1.default onClick={function () {
                        onRemoveQuery(queryIndex);
                    }} size="small">
                    {locale_1.t('Delete Query')}
                  </button_1.default>
                </ButtonDeleteWrapper>
                <IconDeleteWrapper onClick={function () {
                        onRemoveQuery(queryIndex);
                    }}>
                  <icons_1.IconDelete aria-label={locale_1.t('Delete Query')}/>
                </IconDeleteWrapper>
              </react_1.Fragment>)}
          </Fields>);
        })}
      <div>
        <button_1.default size="small" icon={<icons_1.IconAdd isCircled/>} onClick={onAddQuery}>
          {locale_1.t('Add query')}
        </button_1.default>
      </div>
    </Wrapper>);
}
exports.default = Queries;
var IconDeleteWrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  height: 40px;\n  cursor: pointer;\n  display: none;\n\n  @media (min-width: ", ") {\n    display: flex;\n    align-items: center;\n  }\n"], ["\n  height: 40px;\n  cursor: pointer;\n  display: none;\n\n  @media (min-width: ", ") {\n    display: flex;\n    align-items: center;\n  }\n"])), function (p) { return p.theme.breakpoints[3]; });
var Fields = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n\n  @media (min-width: ", ") {\n    grid-template-columns: ", ";\n    grid-gap: ", ";\n    align-items: center;\n  }\n"], ["\n  display: grid;\n  grid-gap: ", ";\n\n  @media (min-width: ", ") {\n    grid-template-columns: ", ";\n    grid-gap: ", ";\n    align-items: center;\n  }\n"])), space_1.default(2), function (p) { return p.theme.breakpoints[3]; }, function (p) {
    return p.displayDeleteButton ? '1.3fr 1fr 0.5fr max-content' : '1.3fr 1fr 0.5fr';
}, space_1.default(1));
var Wrapper = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n  @media (max-width: ", ") {\n    ", " {\n      :not(:first-child) {\n        border-top: 1px solid ", ";\n        padding-top: ", ";\n      }\n    }\n  }\n"], ["\n  display: grid;\n  grid-gap: ", ";\n  @media (max-width: ", ") {\n    ", " {\n      :not(:first-child) {\n        border-top: 1px solid ", ";\n        padding-top: ", ";\n      }\n    }\n  }\n"])), space_1.default(2), function (p) { return p.theme.breakpoints[3]; }, Fields, function (p) { return p.theme.border; }, space_1.default(2));
var ButtonDeleteWrapper = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  justify-content: flex-end;\n  @media (min-width: ", ") {\n    display: none;\n  }\n"], ["\n  display: flex;\n  justify-content: flex-end;\n  @media (min-width: ", ") {\n    display: none;\n  }\n"])), function (p) { return p.theme.breakpoints[3]; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=queries.jsx.map