Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var checkboxFancy_1 = tslib_1.__importDefault(require("app/components/checkboxFancy/checkboxFancy"));
var dropdownAutoComplete_1 = tslib_1.__importDefault(require("app/components/dropdownAutoComplete"));
var highlight_1 = tslib_1.__importDefault(require("app/components/highlight"));
var textOverflow_1 = tslib_1.__importDefault(require("app/components/textOverflow"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var input_1 = require("app/styles/input");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
function GroupByField(_a) {
    var metricTags = _a.metricTags, _b = _a.groupBy, groupBy = _b === void 0 ? [] : _b, onChange = _a.onChange;
    var hasSelected = !!groupBy.length;
    function handleClick(tag) {
        if (groupBy.includes(tag)) {
            var filteredGroupBy = groupBy.filter(function (groupByOption) { return groupByOption !== tag; });
            onChange(filteredGroupBy);
            return;
        }
        onChange(tslib_1.__spreadArray([], tslib_1.__read(new Set(tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(groupBy)), [tag])))));
    }
    function handleUnselectAll(event) {
        event.stopPropagation();
        onChange([]);
    }
    return (<dropdownAutoComplete_1.default searchPlaceholder={locale_1.t('Search tag')} items={metricTags.map(function (metricTag) { return ({
            value: metricTag,
            searchKey: metricTag,
            label: function (_a) {
                var inputValue = _a.inputValue;
                return (<Item onClick={function () { return handleClick(metricTag); }}>
            <div>
              <highlight_1.default text={inputValue}>{metricTag}</highlight_1.default>
            </div>
            <checkboxFancy_1.default isChecked={groupBy.includes(metricTag)}/>
          </Item>);
            },
        }); })} style={{
            width: '100%',
            borderRadius: 0,
        }} maxHeight={110}>
      {function (_a) {
            var isOpen = _a.isOpen, getActorProps = _a.getActorProps;
            return (<Field {...getActorProps()} hasSelected={hasSelected} isOpen={isOpen}>
          {!hasSelected ? (<Placeholder>{locale_1.t('Group by')}</Placeholder>) : (<React.Fragment>
              <StyledTextOverflow>
                {groupBy.map(function (groupByOption) { return groupByOption; }).join(',')}
              </StyledTextOverflow>
              <StyledClose color={hasSelected ? 'textColor' : 'gray300'} onClick={handleUnselectAll}/>
            </React.Fragment>)}
          <ChevronWrapper>
            <icons_1.IconChevron direction={isOpen ? 'up' : 'down'} size="sm" color={isOpen ? 'textColor' : 'gray300'}/>
          </ChevronWrapper>
        </Field>);
        }}
    </dropdownAutoComplete_1.default>);
}
exports.default = GroupByField;
var Field = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  ", ";\n  padding: 0 10px;\n  min-width: 250px;\n  display: grid;\n  grid-template-columns: ", ";\n  resize: none;\n  overflow: hidden;\n  align-items: center;\n  ", "\n"], ["\n  ", ";\n  padding: 0 10px;\n  min-width: 250px;\n  display: grid;\n  grid-template-columns: ", ";\n  resize: none;\n  overflow: hidden;\n  align-items: center;\n  ", "\n"])), function (p) { return input_1.inputStyles(p); }, function (p) {
    return p.hasSelected ? '1fr max-content max-content' : '1fr  max-content';
}, function (p) {
    return p.isOpen &&
        "\n      border-bottom-left-radius: 0;\n      border-bottom-right-radius: 0;\n    ";
});
var Item = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 1fr max-content;\n  grid-gap: ", ";\n  word-break: break-all;\n"], ["\n  display: grid;\n  grid-template-columns: 1fr max-content;\n  grid-gap: ", ";\n  word-break: break-all;\n"])), space_1.default(1.5));
var ChevronWrapper = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  width: 14px;\n  height: 14px;\n  display: inline-flex;\n  align-items: center;\n  justify-content: center;\n  margin-left: ", ";\n"], ["\n  width: 14px;\n  height: 14px;\n  display: inline-flex;\n  align-items: center;\n  justify-content: center;\n  margin-left: ", ";\n"])), space_1.default(1));
var StyledClose = styled_1.default(icons_1.IconClose)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  height: 100%;\n  width: 10px;\n  padding: ", " 0;\n  stroke-width: 1.5;\n  margin-left: ", ";\n  box-sizing: content-box;\n"], ["\n  height: 100%;\n  width: 10px;\n  padding: ", " 0;\n  stroke-width: 1.5;\n  margin-left: ", ";\n  box-sizing: content-box;\n"])), space_1.default(1), space_1.default(1));
var Placeholder = styled_1.default('div')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  flex: 1;\n  color: ", ";\n  padding: 0 ", ";\n"], ["\n  flex: 1;\n  color: ", ";\n  padding: 0 ", ";\n"])), function (p) { return p.theme.gray200; }, space_1.default(0.25));
var StyledTextOverflow = styled_1.default(textOverflow_1.default)(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  flex: 1;\n"], ["\n  flex: 1;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6;
//# sourceMappingURL=groupByField.jsx.map