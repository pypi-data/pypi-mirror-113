Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var checkboxFancy_1 = tslib_1.__importDefault(require("app/components/checkboxFancy/checkboxFancy"));
var dropdownControl_1 = tslib_1.__importStar(require("app/components/dropdownControl"));
var list_1 = tslib_1.__importDefault(require("app/components/list"));
var listItem_1 = tslib_1.__importDefault(require("app/components/list/listItem"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var dropDownButton_1 = tslib_1.__importDefault(require("./dropDownButton"));
function SearchBarActionFilter(_a) {
    var options = _a.options, onChange = _a.onChange;
    var checkedQuantity = Object.values(options)
        .flatMap(function (option) { return option; })
        .filter(function (option) { return option.isChecked; }).length;
    function handleClick(category, option) {
        var _a;
        var updatedOptions = tslib_1.__assign(tslib_1.__assign({}, options), (_a = {}, _a[category] = options[category].map(function (groupedOption) {
            if (option.id === groupedOption.id) {
                return tslib_1.__assign(tslib_1.__assign({}, groupedOption), { isChecked: !groupedOption.isChecked });
            }
            return groupedOption;
        }), _a));
        onChange(updatedOptions);
    }
    return (<Wrapper>
      <dropdownControl_1.default button={function (_a) {
            var isOpen = _a.isOpen, getActorProps = _a.getActorProps;
            return (<dropDownButton_1.default isOpen={isOpen} getActorProps={getActorProps} checkedQuantity={checkedQuantity}/>);
        }}>
        {function (_a) {
            var getMenuProps = _a.getMenuProps, isOpen = _a.isOpen;
            return (<StyledContent {...getMenuProps()} data-test-id="filter-dropdown-menu" alignMenu="left" width="240px" isOpen={isOpen} blendWithActor blendCorner>
            {Object.keys(options).map(function (category) { return (<react_1.Fragment key={category}>
                <Header>{category}</Header>
                <list_1.default>
                  {options[category].map(function (groupedOption) {
                        var symbol = groupedOption.symbol, isChecked = groupedOption.isChecked, id = groupedOption.id, description = groupedOption.description;
                        return (<StyledListItem key={id} onClick={function (event) {
                                event.stopPropagation();
                                handleClick(category, groupedOption);
                            }} isChecked={isChecked} hasDescription={!!description}>
                        {symbol}
                        {description && <Description>{description}</Description>}
                        <checkboxFancy_1.default isChecked={isChecked}/>
                      </StyledListItem>);
                    })}
                </list_1.default>
              </react_1.Fragment>); })}
          </StyledContent>);
        }}
      </dropdownControl_1.default>
    </Wrapper>);
}
exports.default = SearchBarActionFilter;
var Wrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  position: relative;\n  display: flex;\n"], ["\n  position: relative;\n  display: flex;\n"])));
var StyledContent = styled_1.default(dropdownControl_1.Content)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  top: calc(100% + ", " - 1px);\n  border-radius: ", ";\n  > * :last-child {\n    margin-bottom: -1px;\n  }\n"], ["\n  top: calc(100% + ", " - 1px);\n  border-radius: ", ";\n  > * :last-child {\n    margin-bottom: -1px;\n  }\n"])), space_1.default(0.5), function (p) { return p.theme.borderRadius; });
var Header = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  margin: 0;\n  background-color: ", ";\n  color: ", ";\n  font-weight: normal;\n  font-size: ", ";\n  padding: ", " ", ";\n  border-bottom: 1px solid ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  margin: 0;\n  background-color: ", ";\n  color: ", ";\n  font-weight: normal;\n  font-size: ", ";\n  padding: ", " ", ";\n  border-bottom: 1px solid ", ";\n"])), function (p) { return p.theme.backgroundSecondary; }, function (p) { return p.theme.gray300; }, function (p) { return p.theme.fontSizeMedium; }, space_1.default(1), space_1.default(2), function (p) { return p.theme.border; });
var StyledListItem = styled_1.default(listItem_1.default)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: ", ";\n  grid-column-gap: ", ";\n  padding: ", " ", ";\n  align-items: center;\n  cursor: pointer;\n  border-bottom: 1px solid ", ";\n  ", " {\n    opacity: ", ";\n  }\n\n  :hover {\n    background-color: ", ";\n    ", " {\n      opacity: 1;\n    }\n    span {\n      color: ", ";\n      text-decoration: underline;\n    }\n  }\n"], ["\n  display: grid;\n  grid-template-columns: ", ";\n  grid-column-gap: ", ";\n  padding: ", " ", ";\n  align-items: center;\n  cursor: pointer;\n  border-bottom: 1px solid ", ";\n  ", " {\n    opacity: ", ";\n  }\n\n  :hover {\n    background-color: ", ";\n    ", " {\n      opacity: 1;\n    }\n    span {\n      color: ", ";\n      text-decoration: underline;\n    }\n  }\n"])), function (p) {
    return p.hasDescription ? 'max-content 1fr max-content' : '1fr max-content';
}, space_1.default(1), space_1.default(1), space_1.default(2), function (p) { return p.theme.border; }, checkboxFancy_1.default, function (p) { return (p.isChecked ? 1 : 0.3); }, function (p) { return p.theme.backgroundSecondary; }, checkboxFancy_1.default, function (p) { return p.theme.blue300; });
var Description = styled_1.default('div')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n"], ["\n  font-size: ", ";\n"])), function (p) { return p.theme.fontSizeMedium; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=searchBarActionFilter.jsx.map